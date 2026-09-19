from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserCreateResponse

logger = get_logger(__name__)


async def read_users(session: AsyncSession) -> Sequence[User]:
    """Pobiera wszystkich użytkowników z bazy danych"""
    statement = select(User)
    result = await session.execute(statement)
    return result.scalars().all()


async def create_user(session: AsyncSession, user: UserCreate) -> UserCreateResponse:
    try:
        statement = text("SELECT 1")
        await session.execute(statement)
    except SQLAlchemyError:
        logger.debug("Error")

    return UserCreateResponse(
        id=1,
        username=user.username,
        email=user.email,
    )
