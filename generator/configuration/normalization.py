import secrets
from collections.abc import Mapping

from pydantic import SecretStr, StrictInt

from generator.common.schema import Port, ProjectRealm
from generator.configuration.schema import ConfigFile, NormalizedConfig
from generator.registry.schema import Manifest
from generator.settings.logger import get_logger

logger = get_logger(__name__)


class Normalizer:
    """
    Tutaj konfiguracja zostaje uporządkowana i znormalizowana. Wynikiem normalizacji powinien być docelowy model konfiguracji: uporządkowany, uzupełniony o dane domyślne i poprawny semantycznie. Poprawność semantyczna oznacza tutaj spójne znaczenie danych, a nie potwierdzenie, że dana technologia lub kombinacja jest obsługiwana przez generator.
    Normalizacja obejmuje:

    - uzupełnienie domyślnych portów
    - wylosowanie brakujących sekretów wymaganych przez template packi
    """

    def __init__(self, config_file: ConfigFile, frontend_manifest: Manifest, backend_manifest: Manifest):
        self.config_file = config_file
        self.manifests = (frontend_manifest, backend_manifest)

    def _get_default_ports(self) -> dict[ProjectRealm, Port]:
        default_ports: dict[ProjectRealm, Port] = {}
        for manifest in self.manifests:
            default_ports.update(manifest.ports)

        return default_ports

    def _get_required_env_names(self) -> dict[ProjectRealm, list[str]]:
        required_env_names: dict[ProjectRealm, list[str]] = {realm: [] for realm in ProjectRealm}
        for manifest in self.manifests:
            for realm, env_names in manifest.required_envs.items():
                for env_name in env_names:
                    if env_name not in required_env_names[realm]:
                        required_env_names[realm].append(env_name)

        return required_env_names

    def _fill_default_ports(self) -> Mapping[ProjectRealm, Port]:
        """
        Uzupełnia porty domyślnymi wartościami z manifestów wybranych template packów.
        Port podany przez użytkownika zostaje bez zmian.
        Niepodany port jest brany z manifestu, który go deklaruje.
        Niepodany port części projektu, której nie deklaruje żaden z manifestów, jest usuwany.
        """

        default_ports = self._get_default_ports()

        target_ports: dict[ProjectRealm, Port] = {}
        for realm in ProjectRealm:
            target_port = self.config_file.ports[realm]
            if target_port is None:
                target_port = default_ports.get(realm)
            if target_port is None:
                continue
            target_ports[realm] = target_port

        return target_ports

    def _fill_default_envs(self) -> dict[ProjectRealm, dict[str, SecretStr | StrictInt]]:
        """
        Uzupełnia zmienne środowiskowe sekretami wymaganymi przez manifesty wybranych template packów.
        Zmienna podana przez użytkownika zostaje bez zmian.
        Niepodany sekret wymagany przez manifest jest losowany.
        """

        config_file_envs = self.config_file.envs or {}

        target_envs: dict[ProjectRealm, dict[str, SecretStr | StrictInt]] = {}
        for realm, env_names in self._get_required_env_names().items():
            realm_envs = config_file_envs.get(realm, {})

            target_realm_envs: dict[str, SecretStr | StrictInt] = {}
            for env_name in env_names:
                if env_name in realm_envs:
                    target_realm_envs[env_name] = realm_envs[env_name]
                else:
                    target_realm_envs[env_name] = SecretStr(secrets.token_urlsafe(32))

            target_envs[realm] = target_realm_envs

        return target_envs

    def run_normalization(self) -> NormalizedConfig:
        target_ports = self._fill_default_ports()
        target_envs = self._fill_default_envs()

        config_file = self.config_file.model_dump()
        config_file["ports"] = target_ports
        config_file["envs"] = target_envs

        logger.debug(config_file)

        return NormalizedConfig.model_validate(config_file)
