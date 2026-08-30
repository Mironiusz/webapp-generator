from __future__ import annotations

from enum import StrEnum
from functools import lru_cache
from importlib.metadata import version
from pathlib import Path
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = [
    "ApiSettings",
    "DatabaseSettings",
    "Environment",
    "LogLevel",
    "LogSettings",
    "Settings",
    "SettingsSection",
    "get_settings",
]


_PROJECT_ROOT_PATH = Path(__file__).resolve().parents[2]

_MIN_PRODUCTION_SECRET_LENGTH = 32

_PACKAGE_VERSION = version("backend")

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Environment(StrEnum):
    """Środowisko, w którym uruchomiony jest backend."""

    LOCAL = "local"
    PRODUCTION = "production"


class SettingsSection(BaseModel):
    """Baza każdej sekcji ustawień."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )


class ApiSettings(SettingsSection):
    """Ustawienia warstwy HTTP wystawianej przez aplikację."""

    title: str = "backend"
    version: str = _PACKAGE_VERSION
    root_path: str = ""
    docs_enabled: bool = True


class DatabaseSettings(SettingsSection):
    """Ustawienia połączenia z bazą danych."""

    url: str = "sqlite+aiosqlite:///./app.db"
    echo: bool = False
    pool_pre_ping: bool = True


class LogSettings(SettingsSection):
    """Ustawienia loggera aplikacji."""

    base_name: str = "backend"
    console_level: LogLevel = "DEBUG"
    file_level: LogLevel = "DEBUG"
    file_path: Path = Path("log/backend.log")


class Settings(BaseSettings):
    """Konfiguracja backendu budowana z plików env, z podziałem na sekrety i ustawienia lokalne."""

    model_config = SettingsConfigDict(
        env_file=(
            _PROJECT_ROOT_PATH / ".env",
            _PROJECT_ROOT_PATH / ".env.local",
        ),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="forbid",
        frozen=True,
    )

    secret_key: SecretStr
    environment: Environment = Environment.LOCAL

    api: ApiSettings = ApiSettings()
    database: DatabaseSettings = DatabaseSettings()
    log: LogSettings = LogSettings()

    @property
    def is_production(self) -> bool:
        """Informuje, czy backend działa na produkcji."""
        return self.environment is Environment.PRODUCTION

    @model_validator(mode="after")
    def _enforce_production_rules(self) -> Self:
        """Pilnuje reguł, które wolno złamać lokalnie, ale nie na produkcji."""
        if not self.is_production:
            return self

        if len(self.secret_key.get_secret_value()) < _MIN_PRODUCTION_SECRET_LENGTH:
            raise ValueError(f"SECRET_KEY na produkcji musi mieć co najmniej {_MIN_PRODUCTION_SECRET_LENGTH} znaków")

        if self.database.echo:
            raise ValueError("DATABASE__ECHO na produkcji wypisuje zapytania SQL do logów")

        return self


@lru_cache
def get_settings() -> Settings:
    """Zwraca singleton konfiguracji."""
    return Settings()
