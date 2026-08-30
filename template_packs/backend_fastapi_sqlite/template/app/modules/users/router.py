from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import SessionDep
from app.modules.users.schemas import UsersRead
from app.modules.users.service import read_users

user_router = APIRouter(prefix="/users")


@user_router.get("")
async def get_users(session: SessionDep) -> UsersRead:
    return UsersRead(users=await read_users(session))
