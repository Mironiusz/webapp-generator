from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Response, status

from app.api.deps import SessionDep
from app.api.system.health import db_connection_check, db_schema_check
from app.api.system.schemas import (
    DatabaseStatus,
    GetDatabaseStatus,
    GetHealthStatus,
    GetReadinessStatus,
    SchemaStatus,
    ServiceStatus,
)

_UNAVAILABLE_RESPONSE: dict[int | str, dict[str, Any]] = {
    status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Backend nie jest gotowy do obsługi ruchu"},
}

SERVICE_STATUS_RESPONSE_CODE_MAP: dict[ServiceStatus, int] = {
    ServiceStatus.OK: status.HTTP_200_OK,
    ServiceStatus.DEGRADED: status.HTTP_503_SERVICE_UNAVAILABLE,
}

system_router = APIRouter(
    prefix="/health",
)


@system_router.get("")
async def get_health_status() -> GetHealthStatus:
    """Sprawdza, czy system odpowiada"""
    return GetHealthStatus(
        status=ServiceStatus.OK,
    )


@system_router.get("/db", responses=_UNAVAILABLE_RESPONSE)
async def get_db_status(
    session: SessionDep,
    response: Response,
) -> GetDatabaseStatus:
    """Sprawdza, czy baza danych odpowiada"""

    service_status = ServiceStatus.DEGRADED
    database_status = await db_connection_check(session)

    if database_status is DatabaseStatus.UP:
        service_status = ServiceStatus.OK

    response.status_code = SERVICE_STATUS_RESPONSE_CODE_MAP.get(service_status)

    return GetDatabaseStatus(
        status=service_status,
        database_status=database_status,
    )


@system_router.get("/ready", responses=_UNAVAILABLE_RESPONSE)
async def get_ready_status(
    session: SessionDep,
    response: Response,
) -> GetReadinessStatus:
    """Sprawdza, czy baza danych jest gotowa do działania i ma aktualną schemę"""

    service_status = ServiceStatus.DEGRADED
    database_status = await db_connection_check(session)
    schema_status = SchemaStatus.UNKNOWN

    if database_status is DatabaseStatus.UP:
        schema_status = await db_schema_check(session)

    if schema_status is SchemaStatus.READY:
        service_status = ServiceStatus.OK

    response.status_code = SERVICE_STATUS_RESPONSE_CODE_MAP.get(service_status)

    return GetReadinessStatus(
        status=service_status,
        database_status=database_status,
        schema_status=schema_status,
    )
