from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm

import cloudinary
import cloudinary.uploader
import cloudinary.utils

import httpx

from dependency.user import get_password_hash, create_access_token, verify_password
from models.project import get_project_collection
from models.user import authenticate_user, get_current_user, get_user_collection
from schemas.project import ProjectInDB
from schemas.user import User, UserInDB, Token, UserCreate, UserUpdateAvatar, UserChangePassword, UserAddYoutubeChannel, UserYoutubeChannelInfo

router = APIRouter()

# Configuration       
cloudinary.config( 
    cloud_name = "dxovnpypb", 
    api_key = "163478744136852", 
    api_secret = "sjuU6l-A4wTGCHxwcYZ5HecB0xg", # Click 'View API Keys' above to copy your API secret
    secure=True
)

YOUTUBE_API_KEY = "AIzaSyBFpSqujRWHa3z2nu73mwMFqCL01ib3KSI" 

UPLOAD_DIR = "public/avatars/"

@router.post("/upload-avatar", response_model=UserUpdateAvatar)
async def upload_avatar(avatar: UploadFile = File(...), current_user: UserInDB = Depends(get_current_user)):
    user_collection = await get_user_collection()

    # Upload the avatar file to Cloudinary
    upload_result = cloudinary.uploader.upload(avatar.file, public_id=f"{current_user.username}_avatar")

    # Get the URL of the uploaded avatar
    avatar_url = upload_result.get("secure_url")

    # Update user's avatar URL in the database
    await user_collection.update_one(
        {"username": current_user.username}, {"$set": {"avatar": avatar_url}}
    )

    # Fetch updated user details
    updated_user = await user_collection.find_one({"username": current_user.username})

    return updated_user


# Register a new user
@router.post("/register", response_model=UserCreate)
async def register_user(user: UserCreate):
    
    user_collection = await get_user_collection()
    
    # Check if the user already existed by username or email
    existing_user = await user_collection.find_one(
        {"$or": [{"username": user.username}, {"email": user.email}]})
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
        
    hashed_password = get_password_hash(user.password)  # Use the password field
    user_dict = user.model_dump()
    user_dict['hashed_password'] = hashed_password
    
    # Insert the user into the database
    result = await user_collection.insert_one(user_dict)
    
    if result.inserted_id:
        return user
    raise HTTPException(status_code=400, detail="Registration failed")
    

# Login and get an access token
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Attempt to authenticate user by username or email
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username, email, or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}



# Get the current user
@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# Get all the project and the project count that has owner_name as the current user (small route for update project
# info)
@router.get("/projects", response_model=List[ProjectInDB])
async def get_user_projects(current_user: UserInDB = Depends(get_current_user)):
    project_collection = await get_project_collection()
    projects = await project_collection.find({"owner_name": current_user.username}).to_list(length=100)
    return projects


@router.get("/projects/count", response_model=int)
async def get_user_project_count(current_user: UserInDB = Depends(get_current_user)):
    project_collection = await get_project_collection()
    project_count = await project_collection.count_documents({"owner_name": current_user.username})
    return project_count


# Update the user's project information using small route before
@router.get("/user/update_project", response_model=UserInDB)
async def update_user_project_info(current_user: UserInDB = Depends(get_current_user)):
    # get collection
    project_collection = await get_project_collection()
    user_collection = await get_user_collection()

    # get project count
    project_count = await project_collection.count_documents({"owner_name": current_user.username})
    # get projects
    projects = await project_collection.find({"owner_name": current_user.username}).to_list(length=100)

    # update data
    updated_data = {
        "number_of_projects": project_count,
        "projects": projects
    }

    # update the user's information in the database
    await user_collection.update_one(
        {"username": current_user.username},
        {"$set": updated_data}
    )

    # return the updated user info
    updated_user = await user_collection.find_one({"username": current_user.username})

    return updated_user


# Change the user's password
@router.put("/change-password", response_model=UserInDB)
async def change_password(
    user: UserChangePassword,
    current_user: UserInDB = Depends(get_current_user)
):
    user_collection = await get_user_collection()

    # If new password is the same as the old password
    if user.old_password == user.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the old password")

    # Check if the old password is correct
    if not user.old_password == current_user.password:
        raise HTTPException(
            status_code=400, detail="Old password is incorrect")

    # Generate new hashed password
    new_hashed_password = get_password_hash(user.new_password)

    # Cập nhật mật khẩu trong cơ sở dữ liệu
    await user_collection.update_one(
        {"username": current_user.username},
        {"$set": {
            "hashed_password": new_hashed_password,
            "password": user.new_password
        }}
    )

    # Fetch updated user information
    updated_user = await user_collection.find_one({"username": current_user.username})

    return updated_user


@router.post("/set_youtube_id", response_model=UserYoutubeChannelInfo)
async def set_youtube_id(
    youtube_channel_id: UserAddYoutubeChannel,
    current_user: UserInDB = Depends(get_current_user)
):
    user_collection = await get_user_collection()

    # Fetch YouTube channel info
    channel_url = (
        f"https://www.googleapis.com/youtube/v3/channels"
        f"?part=snippet,contentDetails&id={youtube_channel_id.youtube_channel_id}&key={YOUTUBE_API_KEY}"
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(channel_url)
            response.raise_for_status()

        data = response.json()
        if "items" not in data or len(data["items"]) == 0:
            raise HTTPException(status_code=404, detail="Channel not found")

        channel_item = data["items"][0]
        channel_name = channel_item["snippet"]["title"]
        uploads_playlist_id = channel_item["contentDetails"]["relatedPlaylists"]["uploads"]

        # Fetch playlists
        playlists_url = (
            f"https://www.googleapis.com/youtube/v3/playlists"
            f"?part=snippet&channelId={youtube_channel_id.youtube_channel_id}&key={YOUTUBE_API_KEY}"
        )

        async with httpx.AsyncClient() as client:
            response = await client.get(playlists_url)
            response.raise_for_status()

        playlists_data = response.json()
        playlist_ids = [item["id"] for item in playlists_data.get("items", [])]
        playlist_ids.append(uploads_playlist_id)  # Add uploads playlist ID

        # Update the user document with the new channel ID, name, and playlist IDs
        update_data = {
            "youtube_channel_id": youtube_channel_id.youtube_channel_id,
            "youtube_channel_name": channel_name,
            "play_list_id": playlist_ids
        }

        await user_collection.update_one(
            {"username": current_user.username},
            {"$set": update_data}
        )

        # Fetch the updated user data
        updated_user = await user_collection.find_one({"username": current_user.username})

        return UserYoutubeChannelInfo(
            youtube_channel_id=updated_user["youtube_channel_id"],
            youtube_channel_name=updated_user["youtube_channel_name"],
            play_list_id=updated_user["play_list_id"]
        )

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Error fetching YouTube data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



