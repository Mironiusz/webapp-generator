from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from alembic.config import Config
from alembic.script import ScriptDirectory
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import Lifespan

from app.api.errors import register_exception_handlers
from app.api.system.router import system_router
from app.api.v1.router import v1_router
from app.core.config import Settings, get_settings
from app.core.logger import configure_logging, get_logger
from app.db.session import LifespanState, build_engine, build_orm_session_factory

logger = get_logger(__name__)


def build_lifespan(settings: Settings) -> Lifespan[FastAPI]:
    """Buduje handler cyklu życia aplikacji"""

    @asynccontextmanager
    async def lifespan(_application: FastAPI) -> AsyncGenerator[LifespanState]:
        """Konfiguruje logowanie przy starcie aplikacji i domyka zasoby przy jej zatrzymaniu."""
        configure_logging()

        alembic_config = Config(toml_file=settings.database.alembic_config_path)
        alembic_current_head = ScriptDirectory.from_config(alembic_config).get_current_head()
        if alembic_current_head is None:
            raise RuntimeError("Alembic migration has 0 revisions")

        engine = build_engine(settings.database)
        db_session_factory = build_orm_session_factory(engine)

        logger.info("Start backendu w środowisku %s", settings.environment)

        try:
            yield {
                "db_session_factory": db_session_factory,
                "alembic_current_head": alembic_current_head,
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

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api.cors_origins,
        allow_credentials=False,
        allow_methods=settings.api.allow_methods,
        allow_headers=settings.api.allow_headers,
    )

    register_exception_handlers(application)

    return application


app = create_app(get_settings())
