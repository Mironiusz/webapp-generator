import logging
import sys
from pathlib import Path

import pytest

import config.logger as logger_module
from config.config import BASE_LOGGER_NAME
from config.logger import configure_logging, get_logger


def test_configure_logging_configures_base_logger(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        logger_module,
        "LOG_FILE_PATH",
        tmp_path / "generator.log",
    )

    logger = configure_logging()

    assert logger.name == BASE_LOGGER_NAME
    assert logger.level == min(
        logger_module.CONSOLE_LOG_LEVEL,
        logger_module.FILE_LOG_LEVEL,
    )
    assert logger.propagate is False


def test_configure_logging_adds_one_console_and_one_file_handler(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        logger_module,
        "LOG_FILE_PATH",
        tmp_path / "generator.log",
    )

    logger = configure_logging()

    console_handlers = [handler for handler in logger.handlers if type(handler) is logging.StreamHandler]
    file_handlers = [handler for handler in logger.handlers if isinstance(handler, logging.FileHandler)]

    assert len(console_handlers) == 1
    assert len(file_handlers) == 1


def test_configure_logging_is_idempotent(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        logger_module,
        "LOG_FILE_PATH",
        tmp_path / "generator.log",
    )

    first = configure_logging()
    second = configure_logging()

    assert first is second
    assert len(first.handlers) == 2


def test_configure_logging_creates_log_directory(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    log_file_path = tmp_path / "nested" / "log" / "generator.log"

    monkeypatch.setattr(
        logger_module,
        "LOG_FILE_PATH",
        log_file_path,
    )

    configure_logging()

    assert log_file_path.parent.is_dir()
    assert log_file_path.is_file()


def test_configure_logging_truncates_existing_log_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    log_file_path = tmp_path / "generator.log"
    log_file_path.write_text(
        "historyczne logi",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        logger_module,
        "LOG_FILE_PATH",
        log_file_path,
    )

    configure_logging()

    assert log_file_path.read_text(encoding="utf-8") == ""


def test_configure_logging_rejects_string_log_level(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        logger_module,
        "LOG_FILE_PATH",
        tmp_path / "generator.log",
    )
    monkeypatch.setattr(
        logger_module,
        "CONSOLE_LOG_LEVEL",
        "DEBUG",
    )

    with pytest.raises(TypeError, match="CONSOLE_LOG_LEVEL"):
        configure_logging()


def test_configure_logging_does_not_modify_root_logger(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        logger_module,
        "LOG_FILE_PATH",
        tmp_path / "generator.log",
    )

    root_logger = logging.getLogger()
    handlers_before = tuple(root_logger.handlers)
    level_before = root_logger.level

    configure_logging()

    assert tuple(root_logger.handlers) == handlers_before
    assert root_logger.level == level_before


def test_configure_logging_does_not_replace_standard_streams(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        logger_module,
        "LOG_FILE_PATH",
        tmp_path / "generator.log",
    )

    stdout_before = sys.stdout
    stderr_before = sys.stderr

    configure_logging()

    assert sys.stdout is stdout_before
    assert sys.stderr is stderr_before


def test_module_logger_has_no_handlers_and_propagates(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        logger_module,
        "LOG_FILE_PATH",
        tmp_path / "generator.log",
    )

    configure_logging()

    logger = get_logger("fleethand.tasks")

    assert logger.handlers == []
    assert logger.propagate is True
