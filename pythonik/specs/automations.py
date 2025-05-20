from typing import (
    Any,
    Dict,
    Optional,
    Union,
)

from pythonik.models.automations import (
    AutomationHistorySchema,
    AutomationRunEstimateSchema,
    AutomationSchema,
    AutomationsSchema,
    AutomationStatsSchema,
)
from pythonik.models.base import Response
from pythonik.specs._internal_utils import is_pydantic_model
from pythonik.specs.base import Spec


class AutomationsSpec(Spec):
    server = "API/automations/"

    def fetch_automations(
        self,
        page: int = 1,
        per_page: int = 10,
        **kwargs,
    ) -> Response:
        """
        List of automations

        Args:
            page: Which page number to fetch (default: 1)
            per_page: The number of items for each page (default: 10)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=AutomationsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        params = {
            "page": page,
            "per_page": per_page,
        }
        url = self.gen_url("")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, AutomationsSchema)

    def create_automation(
        self,
        automation: Union[AutomationSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Create a new automation

        Args:
            automation: Automation data (either as AutomationSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=AutomationSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (automation.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(automation) else automation)
        url = self.gen_url("")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, AutomationSchema)

    def fetch_automations_stats(self, **kwargs) -> Response:
        """
        Return statistics for automations associated with the system domain

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=AutomationStatsSchema)

        Raises:
            - 401 Token is invalid
        """
        url = self.gen_url("stats/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, AutomationStatsSchema)

    def get_automation(self, automation_id: str, **kwargs) -> Response:
        """
        Returns a particular automation by id

        Args:
            automation_id: ID of the automation
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=AutomationSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        url = self.gen_url(f"{automation_id}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, AutomationSchema)

    def update_automation(
        self,
        automation_id: str,
        automation: Union[AutomationSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Update automation

        Args:
            automation_id: ID of the automation
            automation: Automation data (either as AutomationSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=AutomationSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (automation.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(automation) else automation)
        url = self.gen_url(f"{automation_id}/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, AutomationSchema)

    def partial_update_automation(
        self,
        automation_id: str,
        automation: Union[AutomationSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Update automation

        Args:
            automation_id: ID of the automation
            automation: Automation data to update (either as AutomationSchema
                or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=AutomationSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (automation.model_dump(exclude_defaults=exclude_defaults,
                                      exclude_unset=True)
                if is_pydantic_model(automation) else automation)
        url = self.gen_url(f"{automation_id}/")
        resp = self._patch(url, json=body, **kwargs)
        return self.parse_response(resp, AutomationSchema)

    def delete_automation(self, automation_id: str, **kwargs) -> Response:
        """
        Delete a particular automation by id

        Args:
            automation_id: ID of the automation to delete
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        url = self.gen_url(f"{automation_id}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def create_automation_history(
        self,
        automation_id: str,
        history: Union[AutomationHistorySchema, Dict[str, Any]],
        ttl: Optional[int] = None,
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Create a new history entity

        Args:
            automation_id: ID of the automation
            history: History data (either as AutomationHistorySchema or dict)
            ttl: Time to live for the history entry in seconds
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=AutomationHistorySchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        params = {}
        if ttl is not None:
            params["ttl"] = ttl

        body = (history.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(history) else history)
        url = self.gen_url(f"{automation_id}/history/")
        resp = self._post(url, params=params, json=body, **kwargs)
        return self.parse_response(resp, AutomationHistorySchema)

    def get_automation_history(
        self,
        automation_id: str,
        object_type: str,
        object_id: str,
        version_id: str,
        **kwargs,
    ) -> Response:
        """
        Returns a particular history entity by id

        Args:
            automation_id: ID of the automation
            object_type: Type of the object
            object_id: ID of the object
            version_id: ID of the version
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=AutomationHistorySchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        url = self.gen_url(
            f"{automation_id}/history/{object_type}/{object_id}/{version_id}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, AutomationHistorySchema)

    def delete_automation_history(
        self,
        automation_id: str,
        object_type: str,
        object_id: str,
        version_id: str,
        **kwargs,
    ) -> Response:
        """
        Delete history event

        Args:
            automation_id: ID of the automation
            object_type: Type of the object
            object_id: ID of the object
            version_id: ID of the version
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 History entity not found
        """
        url = self.gen_url(
            f"{automation_id}/history/{object_type}/{object_id}/{version_id}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def run_automation(self, automation_id: str, **kwargs) -> Response:
        """
        Run an automation for existing objects

        Args:
            automation_id: ID of the automation
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        url = self.gen_url(f"{automation_id}/runs/")
        resp = self._post(url, **kwargs)
        return self.parse_response(resp, None)

    def get_automation_runs_estimate(
        self,
        automation_id: str,
        **kwargs,
    ) -> Response:
        """
        Get estimated number objects that might be affected by an automation run

        Args:
            automation_id: ID of the automation
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=AutomationRunEstimateSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        url = self.gen_url(f"{automation_id}/runs/estimate/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, AutomationRunEstimateSchema)
