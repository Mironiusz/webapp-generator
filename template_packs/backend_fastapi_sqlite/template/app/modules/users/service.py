from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.modules.users.models import User

logger = get_logger(__name__)


async def read_users(session: AsyncSession) -> Sequence[User]:
    """Pobiera wszystkich użytkowników z bazy danych"""
    statement = select(User)
    result = await session.execute(statement)
    return result.scalars().all()
