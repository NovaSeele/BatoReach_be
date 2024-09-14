from pydantic import BaseModel
from typing import List, Optional

class Audio(BaseModel):
    url: Optional[str] = None
    video_type: Optional[str] = None
    video_id: Optional[str] = None
    music_name: Optional[str] = None
    shorts_duration: Optional[int] = None
