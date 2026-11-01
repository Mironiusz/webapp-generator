from fastapi import APIRouter

from template_packs.backend_fastapi_sqlite.template.backend.app.modules.users.router import user_router

v1_router = APIRouter(
    prefix="/api/v1",
)

v1_router.include_router(user_router)
