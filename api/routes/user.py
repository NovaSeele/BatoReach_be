# router.py
import os, shutil

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm

from schemas.user import User, UserInDB, Token, UserCreate
from models.user import authenticate_user, get_current_user, get_user_collection
from dependency.user import get_password_hash, create_access_token

router = APIRouter()

UPLOAD_DIR = "public/avatars/"

@router.post("/register", response_model=UserCreate)
async def register_user(user: UserCreate):
    user_collection = await get_user_collection()

    # Check if the user already existed
    existing_user = await user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)  # Use the password field
    user_in_db = UserInDB(**user.model_dump(), hashed_password=hashed_password)    
    
    # Insert the user into the database
    result = await user_collection.insert_one(user_in_db.model_dump())

    if result.inserted_id:
        return user
    raise HTTPException(status_code=400, detail="Registration failed")


@router.post("/upload-avatar", response_model=UserCreate)
async def upload_avatar(avatar: UploadFile = File(...), current_user: UserCreate = Depends(get_current_user)):
    user_collection = await get_user_collection()

    # Ensure the uploads directory exists
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
        

    # Save the avatar file
    avatar_filename = f"{current_user.username}_avatar.jpg"
    avatar_path = os.path.join(UPLOAD_DIR, avatar_filename)
    with open(avatar_path, "wb") as f:
        shutil.copyfileobj(avatar.file, f)

    # Update user's avatar in the database
    await user_collection.update_one(
        {"username": current_user.username}, {"$set": {"avatar": avatar_path}}
    )

    # Fetch updated user details
    updated_user = await user_collection.find_one({"username": current_user.username})
    
    return updated_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

