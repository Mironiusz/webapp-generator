from generator.configuration.schema import ConfigFile, NormalizedConfig
from generator.registry.schema import Manifest
from generator.settings.logger import get_logger

logger = get_logger(__name__)


class Normalizer:
    """
    Tutaj konfiguracja zostaje uporządkowana i znormalizowana. Wynikiem normalizacji powinien być docelowy model konfiguracji: uporządkowany, uzupełniony o dane domyślne i poprawny semantycznie. Poprawność semantyczna oznacza tutaj spójne znaczenie danych, a nie potwierdzenie, że dana technologia lub kombinacja jest obsługiwana przez generator.
    Normalizacja obejmuje:

    - uzupełnienie domyślnych portów
    - ujednolicenie nazw technologii
    - zamiana ścieżki względnej na docelową ścieżkę output_dir
    - uzupełnienie domyślnych wartości env
    """

    def __init__(self, config_file: ConfigFile, frontend_manifest: Manifest, backend_manifest: Manifest):
        self.config_file = config_file
        self.frontend_manifest = frontend_manifest
        self.backend_manifest = backend_manifest

    def _fill_default_ports(self) -> None:
        pass

    def _fill_default_envs(self) -> None:
        pass

    def run_normalization(self) -> NormalizedConfig:
        self._fill_default_ports()
        self._fill_default_envs()
        return NormalizedConfig.model_validate(self.config_file.model_dump())
