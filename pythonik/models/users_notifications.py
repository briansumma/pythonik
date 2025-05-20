"""
Iconik Users-notifications Models
This module contains Pydantic models for the Iconik Users-notifications API.
"""

from __future__ import annotations

from datetime import datetime
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
)


class SystemNotificationSchema(BaseModel):
    """Represents a SystemNotificationSchema in the Iconik system."""

    context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    date_created: Optional[datetime] = None
    date_modified: Optional[datetime] = None
    event_type: str
    exclude_users: Optional[List[str]] = Field(default_factory=list)
    id: Optional[str] = None
    message_long: str
    message_short: str
    object_id: Optional[str] = None
    object_type: str
    recipient_id: str
    sender_id: str
    share_id: Optional[str] = None
    share_user_id: Optional[str] = None
    status: Optional[Literal["QUEUED", "SENT", "READ"]] = None
    sub_object_id: Optional[str] = None
    sub_object_type: Optional[str] = None
    system_domain_id: str
    user_id: Optional[str] = None


class SubscriptionsSchema(BaseModel):
    """Represents a SubscriptionsSchema in the Iconik system."""

    first_url: Optional[str] = None
    last_url: Optional[str] = None
    next_url: Optional[str] = None
    objects: Optional[List["SubscriptionSchema"]] = Field(default_factory=list)
    page: Optional[int] = Field(None, ge=-2147483648, le=2147483647)
    pages: Optional[int] = Field(None, ge=-2147483648, le=2147483647)
    per_page: Optional[int] = Field(None, ge=-2147483648, le=2147483647)
    prev_url: Optional[str] = None
    total: Optional[int] = Field(None,
                                 ge=-9223372036854775808,
                                 le=9223372036854775807)


class SubscriptionSchema(BaseModel):
    """Represents a SubscriptionSchema in the Iconik system."""

    date_created: Optional[datetime] = None
    date_modified: Optional[datetime] = None
    event_type: Optional[str] = None
    id: Optional[str] = None
    object_id: Optional[str] = None
    object_type: str
    sub_object_id: Optional[str] = None
    sub_object_type: Optional[str] = None
    system_domain_id: Optional[str] = None
    user_id: Optional[str] = None


class NotificationsSchema(BaseModel):
    """Represents a NotificationsSchema in the Iconik system."""

    first_url: Optional[str] = None
    last_url: Optional[str] = None
    next_url: Optional[str] = None
    objects: Optional[List["NotificationSchema"]] = Field(default_factory=list)
    page: Optional[int] = Field(None, ge=-2147483648, le=2147483647)
    pages: Optional[int] = Field(None, ge=-2147483648, le=2147483647)
    per_page: Optional[int] = Field(None, ge=-2147483648, le=2147483647)
    prev_url: Optional[str] = None
    total: Optional[int] = Field(None,
                                 ge=-9223372036854775808,
                                 le=9223372036854775807)


class NotificationSettingsSchema(BaseModel):
    """Represents a NotificationSettingsSchema in the Iconik system."""

    first_url: Optional[str] = None
    last_url: Optional[str] = None
    next_url: Optional[str] = None
    objects: Optional[List["NotificationSettingSchema"]] = Field(
        default_factory=list)
    page: Optional[int] = Field(None, ge=-2147483648, le=2147483647)
    pages: Optional[int] = Field(None, ge=-2147483648, le=2147483647)
    per_page: Optional[int] = Field(None, ge=-2147483648, le=2147483647)
    prev_url: Optional[str] = None
    total: Optional[int] = Field(None,
                                 ge=-9223372036854775808,
                                 le=9223372036854775807)


class NotificationSettingSchema(BaseModel):
    """Represents a NotificationSettingSchema in the Iconik system."""

    enabled: bool
    event_type: str
    object_type: str
    protocol: Optional[str] = None
    recipient_id: str
    settings: Optional[Dict[str, Any]] = Field(default_factory=dict)
    sub_object_type: Optional[str] = None
    system_domain_id: Optional[str] = None


class NotificationSchema(BaseModel):
    """Represents a NotificationSchema in the Iconik system."""

    context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    date_created: Optional[datetime] = None
    date_modified: Optional[datetime] = None
    event_type: str
    exclude_users: Optional[List[str]] = Field(default_factory=list)
    id: Optional[str] = None
    message_long: str
    message_short: str
    object_id: str
    object_type: str
    recipient_id: str
    sender_id: str
    share_id: Optional[str] = None
    share_user_id: Optional[str] = None
    status: Optional[Literal["QUEUED", "SENT", "READ"]] = None
    sub_object_id: Optional[str] = None
    sub_object_type: Optional[str] = None
    system_domain_id: Optional[str] = None
    user_id: Optional[str] = None


class ListObjectsSchema(BaseModel):
    """Represents a ListObjectsSchema in the Iconik system."""

    first_url: Optional[str] = None
    last_url: Optional[str] = None
    next_url: Optional[str] = None
    page: Optional[int] = Field(None, ge=-2147483648, le=2147483647)
    pages: Optional[int] = Field(None, ge=-2147483648, le=2147483647)
    per_page: Optional[int] = Field(None, ge=-2147483648, le=2147483647)
    prev_url: Optional[str] = None
    total: Optional[int] = Field(None,
                                 ge=-9223372036854775808,
                                 le=9223372036854775807)


# Update forward references
SystemNotificationSchema.model_rebuild()
SubscriptionsSchema.model_rebuild()
SubscriptionSchema.model_rebuild()
NotificationsSchema.model_rebuild()
NotificationSettingsSchema.model_rebuild()
NotificationSettingSchema.model_rebuild()
NotificationSchema.model_rebuild()
ListObjectsSchema.model_rebuild()
