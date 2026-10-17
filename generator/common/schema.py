from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

PROJECT_MIN_PORT = 1
PROJECT_MAX_PORT = 65535

Port = Annotated[int, Field(ge=PROJECT_MIN_PORT, le=PROJECT_MAX_PORT)]


class ProjectRealm(StrEnum):
    """Części wygenerowanego projektu, z własnym katalogiem i plikiem .env."""

    BACKEND = "backend"
    FRONTEND = "frontend"
    DATABASE = "database"


class StrictModel(BaseModel):
    """Baza modeli wejścia: nieznane klucze są błędem, a wczytane dane są niezmienne."""

    model_config = ConfigDict(extra="forbid", frozen=True)
