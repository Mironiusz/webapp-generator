from generator.config.logger import configure_logging
from generator.core import Core

configure_logging()

core = Core()
core.run_generator()
