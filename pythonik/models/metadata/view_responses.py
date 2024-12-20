from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from pythonik.models.metadata.views import ViewField


class ViewResponse(BaseModel):
    """Response model for a view."""
    id: str
    name: str
    description: Optional[str] = None
    date_created: str
    date_modified: str
    view_fields: List[ViewField]
