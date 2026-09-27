from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.core.security import hash_password, verify_password
from app.modules.users.exceptions import InactiveUserError, InvalidCredentialsError, UserAlreadyExistsError
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserLogin

logger = get_logger(__name__)


async def create_user(session: AsyncSession, payload: UserCreate) -> User:
    """Tworzy użytkownika i zapisuje go do bazy danych"""

    user = User(
        username=payload.username,
        email=payload.email,
        pass_hash=hash_password(payload.password),
        is_active=True,
    )

    try:
        session.add(user)
        await session.commit()

    except IntegrityError as e:
        raise UserAlreadyExistsError() from e

    return user


async def authenticate_user(session: AsyncSession, payload: UserLogin) -> User:
    """Uwierzytelnia użytkownika"""
    statement = select(User).where(User.email == payload.email)
    logger.debug(statement)

    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    if user is None:
        raise InvalidCredentialsError

    is_verified = verify_password(payload.password, user.pass_hash)

    if not is_verified:
        raise InvalidCredentialsError

    if not user.is_active:
        raise InactiveUserError

    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    """Zwraca użytkownika o podanym id albo None, gdy takiego nie ma w bazie"""
    return await session.get(User, user_id)
