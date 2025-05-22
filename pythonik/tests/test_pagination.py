# pythonik/tests/test_pagination.py
"""
Unit tests for pagination utilities.

Tests cover pagination logic, error handling, retry mechanisms,
and date-based continuation for large datasets.
"""

from typing import (
    Any,
    Dict,
    List,
)
from unittest.mock import (
    Mock,
    patch,
)

import pytest
from pydantic import BaseModel

from pythonik.utils.pagination import (
    PaginationConfig,
    PaginationError,
    _calculate_delay,
    _extract_date_range,
    _extract_response_data,
    _merge_paginated_objects,
    _should_use_date_fallback,
    estimate_total_results,
    paginate_iconik_response,
    paginate_search_results,
)


class MockResponse(BaseModel):
    """Mock response for testing."""

    page: int = 1
    pages: int = 1
    per_page: int = 100
    total: int = 0
    objects: List[Dict[str, Any]] = []


class MockPythonikResponse:
    """Mock pythonik Response object."""

    def __init__(self, data: MockResponse):
        self.data = data


class TestPaginationConfig:
    """Test pagination configuration validation."""

    def test_default_config(self):
        """Test default configuration values."""
        config = PaginationConfig()

        assert config.max_per_page == 1000
        assert config.default_per_page == 100
        assert config.max_retries == 5
        assert config.retry_delay == 1.0
        assert config.retry_backoff == 2.0
        assert config.verbose is False
        assert config.date_fallback_enabled is True
        assert config.elasticsearch_limit == 10000

    def test_custom_config(self):
        """Test custom configuration values."""
        config = PaginationConfig(
            max_per_page=500,
            default_per_page=50,
            max_retries=3,
            verbose=True,
            elasticsearch_limit=5000,
        )

        assert config.max_per_page == 500
        assert config.default_per_page == 50
        assert config.max_retries == 3
        assert config.verbose is True
        assert config.elasticsearch_limit == 5000

    def test_config_validation(self):
        """Test configuration field validation."""
        with pytest.raises(ValueError):
            PaginationConfig(max_per_page=0)

        with pytest.raises(ValueError):
            PaginationConfig(max_per_page=1001)

        with pytest.raises(ValueError):
            PaginationConfig(max_retries=0)


class TestUtilityFunctions:
    """Test utility functions used by pagination."""

    def test_calculate_delay(self):
        """Test exponential backoff delay calculation."""
        assert _calculate_delay(1, 1.0, 2.0) == 1.0
        assert _calculate_delay(2, 1.0, 2.0) == 2.0
        assert _calculate_delay(3, 1.0, 2.0) == 4.0
        assert _calculate_delay(1, 2.0, 3.0) == 2.0
        assert _calculate_delay(2, 2.0, 3.0) == 6.0

    def test_merge_paginated_objects(self):
        """Test merging pagination responses."""
        base_data = {
            "objects": [{
                "id": "1"
            }, {
                "id": "2"
            }],
            "page": 1,
            "pages": 2,
            "total": 100,
        }

        new_data = {
            "objects": [{
                "id": "3"
            }, {
                "id": "4"
            }],
            "page": 2,
            "pages": 2,
            "total": 100,
        }

        merged = _merge_paginated_objects(base_data, new_data)

        assert len(merged["objects"]) == 4
        assert merged["objects"][0]["id"] == "1"
        assert merged["objects"][3]["id"] == "4"
        assert merged["page"] == 2
        assert merged["pages"] == 2
        assert merged["total"] == 100

    def test_merge_empty_objects(self):
        """Test merging with empty objects list."""
        base_data = {"objects": [{"id": "1"}]}
        new_data = {"objects": []}

        merged = _merge_paginated_objects(base_data, new_data)
        assert len(merged["objects"]) == 1

    def test_extract_date_range(self):
        """Test date range extraction for continuation."""
        objects = [
            {
                "date_created": "2023-01-01T10:00:00Z",
                "id": "1"
            },
            {
                "date_created": "2023-01-01T12:00:00Z",
                "id": "2"
            },
            {
                "date_created": "2023-01-01T08:00:00Z",
                "id": "3"
            },
        ]

        next_date = _extract_date_range(objects)
        assert next_date is not None
        assert "2023-01-01T12:00:01Z" == next_date

    def test_extract_date_range_empty(self):
        """Test date extraction with empty objects."""
        assert _extract_date_range([]) is None

    def test_extract_date_range_no_dates(self):
        """Test date extraction with objects missing dates."""
        objects = [{"id": "1"}, {"id": "2"}]
        assert _extract_date_range(objects) is None

    def test_extract_date_range_invalid_dates(self):
        """Test date extraction with invalid date formats."""
        objects = [
            {
                "date_created": "invalid-date",
                "id": "1"
            },
            {
                "date_created": None,
                "id": "2"
            },
        ]
        assert _extract_date_range(objects) is None

    def test_should_use_date_fallback(self):
        """Test date fallback decision logic."""
        config = PaginationConfig(elasticsearch_limit=1000,
                                  date_fallback_enabled=True)

        # Should use fallback when limit exceeded and more pages
        assert _should_use_date_fallback(1000, config, 5, 10) is True

        # Should not use when limit not exceeded
        assert _should_use_date_fallback(500, config, 5, 10) is False

        # Should not use when no more pages
        assert _should_use_date_fallback(1000, config, 10, 10) is False

        # Should not use when fallback disabled
        config.date_fallback_enabled = False
        assert _should_use_date_fallback(1000, config, 5, 10) is False


class TestResponseExtraction:
    """Test response data extraction from various formats."""

    def test_extract_pydantic_response(self):
        """Test extracting data from Pydantic model response."""
        mock_data = MockResponse(page=1, total=10, objects=[{"id": "1"}])
        mock_response = MockPythonikResponse(mock_data)

        data = _extract_response_data(mock_response)

        assert isinstance(data, dict)
        assert data["page"] == 1
        assert data["total"] == 10
        assert len(data["objects"]) == 1

    def test_extract_dict_response(self):
        """Test extracting data from direct dictionary."""
        response_dict = {
            "page": 1,
            "total": 5,
            "objects": [{
                "id": "1"
            }, {
                "id": "2"
            }],
        }

        data = _extract_response_data(response_dict)

        assert data == response_dict

    def test_extract_json_response(self):
        """Test extracting data from requests-like response."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "page": 2,
            "total": 20,
            "objects": [{
                "id": "3"
            }],
        }

        data = _extract_response_data(mock_response)

        assert data["page"] == 2
        assert data["total"] == 20

    def test_extract_unsupported_response(self):
        """Test handling unsupported response types."""
        with pytest.raises(PaginationError):
            _extract_response_data("unsupported")


class TestPaginationDecorator:
    """Test the pagination decorator functionality."""

    def test_single_page_response(self):
        """Test pagination with single page response."""
        mock_data = MockResponse(page=1,
                                 pages=1,
                                 total=2,
                                 objects=[{
                                     "id": "1"
                                 }, {
                                     "id": "2"
                                 }])

        @paginate_iconik_response()
        def mock_api_call(**kwargs):
            return MockPythonikResponse(mock_data)

        result = mock_api_call()

        assert result["page"] == 1
        assert result["pages"] == 1
        assert result["total"] == 2
        assert len(result["objects"]) == 2

    def test_multi_page_response(self):
        """Test pagination with multiple pages."""
        responses = [
            MockResponse(page=1,
                         pages=2,
                         total=4,
                         objects=[{
                             "id": "1"
                         }, {
                             "id": "2"
                         }]),
            MockResponse(page=2,
                         pages=2,
                         total=4,
                         objects=[{
                             "id": "3"
                         }, {
                             "id": "4"
                         }]),
        ]

        call_count = [0]  # Use list to allow modification in closure

        @paginate_iconik_response()
        def mock_api_call(**kwargs):
            if call_count[0] < len(responses):
                response = responses[call_count[0]]
                call_count[0] += 1
                return MockPythonikResponse(response)
            else:
                # Return empty response when no more pages
                return MockPythonikResponse(
                    MockResponse(page=3, pages=2, total=4, objects=[]))

        result = mock_api_call()

        assert result["total"] == 4
        assert len(result["objects"]) == 4
        assert result["objects"][0]["id"] == "1"
        assert result["objects"][3]["id"] == "4"
        assert call_count[0] == 2

    def test_pagination_with_retry(self):
        """Test pagination with retry on failure."""
        call_count = [0]  # Use list to allow modification in closure

        @paginate_iconik_response(PaginationConfig(max_retries=3))
        def mock_api_call(**kwargs):
            call_count[0] += 1

            if call_count[0] < 2:
                raise ConnectionError("Network error")

            return MockPythonikResponse(
                MockResponse(page=1, pages=1, total=1, objects=[{
                    "id": "1"
                }]))

        result = mock_api_call()

        assert call_count[0] == 2
        assert result["total"] == 1

    def test_pagination_max_retries_exceeded(self):
        """Test pagination when max retries exceeded."""

        @paginate_iconik_response(PaginationConfig(max_retries=2))
        def mock_api_call(**kwargs):
            raise ConnectionError("Persistent error")

        with pytest.raises(PaginationError) as exc_info:
            mock_api_call()

        assert "Failed to paginate after 2 attempts" in str(exc_info.value)

    @patch("time.sleep")
    def test_retry_delay(self, mock_sleep):
        """Test retry delay calculation."""
        call_count = [0]  # Use list to allow modification in closure

        @paginate_iconik_response(
            PaginationConfig(max_retries=3, retry_delay=1.0,
                             retry_backoff=2.0))
        def mock_api_call(**kwargs):
            call_count[0] += 1

            if call_count[0] < 3:
                raise ConnectionError("Network error")

            return MockPythonikResponse(
                MockResponse(page=1, pages=1, total=1, objects=[{
                    "id": "1"
                }]))

        mock_api_call()

        # Should have called sleep twice with exponential backoff
        assert mock_sleep.call_count == 2
        mock_sleep.assert_any_call(1.0)  # First retry
        mock_sleep.assert_any_call(2.0)  # Second retry


class TestDateBasedContinuation:
    """Test date-based continuation for large datasets."""

    def test_date_fallback_activation(self):
        """Test automatic switch to date-based pagination."""
        # Create mock responses that trigger date fallback
        base_objects = [{
            "id": f"{i}",
            "date_created": f"2023-01-01T{i:02d}:00:00Z"
        } for i in range(100)]

        responses = [
            MockResponse(page=1, pages=2, total=200,
                         objects=base_objects[:50]),
            MockResponse(page=2, pages=2, total=200,
                         objects=base_objects[50:]),
            # Date-based continuation response
            MockResponse(
                page=1,
                pages=1,
                total=50,
                objects=[{
                    "id": "101",
                    "date_created": "2023-01-02T00:00:00Z"
                }],
            ),
        ]

        call_count = [0]  # Use list to allow modification in closure

        @paginate_iconik_response(
            PaginationConfig(elasticsearch_limit=100,
                             date_fallback_enabled=True))
        def mock_api_call(**kwargs):
            if call_count[0] < len(responses):
                response = responses[call_count[0]]
                call_count[0] += 1
                return MockPythonikResponse(response)
            else:
                # Return empty response when no more data
                return MockPythonikResponse(
                    MockResponse(page=1, pages=1, total=0, objects=[]))

        result = mock_api_call()

        # Should have fetched all objects including date continuation
        assert len(result["objects"]) == 101
        assert call_count[0] == 3

    def test_date_fallback_disabled(self):
        """Test behavior when date fallback is disabled."""
        responses = [
            MockResponse(page=1,
                         pages=2,
                         total=200,
                         objects=[{
                             "id": "1"
                         }] * 50),
            MockResponse(page=2,
                         pages=2,
                         total=200,
                         objects=[{
                             "id": "2"
                         }] * 50),
        ]

        call_count = [0]  # Use list to allow modification in closure

        @paginate_iconik_response(
            PaginationConfig(elasticsearch_limit=100,
                             date_fallback_enabled=False))
        def mock_api_call(**kwargs):
            if call_count[0] < len(responses):
                response = responses[call_count[0]]
                call_count[0] += 1
                return MockPythonikResponse(response)
            else:
                # Return empty response when no more pages
                return MockPythonikResponse(
                    MockResponse(page=3, pages=2, total=200, objects=[]))

        result = mock_api_call()

        # Should stop at normal pagination limit
        assert len(result["objects"]) == 100
        assert call_count[0] == 2


class TestDirectPaginationFunctions:
    """Test direct pagination functions."""

    def test_paginate_search_results(self):
        """Test direct search result pagination."""

        def mock_search_func(search_body, **kwargs):
            return MockPythonikResponse(
                MockResponse(page=1,
                             pages=1,
                             total=2,
                             objects=[{
                                 "id": "1"
                             }, {
                                 "id": "2"
                             }]))

        result = paginate_search_results(mock_search_func, {"query": "test"},
                                         PaginationConfig(verbose=False))

        assert result["total"] == 2
        assert len(result["objects"]) == 2

    def test_estimate_total_results(self):
        """Test total result estimation."""

        def mock_search_func(search_body, **kwargs):
            return MockPythonikResponse(
                MockResponse(page=1,
                             pages=100,
                             total=10000,
                             objects=[{
                                 "id": "1"
                             }]))

        total = estimate_total_results(mock_search_func, {"query": "test"})

        assert total == 10000


class TestErrorHandling:
    """Test error handling scenarios."""

    def test_invalid_response_format(self):
        """Test handling of invalid response formats."""

        @paginate_iconik_response()
        def mock_api_call(**kwargs):
            return "invalid response format"

        with pytest.raises(PaginationError) as exc_info:
            mock_api_call()

        assert "Unsupported response type" in str(exc_info.value)

    def test_no_data_retrieved(self):
        """Test handling when no data is retrieved."""

        @paginate_iconik_response(PaginationConfig(max_retries=1))
        def mock_api_call(**kwargs):
            raise ValueError("API error")

        with pytest.raises(PaginationError) as exc_info:
            mock_api_call()

        assert "Failed to paginate after 1 attempts" in str(exc_info.value)


class TestIntegrationScenarios:
    """Test realistic integration scenarios."""

    def test_large_dataset_scenario(self):
        """Test handling of very large dataset with date continuation."""

        # Simulate 15,000 assets requiring date-based continuation
        def create_objects(start_id: int, count: int, base_date: str):
            return [{
                "id": str(start_id + i),
                "date_created": base_date,
                "title": f"Asset {start_id + i}",
            } for i in range(count)]

        responses = [
            # First 10k objects (hit ES limit)
            MockResponse(
                page=i,
                pages=10,
                total=10000,
                objects=create_objects(
                    (i - 1) * 1000, 1000, f"2023-01-01T{i:02d}:00:00Z"),
            ) for i in range(1, 11)
        ] + [
            # Date-based continuation for remaining 5k
            MockResponse(
                page=1,
                pages=5,
                total=5000,
                objects=create_objects(10000 + (i - 1) * 1000, 1000,
                                       f"2023-01-02T{i:02d}:00:00Z"),
            ) for i in range(1, 6)
        ]

        call_count = [0]  # Use list to allow modification in closure

        @paginate_iconik_response(
            PaginationConfig(
                elasticsearch_limit=10000,
                date_fallback_enabled=True,
                verbose=False,
            ))
        def mock_large_search(**kwargs):
            if call_count[0] < len(responses):
                response = responses[call_count[0]]
                call_count[0] += 1
                return MockPythonikResponse(response)

            # No more data
            return MockPythonikResponse(
                MockResponse(page=1, pages=1, total=0, objects=[]))

        result = mock_large_search()

        # Should retrieve all 15,000 objects
        assert len(result["objects"]) == 15000
        assert result["objects"][0]["id"] == "0"
        assert result["objects"][14999]["id"] == "14999"

    def test_collection_pagination_scenario(self):
        """Test realistic collection pagination scenario."""

        def mock_collection_func(collection_id, **kwargs):
            page = kwargs.get("params", {}).get("page", 1)
            objects_per_page = 100

            if page == 1:
                return MockPythonikResponse(
                    MockResponse(
                        page=1,
                        pages=3,
                        total=250,
                        objects=[{
                            "id": f"item_{i}",
                            "type": "asset"
                        } for i in range(objects_per_page)],
                    ))
            elif page == 2:
                return MockPythonikResponse(
                    MockResponse(
                        page=2,
                        pages=3,
                        total=250,
                        objects=[{
                            "id": f"item_{i}",
                            "type": "collection"
                        } for i in range(100, 200)],
                    ))
            else:  # page == 3
                return MockPythonikResponse(
                    MockResponse(
                        page=3,
                        pages=3,
                        total=250,
                        objects=[{
                            "id": f"item_{i}",
                            "type": "asset"
                        } for i in range(200, 250)],
                    ))

        from pythonik.utils.pagination import paginate_collection_contents

        result = paginate_collection_contents(
            mock_collection_func,
            "test_collection_123",
            PaginationConfig(verbose=False),
        )

        assert result["total"] == 250
        assert len(result["objects"]) == 250
        assert result["objects"][0]["id"] == "item_0"
        assert result["objects"][249]["id"] == "item_249"
