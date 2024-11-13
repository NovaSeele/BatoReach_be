from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm

import cloudinary
import cloudinary.uploader
import cloudinary.utils

import httpx

from dependency.user import get_password_hash, create_access_token, verify_password
from models.project import get_project_collection
from models.user import authenticate_user, get_current_user, get_user_collection
from models.video import get_video_collection
from models.short import get_short_collection
from models.user import get_user_collection
from schemas.project import ProjectInDB
from schemas.user import User, UserInDB, Token, UserCreate, UserUpdateAvatar, UserChangePassword, UserAddYoutubeChannel, UserYoutubeChannelInfo
from schemas.video import VideoInDB, Video
from schemas.short import Short, ShortInDB

router = APIRouter()

@router.post("/shorts/", response_model=ShortInDB)
async def create_short(short: Short, username: Optional[str] = None):
    short_collection = await get_short_collection()
    
    db_short = ShortInDB(
        url=short.url,
        video_type=short.video_type,
        video_id=short.video_id,
        music_name=short.music_name,
        shorts_duration=short.shorts_duration,
    )

    if username:
        user_collection = await get_user_collection()
        user = await user_collection.find_one({"username": username})
        if user:
            if "short_ids" not in user:
                user["short_ids"] = []
            user["short_ids"].append(db_short.video_id)
            await user_collection.update_one({"username": username}, {"$set": user})
    
    result = await short_collection.insert_one(db_short.model_dump())
    if result.inserted_id:
        return db_short
    else:
        raise HTTPException(status_code=500, detail="Failed to create short")
    

@router.get("/shorts/{short_id}", response_model=List[ShortInDB])
async def get_shorts(short_id: str):
    short_collection = await get_short_collection()
    shorts = await short_collection.find({"video_id": short_id}).to_list(None)
    if not shorts:
        raise HTTPException(status_code=404, detail="No short found with this ID")
    return shorts

@router.get("/shorts/list/", response_model=List[ShortInDB])
async def get_shorts_list(short_ids: List[str] = Query(...)):
    short_collection = await get_short_collection()
    shorts = await short_collection.find({"video_id": {"$in": short_ids}}).to_list(None)
    if not shorts:
        raise HTTPException(status_code=404, detail="No shorts found with these IDs")
    return shorts


@router.get("/test/short", response_model=str)
async def test_short(
    url: str,
    video_type: str,
    video_id: str,
    music_name: str,
    shorts_duration: int,
):
    return "test OK"

