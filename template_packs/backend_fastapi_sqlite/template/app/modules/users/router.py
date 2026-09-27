from __future__ import annotations

from fastapi import APIRouter, status

from app.api.deps import SessionDep
from app.api.errors import InvalidRequestDataError, error_responses
from app.core.security import create_access_token
from app.modules.users import service
from app.modules.users.exceptions import InactiveUserError, InvalidCredentialsError, UserAlreadyExistsError
from app.modules.users.schemas import UserCreate, UserLogin, UserRead, UsersRead, UserTokenResponse

user_router = APIRouter(
    prefix="",
)


@user_router.get("/users")
async def read_users(session: SessionDep) -> UsersRead:
    """GET wszystkich użytkowników z bazy danych. Tymczasowo zostaje,
    by pomóc w debugowaniu - docelowa wersja tego nie będzie miała"""
    return UsersRead(users=await service.read_users(session))


@user_router.post(
    "/auth/register",
    status_code=status.HTTP_201_CREATED,
    responses=error_responses(
        InvalidRequestDataError,
        UserAlreadyExistsError,
    ),
)
async def create_user(session: SessionDep, user: UserCreate) -> UserRead:
    """POST użytkownika do bazy danych"""
    result = await service.create_user(session, user)

    return UserRead.model_validate(result)


@user_router.post(
    "/auth/login",
    status_code=status.HTTP_200_OK,
    responses=error_responses(
        InvalidCredentialsError,
        InactiveUserError,
        InvalidRequestDataError,
    ),
)
async def login_user(session: SessionDep, user: UserLogin) -> UserTokenResponse:
    result = await service.authenticate_user(session, user)
    token = create_access_token(str(result.id))

    return UserTokenResponse(access_token=token, token_type="bearer")
