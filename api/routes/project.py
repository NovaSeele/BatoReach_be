# router.py

from datetime import datetime

from fastapi import APIRouter, Depends

from models.project import get_project_collection
from models.user import get_current_user
from schemas.project import ProjectCreate, ProjectInDB
from schemas.user import UserInDB

router = APIRouter()


@router.get("/idk")
async def read_root():
    return {"This is": "Project API"}


@router.post("/projects", response_model=ProjectInDB)
async def create_project(
        project: ProjectCreate,
        current_user: UserInDB = Depends(get_current_user),
):
    project_collection = await get_project_collection()

    # Prepare the new project document
    new_project = {
        "title": project.title,
        "description": project.description,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "owner_name": current_user.username
    }

    # Insert the new project into the MongoDB collection
    result = await project_collection.insert_one(new_project)
    # Add the generated MongoDB ObjectId to the project
    new_project["_id"] = result.inserted_id

    return new_project  # Return the project document with the inserted ID
