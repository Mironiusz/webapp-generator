from __future__ import annotations

import asyncio

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import get_settings
from app.core.logger import configure_logging
from app.db.registry import Base

configure_logging()

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Wypisuje migracje jako gotowy SQL, bez łączenia się z bazą danych"""
    context.configure(
        url=get_settings().database.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Wykonuje synchroniczne migracje na podanym połączeniu"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Otwiera asynchroniczne połączenie z bazą i przepuszcza przez nie synchroniczne migracje"""
    connectable = create_async_engine(
        url=get_settings().database.url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Wykonuje migracje na działającej bazie danych"""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
