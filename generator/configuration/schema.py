from collections.abc import Mapping
from pathlib import Path
from typing import Annotated, Literal

from pydantic import AfterValidator, SecretStr, StrictInt, StringConstraints

from generator.common.schema import Port, ProjectRealm, StrictModel

PROJECT_NAME_MAX_LENGTH = 127


def _ensure_absolute(path: Path) -> Path:
    """Odrzuca ścieżki, które nie są bezwzględne w systemie, na którym działa generator."""

    if not path.is_absolute():
        raise ValueError("Path must be absolute")

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
    ports: Mapping[ProjectRealm, Port | None]
    envs: dict[ProjectRealm, dict[str, SecretStr | StrictInt]] | None


class NormalizedConfig(ConfigFile):
    """Konfiguracja znormalizowana generatora w wersji 1 formatu."""

    ports: Mapping[ProjectRealm, Port]
