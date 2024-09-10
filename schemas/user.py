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
    

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str


class UserAddYoutubeChannel(BaseModel):
    youtube_channel_id: str