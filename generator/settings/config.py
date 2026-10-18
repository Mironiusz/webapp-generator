import logging
from pathlib import Path

BASE_LOGGER_NAME = "generator"

CONSOLE_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.DEBUG

LOG_FILE_PATH = Path("log/generator.log")

ROOT_PATH = Path(__file__).resolve().parents[2]

TEMPLATE_PACKS_PATH = ROOT_PATH / "template_packs"
