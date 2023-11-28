from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Resolution(BaseModel):
    height: Optional[int]
    width: Optional[int]


class Proxy(BaseModel):
    asset_id: Optional[str] = None
    audio_bitrate: Optional[int] = None
    bit_rate: Optional[int] = None
    codec: Optional[str] = None
    filename: Optional[str] = None
    format: Optional[str] = None
    frame_rate: Optional[str] = None
    id: Optional[str] = None
    is_drop_frame: Optional[bool] = None
    is_public: Optional[bool] = None
    multipart_upload_url: Optional[str] = None
    name: Optional[str] = None
    resolution: Optional[Resolution] = None
    rotation: Optional[int] = None
    size: Optional[int] = None
    start_time_code: Optional[str] = None
    status: Optional[str] = None
    storage_id: Optional[str] = None
    storage_method: Optional[str] = None
    upload_credentials: Optional[Dict[str, Any]] = None
    upload_method: Optional[str] = None
    upload_url: Optional[str] = None
    url: Optional[str] = None
    version_id: Optional[str] = None


class Proxies(BaseModel):
    first_url: Optional[str] = None
    last_url: Optional[str] = None
    next_url: Optional[str] = None
    objects: Optional[List[Proxy]] = None
    page: Optional[int] = None
    pages: Optional[int] = None
    per_page: Optional[int] = None
    prev_url: Optional[str] = None
    scroll_id: Optional[str] = None
    total: Optional[int] = None
