from generator.common.errors import GeneratorError
from generator.core import Core
from generator.settings.logger import configure_logging, get_logger

logger = get_logger(__name__)

configure_logging()

core = Core()

try:
    core.run_generator()
except GeneratorError as e:
    logger.error(e)
    raise SystemExit(1) from e
