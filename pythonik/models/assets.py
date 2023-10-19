from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class CreatedByUserInfo(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    id: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[str] = None
    photo_big: Optional[str] = None
    photo_small: Optional[str] = None


class DeletedByUserInfo(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    id: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[str] = None
    photo_big: Optional[str] = None
    photo_small: Optional[str] = None


class UpdatedByUserInfo(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    id: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[str] = None
    photo_big: Optional[str] = None
    photo_small: Optional[str] = None


class Version(BaseModel):
    analyze_status: Optional[str] = None
    archive_status: Optional[str] = None
    created_by_user: Optional[str] = None
    created_by_user_info: Optional[CreatedByUserInfo] = None
    date_created: Optional[str] = None
    id: Optional[str] = None
    is_online: Optional[bool] = None
    status: Optional[str] = None
    transcribe_status: Optional[str] = None


class Asset(BaseModel):
    analyze_status: Optional[str] = None
    archive_status: Optional[str] = None
    category: Optional[str] = None
    created_by_user: Optional[str] = None
    created_by_user_info: Optional[CreatedByUserInfo] = None
    custom_keyframe: Optional[str] = None
    custom_poster: Optional[str] = None
    date_created: Optional[str] = None
    date_deleted: Optional[str] = None
    date_imported: Optional[str] = None
    date_modified: Optional[str] = None
    deleted_by_user: Optional[str] = None
    deleted_by_user_info: Optional[DeletedByUserInfo] = None
    external_id: Optional[str] = None
    external_link: Optional[str] = None
    favoured: Optional[bool] = None
    id: Optional[str] = None
    in_collections: Optional[List[str]] = None
    is_blocked: Optional[bool] = None
    is_online: Optional[bool] = None
    site_name: Optional[str] = None
    status: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None
    updated_by_user: Optional[str] = None
    updated_by_user_info: Optional[UpdatedByUserInfo] = None
    versions: Optional[List[Version]] = None
    warning: Optional[str] = None
