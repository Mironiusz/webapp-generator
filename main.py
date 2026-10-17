from generator.core import Core
from generator.settings.logger import configure_logging

configure_logging()

core = Core()
core.run_generator()
