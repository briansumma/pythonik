from typing import (
    Any,
    Dict,
    Optional,
    Union,
)

from pythonik.models.base import Response
from pythonik.models.users_notifications import (
    NotificationSchema,
    NotificationSettingSchema,
    NotificationSettingsSchema,
    NotificationsSchema,
    SubscriptionSchema,
    SubscriptionsSchema,
    SystemNotificationSchema,
)
from pythonik.specs._internal_utils import is_pydantic_model
from pythonik.specs.base import Spec


class UsersNotificationsSpec(Spec):
    server = "API/users-notifications/"

    def fetch_notification_settings(
        self,
        per_page: int = 10,
        last_id: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        List of notification settings

        Args:
            per_page: The number of items for each page (default: 10)
            last_id: ID of a last file set on previous page
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=NotificationSettingsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Subscription does not exist
        """
        params: Dict[str, Any] = {
            "per_page": per_page,
        }
        if last_id:
            params["last_id"] = last_id

        url = self.gen_url("notification_settings/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, NotificationSettingsSchema)

    def get_notification_setting(
        self,
        object_type: str,
        sub_object_type: str,
        event_type: str,
        protocol: str,
        **kwargs,
    ) -> Response:
        """
        Returns a particular notification_setting by id

        Args:
            object_type: Type of the object
            sub_object_type: Type of the sub-object
            event_type: Type of the event
            protocol: Protocol used
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=NotificationSettingSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 NotificationSetting does not exist
        """
        url = self.gen_url(
            f"notification_settings/{object_type}/{sub_object_type}/"
            f"{event_type}/{protocol}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, NotificationSettingSchema)

    # pylint: disable=too-many-positional-arguments
    def update_notification_setting(
        self,
        object_type: str,
        sub_object_type: str,
        event_type: str,
        protocol: str,
        settings: Union[NotificationSettingSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Create a new notification_setting

        Args:
            object_type: Type of the object
            sub_object_type: Type of the sub-object
            event_type: Type of the event
            protocol: Protocol used
            settings: Notification setting (either as NotificationSettingSchema
                or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=NotificationSettingSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (settings.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(settings) else settings)
        url = self.gen_url(
            f"notification_settings/{object_type}/{sub_object_type}/"
            f"{event_type}/{protocol}/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, NotificationSettingSchema)

    def fetch_notifications(
        self,
        per_page: int = 10,
        last_id: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        Returns a list of notifications

        Args:
            per_page: The number of items for each page (default: 10)
            last_id: ID of a last file set on previous page
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=NotificationsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Notification does not exist
        """
        params: Dict[str, Any] = {
            "per_page": per_page,
        }
        if last_id:
            params["last_id"] = last_id

        url = self.gen_url("notifications/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, NotificationsSchema)

    def create_notification(
        self,
        notification: Union[NotificationSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Create a new notification

        Args:
            notification: Notification data (either as NotificationSchema
                or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=NotificationSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (notification.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(notification) else notification)
        url = self.gen_url("notifications/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, NotificationSchema)

    def mark_all_notifications_read(self, **kwargs) -> Response:
        """
        Update all notifications to read status

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        url = self.gen_url("notifications/all/read/")
        resp = self._put(url, **kwargs)
        return self.parse_response(resp, None)

    def create_system_notification(
        self,
        notification: Union[SystemNotificationSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Create a new system notification

        Args:
            notification: System notification data (either as
                SystemNotificationSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=NotificationSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (notification.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(notification) else notification)
        url = self.gen_url("notifications/system/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, NotificationSchema)

    def get_notification(
        self,
        notification_id: str,
        **kwargs,
    ) -> Response:
        """
        Returns a particular notification by id

        Args:
            notification_id: ID of the notification
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=NotificationSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Notification does not exist
        """
        url = self.gen_url(f"notifications/{notification_id}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, NotificationSchema)

    def delete_notification(
        self,
        notification_id: str,
        **kwargs,
    ) -> Response:
        """
        Delete a particular notification by id

        Args:
            notification_id: ID of the notification to delete
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Notification does not exist
        """
        url = self.gen_url(f"notifications/{notification_id}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def fetch_subscriptions(self, **kwargs) -> Response:
        """
        Returns all user subscriptions

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=SubscriptionSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Subscription does not exist
        """
        url = self.gen_url("subscriptions/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, SubscriptionSchema)

    def create_subscription(
        self,
        subscription: Union[SubscriptionSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Create a new subscription

        Args:
            subscription: Subscription data (either as SubscriptionSchema
                or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=SubscriptionSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (subscription.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(subscription) else subscription)
        url = self.gen_url("subscriptions/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, SubscriptionSchema)

    def get_subscription(
        self,
        subscription_id: str,
        **kwargs,
    ) -> Response:
        """
        Returns a particular subscription by id

        Args:
            subscription_id: ID of the subscription
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=SubscriptionSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Subscription does not exist
        """
        url = self.gen_url(f"subscriptions/{subscription_id}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, SubscriptionSchema)

    def delete_subscription(
        self,
        subscription_id: str,
        **kwargs,
    ) -> Response:
        """
        Delete a particular subscription by id

        Args:
            subscription_id: ID of the subscription to delete
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Subscription does not exist
        """
        url = self.gen_url(f"subscriptions/{subscription_id}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def fetch_object_subscriptions(
        self,
        object_type: str,
        object_id: str,
        **kwargs,
    ) -> Response:
        """
        Returns user subscriptions for a specific object_type and object_id

        Args:
            object_type: Type of the object
            object_id: ID of the object
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=SubscriptionsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Subscription does not exist
        """
        url = self.gen_url(f"{object_type}/{object_id}/subscriptions/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, SubscriptionsSchema)

    def delete_all_object_subscriptions(
        self,
        object_type: str,
        object_id: str,
        **kwargs,
    ) -> Response:
        """
        Delete all user subscriptions for a specific object_type and object_id

        Args:
            object_type: Type of the object
            object_id: ID of the object
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=SubscriptionSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Subscription does not exist
        """
        url = self.gen_url(f"{object_type}/{object_id}/subscriptions/all/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, SubscriptionSchema)
