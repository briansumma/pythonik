from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Point(BaseModel):
    x: Optional[int] = None
    y: Optional[int] = None


class Primitive(BaseModel):
    color: Optional[str] = None
    points: List[Point] = None
    text: Optional[str] = None
    type: Optional[str] = None


class Drawing(BaseModel):
    primitives: List[Primitive] = None


class Word(BaseModel):
    end_ms: Optional[int] = None
    score: Optional[int] = None
    start_ms: Optional[int] = None
    value: Optional[str] = None


class Transcription(BaseModel):
    speaker: Optional[int] = None
    words: List[Word] = None


class SegmentBody(BaseModel):
    drawing: Optional[Drawing] = None
    external_id: Optional[str] = None
    keyframe_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    metadata_view_id: Optional[str] = None
    parent_id: Optional[str] = None
    path: Optional[str] = None
    segment_checked: Optional[bool] = None
    segment_color: Optional[str] = None
    segment_text: Optional[str] = None
    segment_track: Optional[str] = None
    segment_type: Optional[str] = None
    share_user_email: Optional[str] = None
    status: Optional[str] = None
    time_end_åmilliseconds: Optional[int] = None
    time_start_milliseconds: Optional[int] = None
    top_level: Optional[bool] = None
    transcription: Optional[Transcription] = None
    transcription_id: Optional[str] = None
    user_id: Optional[str] = None
    user_info: Optional[Dict[str, Any]] = None
    version_id: Optional[str] = None


class SegmentResponse(SegmentBody):
    pass
