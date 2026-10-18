from pathlib import Path

from generator.registry.loader import Loader
from generator.registry.schema import Manifest
from generator.settings.config import TEMPLATE_PACKS_PATH
from generator.settings.logger import get_logger

logger = get_logger(__name__)

MANIFEST_FILE_NAME = "manifest.yaml"


class Resolver:
    """Odnajduje template packi w katalogu template_packs i udostępnia ich manifesty."""

    def get_manifest_paths(self) -> dict[str, Path]:
        """Zwraca słownik nazwa packa -> ścieżka jego manifestu."""

        manifest_paths = {}

        for tp_path in sorted(TEMPLATE_PACKS_PATH.iterdir()):
            if not tp_path.is_dir():
                continue

            manifest_path = tp_path / MANIFEST_FILE_NAME

            if not manifest_path.is_file():
                logger.warning("%s is not a valid template pack. %s missing.", tp_path, MANIFEST_FILE_NAME)
                continue

            manifest_paths[tp_path.name] = manifest_path

        logger.debug(manifest_paths)

        return manifest_paths

    def get_manifests(self) -> dict[str, Manifest]:
        """Zwraca słownik nazwa packa -> wczytany manifest."""
        manifest_paths = self.get_manifest_paths()
        manifests = {}
        loader = Loader()
        for manifest_name in manifest_paths:
            manifests[manifest_name] = loader.get_manifest(manifest_paths[manifest_name])

        return manifests

    def get_path(self, name: str) -> Path:
        """Zwraca ścieżkę manifestu packa o podanej nazwie."""
        raise NotImplementedError
