import logging

from config.config import BASE_LOGGER_NAME
from config.logger import get_logger


def test_get_logger_returns_standard_logger() -> None:
    logger = get_logger("fleethand.tasks")

    assert isinstance(logger, logging.Logger)


def test_get_logger_adds_application_prefix() -> None:
    logger = get_logger("fleethand.tasks")

    assert logger.name == "generator.fleethand.tasks"


def test_get_logger_preserves_full_application_name() -> None:
    logger = get_logger("generator.database.export")

    assert logger.name == "generator.database.export"


def test_get_logger_maps_main_to_base_logger() -> None:
    logger = get_logger("__main__")

    assert logger.name == BASE_LOGGER_NAME


def test_get_logger_does_not_configure_logging_system() -> None:
    logger = get_logger("fleethand.tasks")
    base_logger = logging.getLogger(BASE_LOGGER_NAME)

    assert logger.handlers == []
    assert base_logger.handlers == []
