from fastapi import APIRouter

from app.modules.users.router import user_router

v1_router = APIRouter(
    prefix="/api/v1",
    responses={404: {"description": "Not found"}},
)

v1_router.include_router(user_router)
