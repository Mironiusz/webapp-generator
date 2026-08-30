from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.system.schemas import (
    DatabaseStatus,
    SchemaStatus,
)
from app.core.logger import get_logger

logger = get_logger(__name__)


async def db_connection_check(session: AsyncSession) -> DatabaseStatus:
    """Sprawdza stan połączenia z bazą danych"""
    try:
        await session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.error("Baza danych nie odpowiada")
        return DatabaseStatus.DOWN

    return DatabaseStatus.UP


async def db_schema_check(_session: AsyncSession) -> SchemaStatus:
    """Sprawdza stan schemy i migracji bazy danych"""
    return SchemaStatus.UNKNOWN
