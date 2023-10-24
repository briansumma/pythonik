from __future__ import annotations

from typing import Any, List, Optional, Dict

from pydantic import BaseModel


class Object(BaseModel):
    date_created: str
    date_modified: str
    description: str
    id: str
    metadata: Dict[str, Any]
    object_type: str
    title: str


class SearchResponse(BaseModel):
    facets: Optional[Dict[str, Any]] = None
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
