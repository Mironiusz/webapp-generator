from __future__ import annotations

import logging
import sys
import threading
from typing import ClassVar, Final, Self, cast, final

from .config import LogLevel, get_settings

__all__ = [
    "configure_logging",
    "get_logger",
]


_STANDARD_LOG_FORMAT: Final = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
_DEBUG_LOG_FORMAT: Final = "%(asctime)s | %(levelname)s | %(name)s: %(funcName)s: %(lineno)d | %(message)s"
_DATE_FORMAT: Final = "%Y-%m-%d %H:%M:%S"

_COLOR_RESET: Final = "\x1b[0m"

_COLOR_BY_LEVEL: Final[dict[int, str]] = {
    logging.DEBUG: "\x1b[36m",
    logging.INFO: "\x1b[32m",
    logging.WARNING: "\x1b[33m",
    logging.ERROR: "\x1b[31m",
    logging.CRITICAL: "\x1b[1;31m",
}


class _LevelAwareFormatter(logging.Formatter):
    """Formatuje logi DEBUG szerzej niż pozostałe poziomy."""

    def __init__(self) -> None:
        super().__init__()

        self._standard_formatter = logging.Formatter(
            fmt=_STANDARD_LOG_FORMAT,
            datefmt=_DATE_FORMAT,
        )
        self._debug_formatter = logging.Formatter(
            fmt=_DEBUG_LOG_FORMAT,
            datefmt=_DATE_FORMAT,
        )

    def format(self, record: logging.LogRecord) -> str:
        formatter = self._debug_formatter if record.levelno == logging.DEBUG else self._standard_formatter

        return formatter.format(record)


class _ConsoleFormatter(_LevelAwareFormatter):
    """Dodaje kolor ANSI do komunikatu przeznaczonego dla konsoli."""

    def format(self, record: logging.LogRecord) -> str:
        formatted_message = super().format(record)
        color = _COLOR_BY_LEVEL.get(record.levelno)

        if color is None:
            return formatted_message

        return f"{color}{formatted_message}{_COLOR_RESET}"


@final
class Logger:
    """Jednorazowo konfiguruje nadrzędny logger aplikacji."""

    _instance: ClassVar[Logger | None] = None
    _lock: ClassVar[threading.RLock] = threading.RLock()

    _initialized: bool

    def __new__(cls) -> Self:
        with cls._lock:
            if cls._instance is None:
                instance = super().__new__(cls)
                instance._initialized = False
                cls._instance = instance

            return cast(Self, cls._instance)

    def __init__(self) -> None:
        if self._initialized:
            return

        self._load_config()
        self._base_logger = logging.getLogger(self._base_logger_name)
        self._configured = False
        self._initialized = True

    def configure(self) -> logging.Logger:
        """Konfiguruje bazowy logger tylko podczas pierwszego wywołania."""
        with self._lock:
            if self._configured:
                return self._base_logger

            self._validate_config()
            self._base_logger = self._configure_base_logger()
            self._configured = True

            return self._base_logger

    def _load_config(self) -> None:
        """Wczytuje konfigurację loggera z sekcji log w ustawieniach aplikacji."""
        log_settings = get_settings().log

        self._base_logger_name = log_settings.base_name
        self._console_log_level = _resolve_log_level(log_settings.console_level)
        self._file_log_level = _resolve_log_level(log_settings.file_level)
        self._log_file_path = log_settings.file_path

    def _validate_config(self) -> None:
        """Pilnuje, by pusta nazwa bazowa nie podpięła konfiguracji pod root logger."""
        if not self._base_logger_name.strip():
            raise ValueError("LOG__BASE_NAME musi być niepustym stringiem")

    def _configure_base_logger(self) -> logging.Logger:
        """Buduje bazowy logger z handlerem konsolowym i plikowym."""
        self._log_file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setLevel(self._console_log_level)
        console_handler.setFormatter(_ConsoleFormatter())

        file_handler = logging.FileHandler(
            filename=self._log_file_path,
            mode="w",
            encoding="utf-8",
        )
        file_handler.setLevel(self._file_log_level)
        file_handler.setFormatter(_LevelAwareFormatter())

        logger = logging.getLogger(self._base_logger_name)

        self._replace_handlers(
            logger=logger,
            handlers=(
                console_handler,
                file_handler,
            ),
        )

        logger.setLevel(
            min(
                self._console_log_level,
                self._file_log_level,
            )
        )
        logger.propagate = False

        return logger

    @staticmethod
    def _replace_handlers(
        logger: logging.Logger,
        handlers: tuple[logging.Handler, ...],
    ) -> None:
        """Zastępuje handlery bazowego loggera i zamyka poprzednie."""
        for handler in tuple(logger.handlers):
            logger.removeHandler(handler)
            handler.close()

        for handler in handlers:
            logger.addHandler(handler)


def configure_logging() -> logging.Logger:
    """Konfiguruje system logowania aplikacji i zwraca bazowy logger."""
    return Logger().configure()


def get_logger(name: str) -> logging.Logger:
    """Zwraca logger modułu bez uruchamiania konfiguracji systemu."""
    return logging.getLogger(_normalize_logger_name(name))


def _resolve_log_level(level: LogLevel) -> int:
    """Zamienia nazwę poziomu z konfiguracji na liczbę rozumianą przez moduł logging."""
    return logging.getLevelNamesMapping()[level]


def _normalize_logger_name(name: str) -> str:
    """Buduje nazwę loggera należącą do przestrzeni nazw aplikacji."""
    if not isinstance(name, str):
        raise TypeError("Nazwa loggera musi być stringiem")

    base_logger_name = get_settings().log.base_name
    normalized_name = name.strip()

    if not normalized_name:
        raise ValueError("Nazwa loggera nie może być pusta")

    if normalized_name == "__main__":
        return base_logger_name

    if normalized_name == base_logger_name or normalized_name.startswith(f"{base_logger_name}."):
        return normalized_name

    return f"{base_logger_name}.{normalized_name}"
