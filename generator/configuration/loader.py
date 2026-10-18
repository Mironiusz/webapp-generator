from pathlib import Path

import yaml
from pydantic import ValidationError

from generator.common.errors import InvalidConfigFileError, format_validation_error, format_yaml_error
from generator.configuration.schema import ConfigFile
from generator.settings.logger import get_logger

logger = get_logger(__name__)


class Loader:
    """
    Klasa zarządzająca wczytaniem pliku i przerobieniem go na ConfigFile.
    """

    def __init__(self, config_file_path: Path) -> None:
        self.config_file_path = config_file_path

    def _get_config_file(self) -> ConfigFile:
        """Wczytuje plik konfiguracyjny i zwraca obiekt ConfigFile."""

        try:
            config_text = self.config_file_path.read_text(encoding="utf-8")
            config_file = ConfigFile.model_validate(yaml.safe_load(config_text))
        except (OSError, UnicodeDecodeError) as e:
            raise InvalidConfigFileError(self.config_file_path, f"File could not be read: {e}") from e
        except yaml.YAMLError as e:
            raise InvalidConfigFileError(self.config_file_path, f"File is not valid YAML: {format_yaml_error(e)}") from e
        except ValidationError as e:
            raise InvalidConfigFileError(self.config_file_path, f"File does not match the schema: {format_validation_error(e)}") from e

        logger.debug(config_file)

        return config_file

    def get_config(self) -> ConfigFile:
        return self._get_config_file()
