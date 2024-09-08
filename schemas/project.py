from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Project(BaseModel):
    title: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    owner_name: str


class ProjectCreate(Project):
    pass


class ProjectInDB(Project):
    pass
