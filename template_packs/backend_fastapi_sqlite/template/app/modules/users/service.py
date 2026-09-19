from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.core.security import hash_password
from app.modules.users.exceptions import UserAlreadyExistsError
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate

logger = get_logger(__name__)


async def read_users(session: AsyncSession) -> Sequence[User]:
    """Pobiera wszystkich użytkowników z bazy danych"""
    statement = select(User)
    result = await session.execute(statement)
    return result.scalars().all()


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
