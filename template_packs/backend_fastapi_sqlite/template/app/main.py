from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.types import Lifespan

from app.api.system.router import system_router
from app.api.v1.router import v1_router
from app.core.config import Settings, get_settings
from app.core.logger import configure_logging, get_logger
from app.db.session import LifespanState, build_engine, build_orm_session_factory

logger = get_logger(__name__)


def build_lifespan(settings: Settings) -> Lifespan[FastAPI]:
    """Buduje handler cyklu życia aplikacji"""

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncGenerator[LifespanState]:
        """Konfiguruje logowanie przy starcie aplikacji i domyka zasoby przy jej zatrzymaniu."""
        configure_logging()
        engine = build_engine(settings.database)
        db_session_factory = build_orm_session_factory(engine)
        logger.info("Start backendu w środowisku %s", settings.environment)

        try:
            yield {
                "db_session_factory": db_session_factory,
            }
        finally:
            await engine.dispose()
            logger.info("Backend finished working")

    return lifespan


def create_app(settings: Settings) -> FastAPI:
    """Buduje instancję FastAPI na podstawie przekazanych ustawień"""
    application = FastAPI(
        title=settings.api.title,
        version=settings.api.version,
        root_path=settings.api.root_path,
        openapi_url="/openapi.json" if settings.api.docs_enabled else None,
        lifespan=build_lifespan(settings),
    )

    application.state.settings = settings
    application.include_router(v1_router)
    application.include_router(system_router)

    return application


app = create_app(get_settings())
