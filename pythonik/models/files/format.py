from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Metadata(BaseModel):
    additionalProp1: Optional[str] = ""
    additionalProp2: Optional[str] = ""
    additionalProp3: Optional[str] = ""


class Component(BaseModel):
    id: Optional[str] = ""
    metadata: Optional[Metadata]
    name: Optional[str] = ""
    type: Optional[str] = ""


class Metadatum(BaseModel):
    additionalProp1: Optional[str] = ""
    additionalProp2: Optional[str] = ""
    additionalProp3: Optional[str] = ""


class Object(BaseModel):
    archive_status: Optional[str] = ""
    asset_id: Optional[str] = ""
    components: List[Component]
    date_deleted: Optional[str] = ""
    deleted_by_user: Optional[str] = ""
    id: Optional[str] = ""
    is_online: Optional[bool]
    metadata: List[Metadatum]
    name: Optional[str] = ""
    status: Optional[str] = ""
    storage_methods: List[str]
    user_id: Optional[str] = ""
    version_id: Optional[str] = ""
    warnings: Optional[List[str]]


class Format(BaseModel):
    first_url: Optional[str] = None
    last_url: Optional[str] = None
    next_url: Optional[str] = None
    objects: Optional[List[Object]] = None
    page: Optional[int] = None
    pages: Optional[int] = None
    per_page: Optional[int] = None
    prev_url: Optional[str] = None
    scroll_id: Optional[str] = None
    total: Optional[int] = None
