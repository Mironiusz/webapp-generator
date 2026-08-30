from __future__ import annotations

from typing import TypedDict

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import DatabaseSettings


class LifespanState(TypedDict):
    db_session_factory: async_sessionmaker[AsyncSession]


def build_engine(database_settings: DatabaseSettings) -> AsyncEngine:
    return create_async_engine(
        url=database_settings.url,
        echo=database_settings.echo,
        pool_pre_ping=database_settings.pool_pre_ping,
    )


def build_orm_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
