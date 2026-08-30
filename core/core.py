from config.logger import get_logger

logger = get_logger(__name__)


class Core:
    def __init__(self) -> None:
        logger.info("Core created")

    def _run_config(self) -> None:
        logger.info("[mock] Config loaded")

    def _run_normalizer(self) -> None:
        logger.info("[mock] Config normalized")

    def _run_validator(self) -> None:
        logger.info("[mock] Config validated")

    def _run_pipeline(self) -> None:
        logger.info("[mock] Pipeline ran")

    def _pass_result(self) -> None:
        logger.info("[mock] Result project passed")

    def _show_stats(self) -> None:
        logger.info("[mock] Stats shown")

    def run_generator(self) -> None:
        self._run_config()
        self._run_normalizer()
        self._run_validator()
        self._run_pipeline()
        self._pass_result()
        self._show_stats()
