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
from models.audio import get_audio_collection
from models.user import get_user_collection
from schemas.project import ProjectInDB
from schemas.user import User, UserInDB, Token, UserCreate, UserUpdateAvatar, UserChangePassword, UserAddYoutubeChannel, UserYoutubeChannelInfo
from schemas.video import VideoInDB, Video
from schemas.audio import Audio, AudioInDB

router = APIRouter()

@router.post("/audios/", response_model=AudioInDB)
async def create_audio(audio: Audio, username: Optional[str] = None):
    audio_collection = await get_audio_collection()
    
    db_audio = AudioInDB(
        url=audio.url,
        video_type=audio.video_type,
        video_id=audio.video_id,
        music_name=audio.music_name,
        shorts_duration=audio.shorts_duration,
    )

    if username:
        user_collection = await get_user_collection()
        user = await user_collection.find_one({"username": username})
        if user:
            if "audio_ids" not in user:
                user["audio_ids"] = []
            user["audio_ids"].append(db_audio.video_id)
            await user_collection.update_one({"username": username}, {"$set": user})
    
    result = await audio_collection.insert_one(db_audio.model_dump())
    if result.inserted_id:
        return db_audio
    else:
        raise HTTPException(status_code=500, detail="Failed to create audio")


@router.get("/test/audio", response_model=str)
async def test_audio(
    url: str,
    video_type: str,
    video_id: str,
    music_name: str,
    shorts_duration: int,
):
    return "test OK"

