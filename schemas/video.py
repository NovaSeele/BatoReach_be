from pydantic import BaseModel
from typing import List, Optional


class Languages(BaseModel):
    language: str
    subtitle_url: Optional[str] = None

class Video(BaseModel):
    video_id: str
    video_language: Optional[str] = None
    video_title: Optional[str] = None
    video_voice: Optional[str] = None
    video_type: Optional[str] = None
    video_url: Optional[str] = None


class VideoInDB(BaseModel):
    video_owner: Optional[str] = None
    video_id: str
    video_title: Optional[str] = None
    video_language: Optional[str] = None
    video_voice: Optional[str] = None
    video_type: Optional[str] = None
    video_url: Optional[str] = None
