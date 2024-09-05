from pydantic import BaseModel
from typing import Optional, Union
from fastapi import UploadFile


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
    # Store avatar as file path (str) or binary data (bytes)
    avatar: Optional[Union[str, bytes]] = None
