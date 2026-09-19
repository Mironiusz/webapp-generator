from __future__ import annotations

from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
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


async def db_connection_check(session: AsyncSession) -> DatabaseStatus:
    """Sprawdza stan połączenia z bazą danych"""
    try:
        await session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.error("Baza danych nie odpowiada")
        return DatabaseStatus.DOWN

    return DatabaseStatus.UP


async def db_schema_check(session: AsyncSession) -> SchemaStatus:
    """Sprawdza stan schemy i migracji bazy danych"""

    schema_status = SchemaStatus.UNKNOWN
    alembic_config = Config(toml_file="pyproject.toml")

    current_head = ScriptDirectory.from_config(alembic_config).get_current_head()

    def get_current_revision(session: Session) -> str:
        return MigrationContext.configure(session.connection()).get_current_revision()

    current_revision = await session.run_sync(get_current_revision)
    schema_status = SchemaStatus.READY if current_head == current_revision else SchemaStatus.NOT_MIGRATED

    return schema_status
