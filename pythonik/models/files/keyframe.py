from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Resolution(BaseModel):
    height: Optional[int] = None
    width: Optional[int] = None


class TimeBase(BaseModel):
    denominator: Optional[int] = None
    numerator: Optional[int] = None


class TimeCode(BaseModel):
    frames_number: Optional[int] = None
    is_drop_frame: Optional[bool] = None
    time_base: Optional[TimeBase] = {}


class Keyframe(BaseModel):
    asset_id: Optional[str] = ""
    collection_id: Optional[str] = ""
    filename: Optional[str] = ""
    format: Optional[str] = ""
    id: Optional[str] = ""
    is_custom_keyframe: Optional[bool] = None
    is_public: Optional[bool] = None
    name: Optional[str] = ""
    resolution: Optional[Resolution] = {}
    rotation: Optional[int] = None
    size: Optional[int] = None
    status: Optional[str] = ""
    storage_id: Optional[str] = ""
    storage_method: Optional[str] = ""
    time_code: Optional[TimeCode] = {}
    type: Optional[str] = ""
    upload_credentials: Optional[Dict[str, Any]] = {}
    upload_method: Optional[str] = ""
    upload_url: Optional[str] = ""
    url: Optional[str] = ""
    version_id: Optional[str] = ""


class Keyframes(BaseModel):
    first_url: Optional[str] = ""
    last_url: Optional[str] = ""
    next_url: Optional[str] = ""
    objects: Optional[List[Keyframe]] = []
    page: Optional[int] = None
    pages: Optional[int] = None
    per_page: Optional[int] = None
    prev_url: Optional[str] = ""
    scroll_id: Optional[str] = ""
    total: Optional[int] = ""
