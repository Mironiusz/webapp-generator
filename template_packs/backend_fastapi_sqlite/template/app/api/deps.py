from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger

logger = get_logger(__name__)


async def get_session(request: Request) -> AsyncGenerator[AsyncSession]:
    """Tworzy czystą sesję na czas requestu i zamyka ją po odpowiedzi"""
    db_session_factory = request.state.db_session_factory
    async with db_session_factory() as session:
        logger.debug("Start sesji")

        try:
            yield session
        finally:
            logger.debug("Sesja zakończyła się")


SessionDep = Annotated[AsyncSession, Depends(get_session)]
