from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class ProjectRealm(StrEnum):
    """Części wygenerowanego projektu, które mają własny katalog i własny plik .env. Służą jako klucze w sekcjach ports i envs."""

    BACKEND = "backend"
    FRONTEND = "frontend"
    DATABASE = "database"


class StrictModel(BaseModel):
    """Baza modeli wejścia: nieznane klucze są błędem, a wczytana konfiguracja jest niezmienna."""

    model_config = ConfigDict(extra="forbid", frozen=True)
