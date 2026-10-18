from pathlib import Path

from generator.common.errors import InvalidTemplatePackError, UnknownTemplatePackError
from generator.configuration.loader import Loader as ConfLoader
from generator.configuration.schema import ConfigFile, NormalizedConfig
from generator.core.normalization import Normalizer
from generator.registry.resolver import Resolver
from generator.registry.schema import Manifest, ManifestType
from generator.settings.logger import get_logger

logger = get_logger(__name__)

CONFIG_FILE_PATH = Path(r"C:\wju\Thesis\generator\cli\example_config_file.yaml")


class Core:
    available_packs: dict[str, Manifest]

    def __init__(self) -> None:
        """
        Tworzy Core.
        """
        logger.info("Core created")

    def _load_available_packs(self) -> dict[str, Manifest]:
        """
        Wczytuje manifesty dostępnych template packów.
        Zwraca słownik nazwa packa -> wczytany manifest.
        """

        resolver = Resolver()
        manifest_paths = resolver.get_manifests()
        logger.debug(manifest_paths)
        logger.info("Available template packs loaded")
        return manifest_paths

    def _get_config(self) -> ConfigFile:
        """
        Uruchamia CLI.
        W CLI użytkownik wybiera tryb (plik, wznowienie lub kontynuacja trybu CLI).
        Następnie CLI pyta użytkownika o wszystko, czego potrzbuje,
        a następnie zwraca pozyskane dane.
        """

        logger.info("[mock] CLI opened")

        loader = ConfLoader(CONFIG_FILE_PATH)
        config_file = loader.get_config()
        logger.info("Config file loaded")

        if config_file.backend not in self.available_packs:
            raise UnknownTemplatePackError(config_file.backend)

        backend_manifest = self.available_packs[config_file.backend]
        if backend_manifest.type is not ManifestType.BACKEND_DB:
            raise InvalidTemplatePackError(config_file.backend, "Template pack is not a backend template pack")

        if config_file.frontend not in self.available_packs:
            raise UnknownTemplatePackError(config_file.frontend)

        frontend_manifest = self.available_packs[config_file.frontend]
        if frontend_manifest.type is not ManifestType.FRONTEND:
            raise InvalidTemplatePackError(config_file.frontend, "Template pack is not a frontend template pack")

        logger.info("Target packs verified")

        return config_file

    def _normalize_config(self, config_file: ConfigFile) -> NormalizedConfig:
        """Spełnia 6.5"""
        frontend_manifest = self.available_packs[config_file.frontend]
        backend_manifest = self.available_packs[config_file.backend]

        normalizer = Normalizer(config_file, frontend_manifest, backend_manifest)
        logger.info("[mock] Config normalized")

        return normalizer.run_normalization()

    def _validate_config(self, config: NormalizedConfig) -> NormalizedConfig:
        """Spełnia 6.6"""
        logger.info("[mock] Config validated")
        return config

    def _run_pipeline(self) -> None:
        logger.info("[mock] Pipeline ran")

    def _pass_result(self) -> None:
        logger.info("[mock] Result project passed")

    def _show_stats(self) -> None:
        logger.info("[mock] Stats shown")

    def run_generator(self) -> None:
        self.available_packs = self._load_available_packs()
        config = self._get_config()
        config = self._normalize_config(config)
        config = self._validate_config(config)
        self._run_pipeline()
        self._pass_result()
        self._show_stats()
