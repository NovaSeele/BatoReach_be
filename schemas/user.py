from pydantic import BaseModel
from typing import Optional, Union, List
from fastapi import UploadFile
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


class UserAvatar(User):
    avatar: str  # This can be the file path or URL of the stored image


class UserCreate(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    password: str
    avatar: Optional[str] = None


class UserInDB(User):
    password: str
    hashed_password: str
    avatar: Optional[Union[str, bytes]] = None
    number_of_projects: Optional[int] = int
    projects: Optional[List[ProjectInDB]] = []
