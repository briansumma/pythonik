from typing import (
    Any,
    Dict,
    Union,
)

from pythonik.models.base import Response
from pythonik.models.notifications import (
    WebhookCreateSchema,
    WebhookSchema,
    WebhooksSchema,
)
from pythonik.specs._internal_utils import is_pydantic_model
from pythonik.specs.base import Spec


class NotificationsSpec(Spec):
    server = "API/notifications/"

    def fetch_webhooks(self, **kwargs) -> Response:
        """
        Get all webhooks

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=WebhooksSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - default Error response
        """
        url = self.gen_url("webhooks/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, WebhooksSchema)

    def create_webhook(
        self,
        webhook: Union[WebhookCreateSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Create a new webhook

        Args:
            webhook: Webhook data (either as WebhookCreateSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=WebhookSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - default Error response
        """
        body = (webhook.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(webhook) else webhook)
        url = self.gen_url("webhooks/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, WebhookSchema)

    def get_webhook(self, webhook_id: str, **kwargs) -> Response:
        """
        Get a webhook definition

        Args:
            webhook_id: ID of the webhook
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=WebhookSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - default Error response
        """
        url = self.gen_url(f"webhooks/{webhook_id}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, WebhookSchema)

    def update_webhook(
        self,
        webhook_id: str,
        webhook: Union[WebhookCreateSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Update a webhook

        Args:
            webhook_id: ID of the webhook
            webhook: Webhook data (either as WebhookCreateSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=WebhookSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - default Error response
        """
        body = (webhook.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(webhook) else webhook)
        url = self.gen_url(f"webhooks/{webhook_id}/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, WebhookSchema)

    def delete_webhook(self, webhook_id: str, **kwargs) -> Response:
        """
        Delete a webhook

        Args:
            webhook_id: ID of the webhook
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - default Error response
        """
        url = self.gen_url(f"webhooks/{webhook_id}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)
