from pydantic import BaseModel
from typing import List, Optional


class Languages(BaseModel):
    language: str
    subtitle_url: Optional[str] = None
    
class Video(BaseModel):
    video_id: str
    video_language: Optional[List[Languages]] = None

class VideoInYoutube(Video):
    pass
    video_type: str = "youtube"
    
class VideoNotInYoutube(Video):
    pass
    video_type: str = "not_youtube"
    video_url: Optional[str] = None