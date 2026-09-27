from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api.deps import SessionDep
from app.core.logger import get_logger
from app.core.security import TokenValidationError, decode_access_token
from app.modules.users import service
from app.modules.users.exceptions import InactiveUserError, NotAuthenticatedError
from app.modules.users.models import User

logger = get_logger(__name__)

security = HTTPBearer()


async def get_current_user(session: SessionDep, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> User:
    """Przyjmuje dane z headera oraz sesję, zwraca poprawny obiekt User dla tych danych.
    Dzięki temu, jeśli kod endpointu używający tego dep wykonuje się, wiemy, że user jest poprawny"""
    try:
        sub = decode_access_token(credentials.credentials)
    except TokenValidationError as exc:
        raise NotAuthenticatedError from exc

    logger.debug("Token dla sub %s", sub)

    try:
        user_id = int(sub)
    except ValueError as exc:
        raise NotAuthenticatedError from exc

    user = await service.get_user_by_id(session, user_id)

    if user is None:
        raise NotAuthenticatedError

    if not user.is_active:
        raise InactiveUserError

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
