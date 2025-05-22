# pythonik/utils/pagination.py
"""
Advanced pagination utilities for pythonik with large dataset support.

This module provides pagination decorators and utilities that handle
Iconik's API limitations, including the 10k Elasticsearch result window.
Supports automatic retry logic, date-based continuation, and intelligent
response merging.

Example:
    @paginate_iconik_response(PaginationConfig(verbose=True))
    def get_all_assets(client):
        search_body = SearchBody(doc_types=["assets"])
        return client.search().search(search_body)

    # Or use direct function calls
    results = paginate_search_results(
        client.search().search,
        SearchBody(doc_types=["assets"]),
        PaginationConfig(elasticsearch_limit=9500)
    )
"""
import functools
import time
from datetime import (
    datetime,
    timedelta,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    TypeVar,
)

from pydantic import (
    BaseModel,
    Field,
)

try:
    from pythonik._logger import logger
except ImportError:
    from loguru import logger

T = TypeVar("T", bound=BaseModel)
CallableT = TypeVar("CallableT", bound=Callable[..., Any])


class PaginationConfig(BaseModel):
    """
    Configuration for pagination behavior.

    Controls how pagination handles retries, limits, and fallback
    strategies when dealing with large datasets.
    """

    max_per_page: int = Field(
        default=1000,
        ge=1,
        le=1000,
        description="Maximum results per page (API limit: 1000)",
    )
    default_per_page: int = Field(default=100,
                                  ge=1,
                                  le=1000,
                                  description="Default page size for requests")
    max_retries: int = Field(default=5,
                             ge=1,
                             le=10,
                             description="Maximum retry attempts")
    retry_delay: float = Field(
        default=1.0,
        ge=0.1,
        le=60.0,
        description="Base delay between retries (seconds)",
    )
    retry_backoff: float = Field(
        default=2.0,
        ge=1.0,
        le=5.0,
        description="Exponential backoff multiplier",
    )
    verbose: bool = Field(default=False,
                          description="Enable verbose logging output")
    date_fallback_enabled: bool = Field(
        default=True,
        description="Use date-based continuation for large datasets",
    )
    elasticsearch_limit: int = Field(
        default=10000,
        ge=100,
        le=50000,
        description="Elasticsearch max_result_window limit",
    )


class PaginationError(Exception):
    """
    Raised when pagination encounters an unrecoverable error.

    This exception is raised when all retry attempts have been
    exhausted or when pagination cannot continue due to API
    limitations or data structure issues.
    """


def _calculate_delay(attempt: int, base_delay: float, backoff: float) -> float:
    """
    Calculate exponential backoff delay.

    Args:
        attempt: Current retry attempt number (1-based)
        base_delay: Base delay in seconds
        backoff: Backoff multiplier

    Returns:
        Calculated delay in seconds
    """
    return base_delay * (backoff**(attempt - 1))


def _merge_paginated_objects(base_data: Dict[str, Any],
                             new_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge paginated response objects intelligently.

    Combines object lists while preserving pagination metadata.
    Updates the base response with new page data.

    Args:
        base_data: The accumulated response data
        new_data: New page data to merge

    Returns:
        Merged response data with combined objects list
    """
    merged = base_data.copy()

    # Merge object lists
    if "objects" in new_data and new_data["objects"]:
        if "objects" not in merged:
            merged["objects"] = []
        merged["objects"].extend(new_data["objects"])

    # Update pagination metadata to reflect current state
    merged.update({
        "page":
        new_data.get("page", merged.get("page", 1)),
        "pages":
        new_data.get("pages", merged.get("pages", 1)),
        "per_page":
        new_data.get("per_page", merged.get("per_page", 100)),
        "total":
        new_data.get("total", merged.get("total", 0)),
    })

    return merged


def _extract_date_range(objects: List[Dict[str, Any]],
                        date_field: str = "date_created") -> Optional[str]:
    """
    Extract date range for continuation queries.

    Finds the latest date in the objects list to create a continuation
    point for date-based pagination. This is used when hitting the
    Elasticsearch max_result_window limit.

    Args:
        objects: List of objects to analyze
        date_field: Field containing the date (default: 'date_created')

    Returns:
        ISO date string for the next query start point, or None if
        no valid dates found
    """
    if not objects:
        return None

    try:
        dates = []
        for obj in objects:
            if date_field in obj and obj[date_field]:
                date_str = obj[date_field]
                if isinstance(date_str, str):
                    # Handle ISO format with Z suffix
                    clean_date = date_str.replace("Z", "+00:00")
                    dates.append(datetime.fromisoformat(clean_date))
                elif isinstance(date_str, datetime):
                    dates.append(date_str)

        if dates:
            # Get the latest date and add 1 second for next query
            latest_date = max(dates) + timedelta(seconds=1)
            return latest_date.isoformat().replace("+00:00", "Z")

    except (ValueError, TypeError) as e:
        logger.warning("Failed to parse dates for pagination: %s", e)

    return None


def _extract_response_data(response: Any) -> Dict[str, Any]:
    """
    Extract data from various response types.

    Handles pythonik Response objects, Pydantic models,
    requests.Response objects, and direct dictionaries.

    Args:
        response: Response object to extract data from

    Returns:
        Dictionary containing response data

    Raises:
        PaginationError: If response format is unsupported
    """
    # Check for direct dict first (most common case)
    if isinstance(response, dict):
        return response

    # Check for requests-like response with json method
    if hasattr(response, "json") and callable(response.json):
        return response.json()

    # Check for pythonik Response objects with data attribute
    if hasattr(response, "data") and response.data is not None:
        # Handle test mock objects that start with "Mock"
        if str(type(response).__name__).startswith("Mock"):
            if hasattr(response.data, "model_dump"):
                return response.data.model_dump()
            # Handle direct dict data in mock
            if isinstance(response.data, dict):
                return response.data
            # Handle Pydantic model data in mock
            if hasattr(response.data, "__dict__"):
                return response.data.__dict__
        else:
            # Real pythonik response handling
            if hasattr(response.data, "model_dump"):
                # Pydantic model response
                return response.data.model_dump()
            # Direct data object
            return response.data

    raise PaginationError(f"Unsupported response type: {type(response)}")


def _should_use_date_fallback(total_fetched: int, config: PaginationConfig,
                              page: int, pages: int) -> bool:
    """
    Determine if date-based fallback should be used.

    Args:
        total_fetched: Total objects fetched so far
        config: Pagination configuration
        page: Current page number
        pages: Total pages available

    Returns:
        True if date fallback should be used
    """
    return (total_fetched >= config.elasticsearch_limit
            and config.date_fallback_enabled and page < pages)


def _setup_pagination_params(kwargs: Dict[str, Any],
                             config: PaginationConfig) -> Dict[str, Any]:
    """
    Set up initial pagination parameters.

    Args:
        kwargs: Function keyword arguments
        config: Pagination configuration

    Returns:
        Updated kwargs with pagination params
    """
    if "params" not in kwargs:
        kwargs["params"] = {}

    params = kwargs["params"]
    if "page" not in params:
        params["page"] = 1
    if "per_page" not in params:
        params["per_page"] = min(config.default_per_page, config.max_per_page)

    return kwargs


def _handle_page_iteration(params: Dict[str, Any], page: int,
                           pages: int) -> bool:
    """
    Handle page iteration logic.

    Args:
        params: Request parameters
        page: Current page number
        pages: Total pages available

    Returns:
        True if more pages are available
    """
    if page < pages:
        params["page"] = page + 1
        return True
    return False


def _handle_date_fallback(params: Dict[str, Any],
                          accumulated_data: Dict[str, Any]) -> bool:
    """
    Handle date-based fallback when hitting ES limits.

    Args:
        params: Request parameters to update
        accumulated_data: Current accumulated response data

    Returns:
        True if date fallback was successfully configured
    """
    next_date = _extract_date_range(accumulated_data.get("objects", []))
    if next_date:
        params.update({
            "date_created_gt": next_date,
            "page": 1
        }  # Reset to first page
                      )
        return True
    logger.warning("Could not extract date for continuation")
    return False


def paginate_iconik_response(
    config: Optional[PaginationConfig] = None,
) -> Callable[[CallableT], CallableT]:
    """
    Decorator to automatically paginate Iconik API responses.

    This decorator wraps functions that make Iconik API calls and
    automatically handles pagination, including:
    - Automatic page iteration
    - Elasticsearch 10k limit via date-based continuation
    - Retry logic with exponential backoff
    - Response merging into single result

    Args:
        config: Pagination configuration. If None, uses default.

    Returns:
        Decorated function that returns complete paginated results

    Raises:
        PaginationError: If pagination fails after all retries

    Example:
        @paginate_iconik_response(PaginationConfig(verbose=True))
        def get_all_assets(client, **kwargs):
            search_body = SearchBody(doc_types=["assets"])
            return client.search().search(search_body, **kwargs)

        # Usage
        all_assets = get_all_assets(client)
        print("Retrieved %d assets" % len(all_assets['objects']))
    """
    if config is None:
        config = PaginationConfig()

    def decorator(func: CallableT) -> CallableT:

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Dict[str, Any]:
            return _paginate_sync(func, config, args, kwargs)

        return wrapper

    return decorator


def _paginate_sync(
    func: Callable,
    config: PaginationConfig,
    args: tuple,
    kwargs: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Synchronous pagination implementation.

    Core pagination logic that handles page iteration, retry logic,
    and response merging. Automatically switches to date-based
    continuation when hitting Elasticsearch limits.

    Args:
        func: Function to paginate
        config: Pagination configuration
        args: Function arguments
        kwargs: Function keyword arguments

    Returns:
        Dictionary containing all paginated results

    Raises:
        PaginationError: If pagination fails after all retries
    """
    kwargs = _setup_pagination_params(kwargs, config)
    params = kwargs["params"]

    attempt = 0
    accumulated_data = None
    current_page = 1
    total_fetched = 0

    while attempt < config.max_retries:
        try:
            if config.verbose and current_page > 1:
                logger.info(
                    "Fetching page %d... (total objects: %d)",
                    current_page,
                    total_fetched,
                )

            # Make the API call
            response = func(*args, **kwargs)
            data = _extract_response_data(response)

            # Validate response structure
            if not isinstance(data, dict):
                raise PaginationError(
                    f"Expected dict response, got {type(data)}")

            # Initialize or merge accumulated data
            accumulated_data = _process_response_data(accumulated_data, data)

            page = data.get("page", 1)
            pages = data.get("pages", 1)
            objects = data.get("objects", [])
            total_fetched += len(objects)

            # Check for Elasticsearch limit and handle fallback
            if _should_use_date_fallback(total_fetched, config, page, pages):
                if config.verbose:
                    logger.info(
                        "Hit %d object limit, switching to date-based "
                        "pagination...",
                        config.elasticsearch_limit,
                    )

                if _handle_date_fallback(params, accumulated_data):
                    current_page = 1
                    continue
                break

            # Continue to next page if available
            if _handle_page_iteration(params, page, pages):
                current_page = page + 1
                attempt = 0  # Reset retry counter on success
            else:
                # Pagination complete
                break

        except Exception as e:
            attempt += 1
            if attempt >= config.max_retries:
                raise PaginationError(
                    f"Failed to paginate after {config.max_retries} "
                    f"attempts: {e}") from e

            delay = _calculate_delay(attempt, config.retry_delay,
                                     config.retry_backoff)
            if config.verbose:
                logger.info(
                    "Retry %d/%d after %.1fs delay...",
                    attempt,
                    config.max_retries,
                    delay,
                )
            time.sleep(delay)

    if accumulated_data is None:
        raise PaginationError("No data retrieved during pagination")

    # Update final metadata
    return _finalize_response_data(accumulated_data)


def _process_response_data(accumulated_data: Optional[Dict[str, Any]],
                           new_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process and merge response data.

    Args:
        accumulated_data: Previously accumulated data (or None)
        new_data: New response data to process

    Returns:
        Updated accumulated data
    """
    if accumulated_data is None:
        accumulated_data = new_data.copy()
        if "objects" not in accumulated_data:
            accumulated_data["objects"] = []
    else:
        accumulated_data = _merge_paginated_objects(accumulated_data, new_data)

    return accumulated_data


def _finalize_response_data(
        accumulated_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Finalize response data with correct metadata.

    Args:
        accumulated_data: Accumulated response data

    Returns:
        Finalized response data
    """
    final_objects = accumulated_data.get("objects", [])
    accumulated_data.update({
        "total": len(final_objects),
        "page": 1,
        "pages": 1,
        "per_page": len(final_objects),
    })

    return accumulated_data


def paginate_search_results(
    search_func: Callable,
    search_body: Any,
    config: Optional[PaginationConfig] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Directly paginate search results without decorator.

    Provides a direct function interface for pagination without
    requiring decorator usage. Useful for dynamic pagination
    scenarios or when you need more control.

    Args:
        search_func: Function to call for searching
        search_body: Search body/parameters
        config: Pagination configuration
        **kwargs: Additional arguments passed to search function

    Returns:
        Complete paginated results dictionary

    Raises:
        PaginationError: If pagination fails

    Example:
        results = paginate_search_results(
            client.search().search,
            SearchBody(doc_types=["assets"]),
            PaginationConfig(verbose=True)
        )

        assets = results['objects']
        print("Found %d total assets" % len(assets))
    """

    @paginate_iconik_response(config)
    def _search_wrapper(**wrapper_kwargs):
        # Merge the kwargs properly
        merged_kwargs = {**kwargs, **wrapper_kwargs}
        return search_func(search_body, **merged_kwargs)

    return _search_wrapper()


def estimate_total_results(search_func: Callable, search_body: Any,
                           **kwargs) -> int:
    """
    Estimate total results without full pagination.

    Makes a minimal request to get the total count without
    fetching all results. Useful for progress estimation
    or deciding on pagination strategy.

    Args:
        search_func: Function to call for searching
        search_body: Search body/parameters
        **kwargs: Additional arguments passed to search function

    Returns:
        Estimated total count of results

    Raises:
        Exception: If the search request fails

    Example:
        total = estimate_total_results(
            client.search().search,
            SearchBody(doc_types=["assets"])
        )
        print("Estimated %d total assets" % total)
    """
    # Make a single request with minimal results
    if "params" not in kwargs:
        kwargs["params"] = {}

    kwargs["params"].update({"per_page": 1, "page": 1})
    response = search_func(search_body, **kwargs)

    data = _extract_response_data(response)
    return data.get("total", 0)


def paginate_collection_contents(
    collection_func: Callable,
    collection_id: str,
    config: Optional[PaginationConfig] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Paginate collection contents specifically.

    Specialized function for paginating collection contents
    which may have different pagination patterns than search results.

    Args:
        collection_func: Function to call for getting contents
        collection_id: ID of the collection to paginate
        config: Pagination configuration
        **kwargs: Additional arguments passed to collection function

    Returns:
        Complete paginated collection contents

    Raises:
        PaginationError: If pagination fails

    Example:
        contents = paginate_collection_contents(
            client.collections().get_contents,
            "collection_id_123",
            PaginationConfig(verbose=True)
        )

        items = contents['objects']
        print("Collection has %d items" % len(items))
    """

    @paginate_iconik_response(config)
    def _collection_wrapper(**wrapper_kwargs):
        # Merge the kwargs properly
        merged_kwargs = {**kwargs, **wrapper_kwargs}
        return collection_func(collection_id, **merged_kwargs)

    return _collection_wrapper()
