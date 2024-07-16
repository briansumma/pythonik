from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel

from pythonik.models.base import ArchiveStatus, Status, UserInfo


class AnalyzeStatus(str, Enum):
    N_A = "N/A"
    REQUESTED = "REQUESTED"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    DONE = "DONE"


class AssetType(str, Enum):
    ASSET = "ASSET"
    SEQUENCE = "SEQUENCE"
    NLE_PROJECT = "NLE_PROJECT"
    PLACEHOLDER = "PLACEHOLDER"
    CUSTOM = "CUSTOM"
    LINK = "LINK"
    SUBCLIP = "SUBCLIP"


class CreatedByUserInfo(UserInfo):
    pass


class DeletedByUserInfo(UserInfo):
    pass


class UpdatedByUserInfo(UserInfo):
    pass


class Version(BaseModel):
    analyze_status: Optional[str] = ""
    archive_status: Optional[str] = ""
    created_by_user: Optional[str] = ""
    created_by_user_info: Optional[CreatedByUserInfo] = None
    date_created: Optional[str] = ""
    id: Optional[str] = ""
    is_online: Optional[bool] = None
    status: Optional[str] = ""
    transcribe_status: Optional[str] = ""


class Asset(BaseModel):
    analyze_status: Optional[AnalyzeStatus] = None
    archive_status: Optional[ArchiveStatus] = None
    category: Optional[str] = ""
    created_by_user: Optional[str] = ""
    created_by_user_info: Optional[CreatedByUserInfo] = None
    custom_keyframe: Optional[str] = ""
    custom_poster: Optional[str] = ""
    date_created: Optional[str] = ""
    date_deleted: Optional[str] = ""
    date_imported: Optional[str] = ""
    date_modified: Optional[str] = ""
    deleted_by_user: Optional[str] = ""
    deleted_by_user_info: Optional[DeletedByUserInfo] = None
    external_id: Optional[str] = ""
    external_link: Optional[str] = ""
    favoured: Optional[bool] = None
    id: Optional[str] = ""
    in_collections: Optional[List[str]] = []
    is_blocked: Optional[bool] = None
    is_online: Optional[bool] = None
    site_name: Optional[str] = ""
    status: Optional[Status] = Status.ACTIVE
    title: Optional[str] = ""
    type: Optional[AssetType] = AssetType.ASSET
    updated_by_user: Optional[str] = ""
    updated_by_user_info: Optional[UpdatedByUserInfo] = None
    versions: Optional[List[Version]] = []
    warning: Optional[str] = ""


class AssetCreate(Asset):
    title: str
    external_id: Union[str, None] = ""
    type: AssetType = AssetType.ASSET
    status: str = Status.ACTIVE
    analyze_status: str = AnalyzeStatus.N_A
    archive_status: str = ArchiveStatus.NOT_ARCHIVED
    is_online: bool = True
    is_blocked: bool = False
