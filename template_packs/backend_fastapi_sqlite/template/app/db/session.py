from __future__ import annotations

from typing import TypedDict

from sqlalchemy import event
from sqlalchemy.engine.interfaces import DBAPIConnection
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import ConnectionPoolEntry

from app.core.config import DatabaseSettings


class LifespanState(TypedDict):
    db_session_factory: async_sessionmaker[AsyncSession]


def build_engine(database_settings: DatabaseSettings) -> AsyncEngine:
    engine = create_async_engine(
        url=database_settings.url,
        echo=database_settings.echo,
        pool_pre_ping=database_settings.pool_pre_ping,
    )

    @event.listens_for(engine.sync_engine, "connect")
    def _enable_foreign_keys(connection: DBAPIConnection, _record: ConnectionPoolEntry) -> None:
        """Funkcja włączająca egzekwowanie kluczy obcych"""
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


def build_orm_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
