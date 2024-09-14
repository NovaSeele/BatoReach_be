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
from schemas.project import ProjectInDB
from schemas.user import User, UserInDB, Token, UserCreate, UserUpdateAvatar, UserChangePassword, UserAddYoutubeChannel, UserYoutubeChannelInfo
from schemas.video import VideoInDB, Video

router = APIRouter()


@router.post("/videos/", response_model=VideoInDB)
async def create_video(video: Video):
    video_collection = await get_video_collection()

    db_video = VideoInDB(
        video_id=video.video_id,
        video_title=video.video_title,
        video_voice=video.video_voice,
        video_language=video.video_language,
        video_type=video.video_type,
        video_url=video.video_url
    )
    result = await video_collection.insert_one(db_video.model_dump())
    if result.inserted_id:
        return db_video
    else:
        raise HTTPException(status_code=500, detail="Failed to create YouTube video")

# @router.post("/videos_no_auth/", response_model=VideoInDB)
# async def create_video_no_auth(video: Video):
#     video_collection = await get_video_collection()

#     db_video = VideoInDB(
#         video_owner="guest",
#         video_id=video.video_id,
#         video_title=video.video_title,
#         video_voice=video.video_voice,
#         video_language=video.video_language,
#         video_type=video.video_type,
#         video_url=video.video_url
#     )
#     result = await video_collection.insert_one(db_video.model_dump())
#     if result.inserted_id:
#         return db_video
#     else:
#         raise HTTPException(status_code=500, detail="Failed to create video")
    
    
# Return all videos that have the same video_id
@router.get("/videos/{video_id}", response_model=List[VideoInDB])
async def get_videos(video_id: str):
    video_collection = await get_video_collection()
    videos = await video_collection.find({"video_id": video_id}).to_list(None)
    if not videos:
        raise HTTPException(status_code=404, detail="No videos found with this ID")
    return videos

# # Return all languages that have the same video_id
# @router.get("/videos/{video_id}/languages", response_model=List[str])
# async def get_video_languages(video_id: str):
#     video_collection = await get_video_collection()
#     videos = await video_collection.find({"video_id": video_id}).to_list(None)
    
#     if not videos:
#         raise HTTPException(status_code=404, detail="No videos found with this ID")
    
#     languages = list(set(video["video_language"] for video in videos))
#     return languages


# actually this is a test for the video translation, return should be a video url after translation
@router.get("/test/video", response_model=str)
async def test_video(
    url: str,
    language: str,
    video_type: str,
    use_captions: str,
    voice_name: str,
    video_id: str
):
    return "test OK"





