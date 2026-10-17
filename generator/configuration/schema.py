from pathlib import Path
from typing import Annotated, Literal

from pydantic import AfterValidator, Field, StrictInt, StringConstraints

from generator.common.schema import ProjectRealm, StrictModel

PROJECT_NAME_MAX_LENGTH = 127
PROJECT_MIN_PORT = 1
PROJECT_MAX_PORT = 65535


def _ensure_absolute(path: Path) -> Path:
    """Przepuszcza tylko ścieżki bezwzględne w systemie, na którym działa generator, a pozostałe odrzuca błędem walidacji."""

    if not path.is_absolute():
        raise ValueError("Ścieżka musi być bezwzględna")

    return path


class ProjectConfig(StrictModel):
    """
    Sekcja project: nazwa projektu i katalog, w którym projekt powstanie.
    """

    name: Annotated[str, StringConstraints(pattern=r"^[a-z](?:[a-z0-9_-]*[a-z0-9])?$", max_length=PROJECT_NAME_MAX_LENGTH)]
    output_dir: Annotated[Path, AfterValidator(_ensure_absolute)]


class ConfigFile(StrictModel):
    """Konfiguracja wejściowa generatora w wersji 1 formatu."""

    version: Literal[1]
    project: ProjectConfig
    frontend: str
    backend: str
    ports: dict[ProjectRealm, Annotated[int, Field(ge=PROJECT_MIN_PORT, le=PROJECT_MAX_PORT)] | None]
    envs: dict[ProjectRealm, dict[str, str | StrictInt]]
