from __future__ import annotations

from alembic.runtime.migration import MigrationContext
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.api.system.schemas import (
    DatabaseStatus,
    SchemaStatus,
)
from app.core.logger import get_logger

logger = get_logger(__name__)


def _read_current_revision(session: Session) -> str | None:
    return MigrationContext.configure(session.connection()).get_current_revision()


async def db_connection_check(session: AsyncSession) -> DatabaseStatus:
    """Sprawdza stan połączenia z bazą danych"""
    try:
        await session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.error("Baza danych nie odpowiada")
        return DatabaseStatus.DOWN

    return DatabaseStatus.UP


async def db_schema_check(session: AsyncSession, alembic_current_head: str) -> SchemaStatus:
    """Sprawdza stan schemy i migracji bazy danych"""

    current_revision = await session.run_sync(_read_current_revision)
    return SchemaStatus.READY if alembic_current_head == current_revision else SchemaStatus.NOT_MIGRATED
