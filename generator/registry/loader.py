from pathlib import Path

import yaml
from pydantic import ValidationError

from generator.common.errors import InvalidTemplatePackError, format_validation_error, format_yaml_error
from generator.registry.schema import Manifest
from generator.settings.logger import get_logger

logger = get_logger(__name__)


class Loader:
    """
    Klasa zarządzająca wczytaniem manifestu i przerobieniem go na Manifest.
    """

    def _get_manifest(self, manifest_path: Path) -> Manifest:
        """Wczytuje plik manifestu i zwraca obiekt Manifest."""

        try:
            manifest_text = manifest_path.read_text(encoding="utf-8")
            manifest = Manifest.model_validate(yaml.safe_load(manifest_text))
        except (OSError, UnicodeDecodeError) as e:
            raise InvalidTemplatePackError(manifest_path.parent.name, f"Manifest could not be read: {e}") from e
        except yaml.YAMLError as e:
            raise InvalidTemplatePackError(manifest_path.parent.name, f"Manifest is not valid YAML: {format_yaml_error(e)}") from e
        except ValidationError as e:
            raise InvalidTemplatePackError(manifest_path.parent.name, f"Manifest does not match the schema: {format_validation_error(e)}") from e

        logger.debug(manifest)

        return manifest

    def get_manifest(self, manifest_path: Path) -> Manifest:
        return self._get_manifest(manifest_path)
