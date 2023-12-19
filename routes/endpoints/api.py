from fastapi import APIRouter
from .collect_face.collect_face_api import router as collect_face

api_router = APIRouter(prefix="/v1")
api_router.include_router(collect_face, prefix="/collect_face", tags=["collect_face"])