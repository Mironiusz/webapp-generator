from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, Secret, StrictInt, StringConstraints

PROJECT_MIN_PORT = 1
PROJECT_MAX_PORT = 65535
ENV_NAME_MIN_LENGTH = 3
ENV_VALUE_MIN_LENGTH = 32

EnvName = Annotated[str, StringConstraints(min_length=ENV_NAME_MIN_LENGTH, pattern=r"^[A-Z_][A-Z0-9_]*$")]
EnvValue = Secret[Annotated[str, StringConstraints(min_length=ENV_VALUE_MIN_LENGTH, pattern=r"^[A-Za-z0-9._-]+$")]]
Port = Annotated[StrictInt, Field(ge=PROJECT_MIN_PORT, le=PROJECT_MAX_PORT)]


class ProjectRealm(StrEnum):
    """Części wygenerowanego projektu, z własnym katalogiem i plikiem .env."""

    BACKEND = "backend"
    FRONTEND = "frontend"
    DATABASE = "database"


class StrictModel(BaseModel):
    """Baza modeli wejścia: nieznane klucze są błędem, a wczytane dane są niezmienne."""

    model_config = ConfigDict(extra="forbid", frozen=True)
