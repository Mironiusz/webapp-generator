from __future__ import annotations

from fastapi import APIRouter, Response, status

from app.api.deps import SessionDep
from app.modules.users import service
from app.modules.users.schemas import UserCreate, UserCreateResponse, UsersRead

user_router = APIRouter(
    prefix="/users",
)


@user_router.get("")
async def read_users(session: SessionDep) -> UsersRead:
    """GET wszystkich użytkowników z bazy danych"""
    return UsersRead(users=await service.read_users(session))


@user_router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def create_user(session: SessionDep, user: UserCreate, response: Response) -> UserCreateResponse:
    """POST użytkownika do bazy danych"""
    result = await service.create_user(session, user)
    response.status_code = status.HTTP_201_CREATED

    return result
