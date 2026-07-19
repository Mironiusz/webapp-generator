from config.logger import configure_logging
from core import Core

configure_logging()

core = Core()
core.run_generator()
