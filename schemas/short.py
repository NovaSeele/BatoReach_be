from pydantic import BaseModel
from typing import List, Optional

class Short(BaseModel):
    url: Optional[str] = None
    video_type: Optional[str] = None
    video_id: Optional[str] = None
    music_name: Optional[str] = None
    shorts_duration: Optional[int] = None
    language: Optional[str] = None
    short_description: Optional[str] = None
    short_title: Optional[str] = None

class ShortInDB(BaseModel):
    url: Optional[str] = None
    video_type: Optional[str] = None
    video_id: Optional[str] = None
    music_name: Optional[str] = None
    shorts_duration: Optional[int] = None
    language: Optional[str] = None
    short_description: Optional[str] = None
    short_title: Optional[str] = None