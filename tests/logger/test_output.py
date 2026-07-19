import logging
import re
from pathlib import Path

import pytest

import config.logger as logger_module
from config.logger import configure_logging, get_logger


def _configure_test_logger(
    monkeypatch: pytest.MonkeyPatch,
    log_file_path: Path,
) -> None:
    monkeypatch.setattr(
        logger_module,
        "LOG_FILE_PATH",
        log_file_path,
    )

    configure_logging()


def test_log_is_written_to_console_and_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    log_file_path = tmp_path / "generator.log"

    _configure_test_logger(
        monkeypatch=monkeypatch,
        log_file_path=log_file_path,
    )

    logger = get_logger("fleethand.tasks")

    logger.info("Rozpoczynam przetwarzanie zadań")

    console_output = capsys.readouterr().out
    file_output = log_file_path.read_text(encoding="utf-8")

    assert "Rozpoczynam przetwarzanie zadań" in console_output
    assert "Rozpoczynam przetwarzanie zadań" in file_output
    assert "\x1b[" in console_output
    assert "\x1b[" not in file_output


def test_debug_log_contains_function_name_and_line_number(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    log_file_path = tmp_path / "generator.log"

    _configure_test_logger(
        monkeypatch=monkeypatch,
        log_file_path=log_file_path,
    )

    logger = get_logger("fleethand.tasks")

    logger.debug("Rozpoczynam generowanie tasków")

    file_output = log_file_path.read_text(encoding="utf-8")

    assert re.search(
        r"\| DEBUG \| generator\.fleethand\.tasks: test_debug_log_contains_function_name_and_line_number: \d+ \| Rozpoczynam generowanie tasków",
        file_output,
    )


def test_info_log_uses_standard_format(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    log_file_path = tmp_path / "generator.log"

    _configure_test_logger(
        monkeypatch=monkeypatch,
        log_file_path=log_file_path,
    )

    logger = get_logger("fleethand.tasks")

    logger.info("Przetworzono rekord")

    file_output = log_file_path.read_text(encoding="utf-8")

    assert "| INFO | generator.fleethand.tasks | Przetworzono rekord" in file_output
    assert "generator.fleethand.tasks:" not in file_output


def test_console_and_file_levels_are_independent(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    log_file_path = tmp_path / "generator.log"

    monkeypatch.setattr(
        logger_module,
        "LOG_FILE_PATH",
        log_file_path,
    )
    monkeypatch.setattr(
        logger_module,
        "CONSOLE_LOG_LEVEL",
        logging.WARNING,
    )
    monkeypatch.setattr(
        logger_module,
        "FILE_LOG_LEVEL",
        logging.DEBUG,
    )

    configure_logging()

    logger = get_logger("tests.levels")

    logger.debug("Tylko plik")
    logger.warning("Konsola i plik")

    console_output = capsys.readouterr().out
    file_output = log_file_path.read_text(encoding="utf-8")

    assert "Tylko plik" not in console_output
    assert "Tylko plik" in file_output
    assert "Konsola i plik" in console_output
    assert "Konsola i plik" in file_output


@pytest.mark.parametrize(
    "method_name",
    [
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ],
)
def test_standard_log_methods_write_to_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    method_name: str,
) -> None:
    log_file_path = tmp_path / "generator.log"

    _configure_test_logger(
        monkeypatch=monkeypatch,
        log_file_path=log_file_path,
    )

    logger = get_logger("tests.methods")
    log_method = getattr(logger, method_name)

    log_method(
        "Wiadomość poziomu %s",
        method_name,
    )

    file_output = log_file_path.read_text(encoding="utf-8")

    assert f"Wiadomość poziomu {method_name}" in file_output


def test_exception_writes_traceback(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    log_file_path = tmp_path / "generator.log"

    _configure_test_logger(
        monkeypatch=monkeypatch,
        log_file_path=log_file_path,
    )

    logger = get_logger("tests.exceptions")

    try:
        raise ValueError("Niepoprawna wartość")
    except ValueError:
        logger.exception("Operacja zakończyła się błędem")

    file_output = log_file_path.read_text(encoding="utf-8")

    assert "Operacja zakończyła się błędem" in file_output
    assert "Traceback" in file_output
    assert "ValueError: Niepoprawna wartość" in file_output


def test_external_logger_is_not_written_to_application_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    log_file_path = tmp_path / "generator.log"

    _configure_test_logger(
        monkeypatch=monkeypatch,
        log_file_path=log_file_path,
    )

    external_logger = logging.getLogger("external.library")
    null_handler = logging.NullHandler()

    external_logger.addHandler(null_handler)
    external_logger.setLevel(logging.DEBUG)
    external_logger.propagate = False

    try:
        external_logger.error("Log z biblioteki zewnętrznej")
    finally:
        external_logger.removeHandler(null_handler)
        null_handler.close()

    file_output = log_file_path.read_text(encoding="utf-8")

    assert "Log z biblioteki zewnętrznej" not in file_output


def test_logger_does_not_create_historical_files(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    log_file_path = tmp_path / "generator.log"

    _configure_test_logger(
        monkeypatch=monkeypatch,
        log_file_path=log_file_path,
    )

    logger = get_logger("tests.files")

    logger.info("Test pliku")

    created_files = {path.name for path in tmp_path.iterdir() if path.is_file()}

    assert created_files == {
        "generator.log",
    }
