from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel


class ViewMetadata(BaseModel):
    date_created: Optional[str] = None
    date_modified: Optional[str] = None
    metadata_values: Optional[Dict[str, Any]] = None
    object_id: Optional[str] = None
    object_type: Optional[str] = None
    version_id: Optional[str] = None
