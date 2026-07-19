from config.logger import get_logger

logger = get_logger(__name__)


class Core:
    def __init__(self):
        logger.info("Core created")

    def _run_config(self):
        logger.info("[mock] Config loaded")

    def _run_normalizer(self):
        logger.info("[mock] Config normalized")

    def _run_validator(self):
        logger.info("[mock] Config validated")

    def _run_pipeline(self):
        logger.info("[mock] Pipeline ran")

    def _pass_result(self):
        logger.info("[mock] Result project passed")

    def _show_stats(self):
        logger.info("[mock] Stats shown")

    def run_generator(self):
        self._run_config()
        self._run_normalizer()
        self._run_validator()
        self._run_pipeline()
        self._pass_result()
        self._show_stats()
