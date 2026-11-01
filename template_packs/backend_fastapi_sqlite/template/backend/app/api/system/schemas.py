from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel


class ServiceStatus(StrEnum):
    """Ogólny werdykt endpointu health."""

    OK = "ok"
    DEGRADED = "degraded"


class DatabaseStatus(StrEnum):
    """Stan połączenia z bazą danych."""

    UP = "up"
    DOWN = "down"


class SchemaStatus(StrEnum):
    """Stan schemy bazy danych."""

    READY = "ready"
    NOT_MIGRATED = "not_migrated"
    UNKNOWN = "unknown"


class GetHealthStatus(BaseModel):
    """Odpowiedź endpointu sprawdzającego dostępność serwisu."""

    status: ServiceStatus


class GetDatabaseStatus(BaseModel):
    """Odpowiedź endpointu sprawdzającego dostępność bazy danych."""

    status: ServiceStatus
    database_status: DatabaseStatus


class GetReadinessStatus(BaseModel):
    """Odpowiedź endpointu sprawdzającego poprawność schemy bazy danych."""

    status: ServiceStatus
    database_status: DatabaseStatus
    schema_status: SchemaStatus
