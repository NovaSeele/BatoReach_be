from typing import Optional

from db.session import get_collection

from schemas.project import ProjectInDB

async def get_project_collection():
    project_collection = get_collection('projects')
    return project_collection

async def get_project_by_title(title: str) -> Optional[ProjectInDB]:
    project_collection = await get_project_collection()
    project_data = await project_collection.find_one({"title": title})
    if project_data:
        return ProjectInDB(**project_data)
    return None