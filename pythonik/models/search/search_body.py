from __future__ import annotations

from typing import Any, List, Optional, Dict

from pydantic import BaseModel


class FacetsFilter(BaseModel):
    name: Optional[str] = ""
    value_in: Optional[List[str]] = []


class Range(BaseModel):
    max: Optional[str] = ""
    min: Optional[str] = ""
    timezone: Optional[str] = ""


class Term(BaseModel):
    exists: Optional[bool] = None
    missing: Optional[bool] = None
    name: Optional[str] = ""
    range: Optional[Range] = None
    value: Optional[str] = ""
    value_in: Optional[List[str]] = []


class Filter(BaseModel):
    filters: Optional[List[Any]] = None
    operator: Optional[str] = ""
    terms: Optional[List[Term]] = None


class SortItem(BaseModel):
    name: Optional[str] = ""
    order: Optional[str] = ""


class SearchBody(BaseModel):
    doc_types: Optional[List[str]] = None
    exclude_fields: Optional[List[str]] = None
    facets: Optional[List[str]] = None
    facets_filters: Optional[List[FacetsFilter]] = None
    filter: Optional[Filter] = Filter()
    include_fields: Optional[List[str]] = None
    metadata_view_id: Optional[str] = ""
    query: Optional[str] = ""
    search_after: Optional[List[Any]] = None
    search_fields: Optional[List[str]] = None
    sort: Optional[List[SortItem]] = None
