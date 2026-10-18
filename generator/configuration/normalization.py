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

    def _get_default_ports(self) -> Mapping[ProjectRealm, Port]:
        default_ports = {}
        for manifest in self.manifests:
            for port in manifest.ports:
                default_ports[port] = manifest.ports[port]

        return default_ports

    def _get_required_envs(self) -> dict[ProjectRealm, list[str]]:
        default_envs = {}
        for manifest in self.manifests:
            for env in ProjectRealm:
                default_envs[env] = manifest.required_envs.get(env, [])

        return default_envs

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

    def _fill_default_envs(self) -> dict[ProjectRealm, dict[str, SecretStr | StrictInt]] | None:
        """
        Uzupełnia zmienne środowiskowe sekretami wymaganymi przez manifesty wybranych template packów.
        Zmienna podana przez użytkownika zostaje bez zmian.
        Niepodany sekret wymagany przez manifest jest losowany.
        """

        if self.config_file.envs is None:
            return None

        default_envs = self._get_required_envs()
        logger.debug(default_envs)

        target_envs: dict[ProjectRealm, dict[str, SecretStr | StrictInt]] = {}
        for realm in default_envs:
            realm_envs_config = self.config_file.envs.get(realm)

            logger.debug(realm_envs_config)
            logger.debug(default_envs[realm])

            target_env_realm = {}
            for env_variable in default_envs[realm]:
                if realm_envs_config is not None:
                    target_env_realm[env_variable] = realm_envs_config.get(env_variable, SecretStr(secrets.token_urlsafe(32)))

            target_envs[realm] = target_env_realm

        logger.debug(target_envs)
        return target_envs

    def run_normalization(self) -> NormalizedConfig:
        target_ports = self._fill_default_ports()
        target_envs = self._fill_default_envs()

        config_file = self.config_file.model_dump()
        config_file["ports"] = target_ports
        config_file["envs"] = target_envs

        logger.debug(config_file)

        return NormalizedConfig.model_validate(config_file)
