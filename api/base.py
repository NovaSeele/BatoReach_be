from fastapi import APIRouter
from .routes.user import router as user_router
from .routes.project import router as project_router
from .routes.video import router as video_router
from .routes.audio import router as audio_router

api_router = APIRouter()
# api_router.include_router(user_router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, tags=["user"])
api_router.include_router(project_router, tags=["project"])
api_router.include_router(video_router, tags=["video"])
api_router.include_router(audio_router, tags=["audio"])


