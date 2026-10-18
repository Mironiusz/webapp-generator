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
    - pominięcie z ostrzeżeniem portów i zmiennych środowiskowych, których nie deklarują wybrane template packi
    """

    def __init__(self, config_file: ConfigFile, frontend_manifest: Manifest, backend_manifest: Manifest):
        self.config_file = config_file
        self.manifests = (frontend_manifest, backend_manifest)

    def _get_default_ports(self) -> dict[ProjectRealm, Port]:
        """
        Zbiera domyślne porty z manifestów wybranych template packów.
        Klucze wyniku wyznaczają części projektu, które istnieją w generowanym projekcie.
        """
        default_ports: dict[ProjectRealm, Port] = {}
        for manifest in self.manifests:
            default_ports.update(manifest.ports)

        return default_ports

    def _get_required_env_names(self) -> dict[ProjectRealm, list[str]]:
        """
        Zbiera nazwy zmiennych środowiskowych wymaganych przez manifesty wybranych template packów.
        Nazwy z kilku manifestów są łączone bez powtórzeń, w kolejności z manifestów.
        Każda część projektu ma wpis, nawet z pustą listą.
        Zmienne wymagane dla części projektu bez portu są pomijane.
        """
        required_env_names: dict[ProjectRealm, list[str]] = {realm: [] for realm in self._get_default_ports()}
        for manifest in self.manifests:
            for realm, env_names in manifest.required_envs.items():
                if realm not in required_env_names:
                    continue
                for env_name in env_names:
                    if env_name not in required_env_names[realm]:
                        required_env_names[realm].append(env_name)

        return required_env_names

    def _fill_default_ports(self) -> Mapping[ProjectRealm, Port]:
        """
        Uzupełnia porty domyślnymi wartościami z manifestów wybranych template packów.
        Port podany przez użytkownika zostaje bez zmian.
        Niepodany port jest brany z manifestu, który go deklaruje.
        Część projektu, której nie deklaruje żaden z manifestów, nie dostaje portu.
        Podany dla niej port jest pomijany z ostrzeżeniem.
        """
        default_ports = self._get_default_ports()

        target_ports: dict[ProjectRealm, Port] = {}
        for realm in ProjectRealm:
            target_port = self.config_file.ports.get(realm)

            if realm not in default_ports:
                if target_port is not None:
                    logger.warning("Ignoring port %s for %s, no selected template pack declares it", target_port, realm)
                continue

            if target_port is None:
                target_port = default_ports[realm]

            target_ports[realm] = target_port

        return target_ports

    def _fill_default_envs(self) -> dict[ProjectRealm, dict[str, SecretStr | StrictInt]]:
        """
        Uzupełnia zmienne środowiskowe sekretami wymaganymi przez manifesty wybranych template packów.
        Każda część projektu, która ma port, dostaje swoją sekcję zmiennych, nawet pustą.
        Wymagana zmienna podana przez użytkownika zostaje bez zmian.
        Niepodany sekret wymagany przez manifest jest losowany.
        Zmienna, której nie wymaga żaden z manifestów, jest pomijana z ostrzeżeniem.
        """
        config_file_envs = self.config_file.envs or {}
        required_env_names = self._get_required_env_names()

        for realm, realm_envs in config_file_envs.items():
            for env_name in sorted(realm_envs.keys() - required_env_names.get(realm, [])):
                logger.warning("Ignoring env %s for %s, no selected template pack requires it", env_name, realm)

        target_envs: dict[ProjectRealm, dict[str, SecretStr | StrictInt]] = {}
        for realm, env_names in required_env_names.items():
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
        """
        Buduje znormalizowaną konfigurację z portami i zmiennymi środowiskowymi uzupełnionymi na podstawie manifestów.
        Konfiguracja wejściowa zostaje bez zmian.
        """
        target_ports = self._fill_default_ports()
        target_envs = self._fill_default_envs()

        config_file = self.config_file.model_dump()
        config_file["ports"] = target_ports
        config_file["envs"] = target_envs

        logger.debug(config_file)

        return NormalizedConfig.model_validate(config_file)
