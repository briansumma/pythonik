from __future__ import annotations

from typing import Any, List, Optional, Dict

from pydantic import BaseModel
from pythonik.models.files.keyframe import Keyframe

from pythonik.models.files.file import File
from pythonik.models.files.proxy import Proxy


class Object(BaseModel):
    date_created: Optional[str] = ""
    date_modified: Optional[str] = ""
    description: Optional[str] = ""
    id: Optional[str] = ""
    metadata: Dict[str, Any]
    object_type: Optional[str] = ""
    title: Optional[str] = ""
    files: Optional[List[File]] = []
    proxies: Optional[List[Proxy]] = []
    keyframes: Optional[List[Keyframe]] = []


class SearchResponse(BaseModel):
    facets: Optional[Dict[str, Any]] = ""
    first_url: Optional[str] = ""
    last_url: Optional[str] = ""
    next_url: Optional[str] = ""
    objects: Optional[List[Object]] = ""
    page: Optional[int] = None
    pages: Optional[int] = None
    per_page: Optional[int] = None
    prev_url: Optional[str] = ""
    scroll_id: Optional[str] = ""
    total: Optional[int] = ""
