from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
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
async def create_video(
    video: Video,
    current_user: UserInDB = Depends(get_current_user)
):
    video_collection = await get_video_collection()
    # existing_video = await video_collection.find_one({"video_id": video.video_id})

    # if existing_video:
    #     raise HTTPException(status_code=400, detail="Video with this ID or URL already exists")

    db_video = VideoInDB(
        video_owner=current_user.username,
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

# @router.post("/videos/add-language", response_model=VideoInDB)
# async def add_language_to_video(
#     video_id: str,
#     video_url: str,
#     new_language: Languages,
#     current_user: UserInDB = Depends(get_current_user)
# ):
#     video_collection = await get_video_collection()
#     existing_video = await video_collection.find_one({"$or": [{"video_id": video_id}, {"video_url": video_url}]})

#     if not existing_video:
#         raise HTTPException(status_code=404, detail="Video not found")

#     existing_languages = set(lang["language"] for lang in existing_video["video_language"])
#     if new_language.language in existing_languages:
#         raise HTTPException(status_code=400, detail="Language already exists for this video")

#     update_result = await video_collection.update_one(
#         {"_id": existing_video["_id"]},
#         {"$push": {"video_language": new_language.model_dump()}}
#     )
#     if update_result.modified_count:
#         updated_video = await video_collection.find_one({"_id": existing_video["_id"]})
#         return VideoInDB(**updated_video)
#     else:
#         raise HTTPException(status_code=500, detail="Failed to add new language to video")


# @router.post("/videos/not-youtube", response_model=VideoInDB)
# async def create_non_youtube_video(
#     video: VideoInYoutube,
#     current_user: UserInDB = Depends(get_current_user)
# ):
#     video_collection = await get_video_collection()
#     # existing_video = await video_collection.find_one({"video_id": video.video_id})

#     # if existing_video:
#     # raise HTTPException(status_code=400, detail="Video with this ID or URL already exists")

#     db_video = VideoInDB(
#         video_owner=current_user.username,
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
#         raise HTTPException(status_code=500, detail="Failed to create YouTube video")
