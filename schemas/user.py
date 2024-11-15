from pydantic import BaseModel
from typing import Optional, List
from schemas.project import ProjectInDB


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    avatar: Optional[str] = None
    youtube_channel_id: Optional[str] = None
    youtube_channel_name: Optional[str] = None
    play_list_id: Optional[List[str]] = None
    video_ids: Optional[List[str]] = None
    short_ids: Optional[List[str]] = None


class UserUpdateAvatar(User):
    avatar: Optional[str] = None    


class UserCreate(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    password: str


class UserInDB(User):
    password: str
    hashed_password: str
    avatar: Optional[str] = None
    number_of_projects: Optional[int] = int
    projects: Optional[List[ProjectInDB]] = []
    youtube_channel_id: Optional[str] = None
    youtube_channel_name: Optional[str] = None
    play_list_id: Optional[List[str]] = None
    video_ids: Optional[List[str]] = None
    short_ids: Optional[List[str]] = None


class UserChangePassword(BaseModel):
    old_password: str
    new_password: str


class UserAddYoutubeChannel(BaseModel):
    youtube_channel_id: str
    # play_list_id: Optional[List[str]] = None
    
    
class UserYoutubeChannelInfo(BaseModel):
    youtube_channel_id: str
    youtube_channel_name: str
    play_list_id: Optional[List[str]] = None
    



