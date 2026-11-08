from pathlib import Path

from generator.common.schema import ProjectPart
from generator.registry.loader import Loader
from generator.registry.schema import Manifest, TemplatePack
from generator.settings.config import TEMPLATE_PACKS_PATH
from generator.settings.logger import get_logger

logger = get_logger(__name__)

MANIFEST_FILE_NAME = "manifest.yaml"
TEMPLATE_PACK_TEMPLATE_NAME = "template"
TEMPLATE_PACK_CONTRIBUTIONS_NAME = "contributions"


class Resolver:
    """Odnajduje template packi w katalogu template_packs i buduje z nich rejestr."""

    def get_pack_dirs(self) -> dict[str, Path]:
        """Zwraca słownik nazwa packa -> katalog packa, pomijając z ostrzeżeniem katalogi bez manifestu."""
        pack_dirs: dict[str, Path] = {}

        for pack_dir in sorted(TEMPLATE_PACKS_PATH.iterdir()):
            if not pack_dir.is_dir():
                continue

            if not (pack_dir / MANIFEST_FILE_NAME).is_file():
                logger.warning("%s is not a valid template pack. %s missing.", pack_dir, MANIFEST_FILE_NAME)
                continue

            pack_dirs[pack_dir.name] = pack_dir

        logger.debug("Detected template packs: %s", ", ".join(pack_dirs))

        return pack_dirs

    def _get_missing_parts(self, template_dir: Path, manifest: Manifest) -> list[ProjectPart]:
        """Zwraca części projektu z manifestu, które nie mają swojego katalogu w katalogu template."""

        return [part for part in manifest.ports if not (template_dir / part).is_dir()]

    def get_template_packs(self) -> dict[str, TemplatePack]:
        """Zwraca słownik nazwa packa -> wczytany manifest wraz z nazwą packa i ścieżką do katalogu /template, który jest w packu."""
        template_packs: dict[str, TemplatePack] = {}
        loader = Loader()

        for pack_name, pack_dir in self.get_pack_dirs().items():
            template_dir = pack_dir / TEMPLATE_PACK_TEMPLATE_NAME
            contributions_dir = pack_dir / TEMPLATE_PACK_CONTRIBUTIONS_NAME

            if not template_dir.is_dir():
                logger.warning("Template pack %s does not have a /%s dir, so it was not loaded", pack_name, TEMPLATE_PACK_TEMPLATE_NAME)
                continue

            if not contributions_dir.is_dir():
                logger.warning("Template pack %s does not have a /%s dir, so it was not loaded", pack_name, TEMPLATE_PACK_CONTRIBUTIONS_NAME)
                continue

            manifest = loader.get_manifest(pack_dir / MANIFEST_FILE_NAME)

            missing_parts = self._get_missing_parts(template_dir, manifest)
            if missing_parts:
                logger.warning("Template pack %s does not have dirs for parts: %s, so it was not loaded", pack_name, ", ".join(missing_parts))
                continue

            template_packs[pack_name] = TemplatePack(name=pack_name, path=template_dir, manifest=manifest)

        return template_packs
