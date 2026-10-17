from generator.settings.logger import get_logger

logger = get_logger(__name__)


class Core:
    def __init__(self) -> None:
        """
        Tworzy Core.
        """
        logger.info("Core created")

    def _run_cli(self) -> None:
        """
        Uruchamia CLI.
        W CLI użytkownik wybiera tryb (plik, wznowienie lub kontynuacja trybu CLI).
        Następnie CLI pyta użytkownika o wszystko, czego potrzbuje,
        a następnie zwraca pozyskane dane.
        """
        logger.info("[mock] CLI opened")

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
        self._run_cli()
        self._run_normalizer()
        self._run_validator()
        self._run_pipeline()
        self._pass_result()
        self._show_stats()
