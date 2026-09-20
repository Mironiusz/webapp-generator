from __future__ import annotations

from fastapi import APIRouter, status

from app.api.deps import SessionDep
from app.modules.users import service
from app.modules.users.schemas import UserCreate, UserRead, UsersRead

user_router = APIRouter(
    prefix="",
)


@user_router.get("/users")
async def read_users(session: SessionDep) -> UsersRead:
    """GET wszystkich użytkowników z bazy danych. Tymczasowo zostaje,
    by pomóc w debugowaniu - docelowa wersja tego nie będzie miała"""
    return UsersRead(users=await service.read_users(session))


@user_router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def create_user(session: SessionDep, user: UserCreate) -> UserRead:
    """POST użytkownika do bazy danych"""
    result = await service.create_user(session, user)

    return UserRead.model_validate(result)
