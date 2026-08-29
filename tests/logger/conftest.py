import logging
from collections.abc import Iterator

import pytest

import config.logger as logger_module
from config.config import BASE_LOGGER_NAME


def _reset_application_logging() -> None:
    logger_module.Logger._instance = None

    logger_names = [BASE_LOGGER_NAME]
    logger_names.extend(name for name, logger in logging.Logger.manager.loggerDict.items() if name.startswith(f"{BASE_LOGGER_NAME}.") and isinstance(logger, logging.Logger))

    for logger_name in logger_names:
        logger = logging.getLogger(logger_name)

        for handler in tuple(logger.handlers):
            logger.removeHandler(handler)
            handler.close()

        logger.setLevel(logging.NOTSET)
        logger.propagate = True


@pytest.fixture(autouse=True)
def reset_application_logging() -> Iterator[None]:
    _reset_application_logging()

    yield

    _reset_application_logging()
