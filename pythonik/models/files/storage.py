from __future__ import annotations

from typing import Any, Dict, Optional, List

from pydantic import BaseModel


class Storage(BaseModel):
    default: Optional[bool] = None
    description: Optional[str] = None
    id: Optional[str] = None
    last_scanned: Optional[str] = None
    method: Optional[str] = None
    name: Optional[str] = None
    purpose: Optional[str] = None
    scanner_status: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    status_message: Optional[str] = None
    version: Optional[str] = None


class Storages(BaseModel):
    facets: Optional[Dict[str, Any]] = None
    first_url: Optional[str] = None
    last_url: Optional[str] = None
    next_url: Optional[str] = None
    objects: Optional[List[Storage]] = None
    page: Optional[int] = None
    pages: Optional[int] = None
    per_page: Optional[int] = None
    prev_url: Optional[str] = None
    scroll_id: Optional[str] = None
    total: Optional[int] = None
