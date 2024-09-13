from pydantic import BaseModel
from typing import List, Optional


class Languages(BaseModel):
    language: str
    subtitle_url: Optional[str] = None

class VideoInYoutube(BaseModel):
    video_id: str
    video_language: Optional[str] = None
    video_title: Optional[str] = None
    video_voice: Optional[str] = None
    video_type: str = "youtube"
    video_url: Optional[str] = None

class VideoNotInYoutube(BaseModel):
    video_id: str
    video_language: Optional[str] = None
    video_title: Optional[str] = None
    video_voice: Optional[str] = None
    video_type: str = "not_youtube"
    video_url: Optional[str] = None

class VideoInDB(BaseModel):
    video_owner: str
    video_id: str
    video_title: Optional[str] = None
    video_language: Optional[str] = None
    video_voice: Optional[str] = None
    video_type: str
    video_url: Optional[str] = None
