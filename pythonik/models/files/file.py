from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class File(BaseModel):
    asset_id: Optional[str] = ""
    checksum: Optional[str] = ""
    date_created: Optional[str] = ""
    date_modified: Optional[str] = ""
    directory_path: Optional[str] = ""
    file_date_created: Optional[str] = ""
    file_date_modified: Optional[str] = ""
    file_set_id: Optional[str] = ""
    file_set_status: Optional[str] = ""
    format_id: Optional[str] = ""
    format_status: Optional[str] = ""
    id: Optional[str] = ""
    multipart_upload_url: Optional[str] = ""
    name: Optional[str] = ""
    original_name: Optional[str] = ""
    parent_id: Optional[str] = ""
    size: Optional[int] = ""
    status: Optional[str] = ""
    storage_id: Optional[str] = ""
    storage_method: Optional[str] = ""
    type: Optional[str] = ""
    upload_credentials: Optional[Dict[str, Any]] = {}
    upload_filename: Optional[str] = ""
    upload_method: Optional[str] = ""
    upload_url: Optional[str] = ""
    url: Optional[str] = ""
    user_id: Optional[str] = ""
    version_id: Optional[str] = ""


class Files(BaseModel):
    first_url: Optional[str] = None
    last_url: Optional[str] = None
    next_url: Optional[str] = None
    objects: Optional[List[File]] = None
    page: Optional[int] = None
    pages: Optional[int] = None
    per_page: Optional[int] = None
    prev_url: Optional[str] = None
    scroll_id: Optional[str] = None
    total: Optional[int] = None
