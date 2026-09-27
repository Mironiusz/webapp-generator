from __future__ import annotations

from fastapi import APIRouter, status

from app.api.deps import SessionDep
from app.api.errors import InvalidRequestDataError, error_responses
from app.core.security import create_access_token
from app.modules.users import service
from app.modules.users.deps import CurrentUserDep
from app.modules.users.exceptions import InactiveUserError, InvalidCredentialsError, NotAuthenticatedError, UserAlreadyExistsError
from app.modules.users.schemas import UserCreate, UserLogin, UserRead, UserTokenResponse

user_router = APIRouter(
    prefix="",
)


@user_router.post(
    "/auth/register",
    status_code=status.HTTP_201_CREATED,
    responses=error_responses(
        InvalidRequestDataError,
        UserAlreadyExistsError,
    ),
)
async def create_user(session: SessionDep, payload: UserCreate) -> UserRead:
    """Tworzy konto użytkownika"""
    result = await service.create_user(session, payload)

    return UserRead.model_validate(result)


@user_router.post(
    "/auth/login",
    responses=error_responses(
        InvalidCredentialsError,
        InactiveUserError,
        InvalidRequestDataError,
    ),
)
async def login_user(session: SessionDep, payload: UserLogin) -> UserTokenResponse:
    """Autentykuje użytkownika i nadaje mu token"""
    result = await service.authenticate_user(session, payload)
    token = create_access_token(str(result.id))

    return UserTokenResponse(access_token=token, token_type="bearer")


@user_router.get(
    "/auth/me",
    responses=error_responses(
        NotAuthenticatedError,
        InactiveUserError,
    ),
)
async def read_current_user(user: CurrentUserDep) -> UserRead:
    """Zwraca informacje o aktualnie zalogowanym użytkowniku"""
    return UserRead.model_validate(user)
