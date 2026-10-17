from enum import StrEnum

from generator.common.schema import Port, ProjectRealm, StrictModel


class ManifestType(StrEnum):
    """Typ template packa, określający, którą część projektu generuje."""

    BACKEND_DB = "backend-db"
    FRONTEND = "frontend"


class ManifestStability(StrEnum):
    """Możliwe poziomy stabilności template packa."""

    ALPHA = "alpha"
    BETA = "beta"
    STABLE = "stable"


class ManifestFramework(StrictModel):
    """Framework, jaki implementuje template pack z tym manifestem."""

    name: str
    version: str


class ManifestLanguage(StrictModel):
    """Język programowania, w jakim napisany jest template pack z tym manifestem."""

    name: str
    version: str


class ManifestDatabase(StrictModel):
    """Baza danych, jaką ma template pack z tym manifestem."""

    engine: str
    version: str


class Manifest(StrictModel):
    """
    Manifest template packa.
    Pack identyfikuje nazwa jego katalogu, a name służy tylko do wyświetlania.
    database jest opcjonalne, bo nie każdy pack ma bazę danych.
    ports to domyślne porty, gdy konfiguracja ich nie podaje.
    """

    name: str
    type: ManifestType
    version: str
    framework: ManifestFramework
    language: ManifestLanguage
    database: ManifestDatabase | None = None
    stability: ManifestStability
    ports: dict[ProjectRealm, Port]
    contributions: list[str]
    required_envs: dict[ProjectRealm, list[str]]
