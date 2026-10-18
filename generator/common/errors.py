from pathlib import Path

import yaml
from pydantic import ValidationError


def format_validation_error(error: ValidationError) -> str:
    """Składa błędy walidacji pydantica w jedną linię."""
    descriptions: list[str] = []
    for detail in error.errors():
        location = ".".join(str(part) for part in detail["loc"])
        descriptions.append(f"{location}: {detail['msg']}" if location else detail["msg"])

    return "; ".join(descriptions)


def format_yaml_error(error: yaml.YAMLError) -> str:
    """Opisuje błąd składni YAML z numerem linii i kolumny."""
    if isinstance(error, yaml.MarkedYAMLError) and error.problem_mark is not None and error.problem is not None:
        mark = error.problem_mark
        return f"line {mark.line + 1}, column {mark.column + 1}: {error.problem}"

    return str(error)


class GeneratorError(Exception):
    """Baza błędów, na których core przerywa generację i pokazuje komunikat użytkownikowi."""


class UnknownTemplatePackError(GeneratorError):
    """Template pack o tej nazwie nie istnieje."""

    def __init__(self, pack_name: str) -> None:
        self.pack_name = pack_name
        super().__init__(f"Template pack {pack_name} does not exist.")


class InvalidTemplatePackError(GeneratorError):
    """Template pack nie spełnia wymagań generatora, np. ma niepoprawny manifest."""

    def __init__(self, pack_name: str, reason: str) -> None:
        self.pack_name = pack_name
        self.reason = reason
        super().__init__(f"Template pack {pack_name} is invalid: {reason}")


class InvalidConfigFileError(GeneratorError):
    """Plik konfiguracyjny nie jest poprawny."""

    def __init__(self, config_file: Path, reason: str) -> None:
        self.config_file = config_file
        self.reason = reason
        super().__init__(f"Config file {config_file} is invalid: {reason}")
