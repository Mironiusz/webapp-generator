import errno
import os
import socket
import sys
import tempfile
from collections import Counter
from pathlib import Path

from generator.common.errors import InvalidConfigurationError
from generator.configuration.schema import NormalizedConfig
from generator.settings.logger import get_logger

logger = get_logger(__name__)

PORT_UNAVAILABLE_ERRNOS = frozenset({errno.EADDRINUSE, errno.EACCES})
WILDCARD_ADDRESSES = ((socket.AF_INET, "0.0.0.0"), (socket.AF_INET6, "::"))


class Validator:
    """
    Tutaj konfiguracja zostaje zwalidowana.
    Obejmuje:
    - sprawdzenie, czy porty znormalizowanej konfiguracji nie mają konfliktów
    - sprawdzenie, czy porty nie są zajęte przez inne procesy
    - sprawdzenie, czy katalog docelowy istnieje i pozwala na zapis, a katalog projektu nie istnieje albo jest pusty
    """

    def __init__(self, normalized_config: NormalizedConfig):
        self.normalized_config = normalized_config

    def _check_port_conflicts(self) -> None:
        """Sprawdza, czy porty znormalizowanej konfiguracji nie mają konfliktów."""
        ports = self.normalized_config.ports
        duplicated_ports = [str(port) for port, count in Counter(ports.values()).items() if count > 1]

        if duplicated_ports:
            raise InvalidConfigurationError(f"The following ports are duplicated in your configuration: {', '.join(duplicated_ports)}")

    def _is_port_free(self, port: int) -> bool:
        """Sprawdza, czy port jest wolny."""

        def _can_bind(family: socket.AddressFamily, host: str, port: int) -> bool:
            """
            Sprawdza, czy port da się zająć na adresie wildcard danej rodziny adresów.
            Na Windowsie bind idzie z SO_EXCLUSIVEADDRUSE, bo bez niej przechodzi obok procesu słuchającego na konkretnym adresie.
            Na pozostałych systemach bind idzie z SO_REUSEADDR, bo bez niej blokują go zamknięte połączenia w TIME_WAIT.
            System bez obsługi danej rodziny adresów nie może mieć na niej zajętego portu.
            """
            try:
                with socket.socket(family, socket.SOCK_STREAM) as sock:
                    if sys.platform == "win32":
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
                    else:
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.bind((host, port))
            except OSError as e:
                if e.errno in PORT_UNAVAILABLE_ERRNOS:
                    return False
                if e.errno == errno.EAFNOSUPPORT:
                    return True
                raise

            return True

        return all(_can_bind(family, host, port) for family, host in WILDCARD_ADDRESSES)

    def _check_ports_availability(self) -> None:
        """Sprawdza, czy podane w konfiguracji porty są aktualnie dostępne."""
        ports = self.normalized_config.ports
        for port in ports.values():
            if not self._is_port_free(port):
                raise InvalidConfigurationError(f"Port {port} is not available")

    def _is_dir_writeable(self, path: Path) -> bool:
        """Sprawdza, czy w katalogu docelowym da się utworzyć katalog, tworząc i usuwając katalog tymczasowy."""
        try:
            with tempfile.TemporaryDirectory(dir=path):
                pass
        except OSError:
            return False

        return True

    def _check_target_dir(self) -> None:
        """Sprawdza, czy katalog docelowy istnieje i pozwala na zapis."""
        target_dir = self.normalized_config.project.output_dir

        if os.path.lexists(target_dir) and not os.path.isdir(target_dir):
            raise InvalidConfigurationError(f"Target path {target_dir} exists but is not a directory")

        if not os.path.isdir(target_dir):
            raise InvalidConfigurationError(f"Target directory {target_dir} in your configuration does not exist")

        if not self._is_dir_writeable(target_dir):
            raise InvalidConfigurationError(f"You do not have write permissions to create your project in {target_dir}")

    def _check_project_dir(self) -> None:
        """Sprawdza, czy katalog projektu nie istnieje albo jest pusty."""
        project_dir = self.normalized_config.project.output_dir / self.normalized_config.project.name
        logger.debug("Project dir: %s", project_dir)

        if os.path.lexists(project_dir) and not os.path.isdir(project_dir):
            raise InvalidConfigurationError(f"Project path {project_dir} exists but is not a directory")

        if os.path.isdir(project_dir) and any(project_dir.iterdir()):
            raise InvalidConfigurationError(f"Your project directory {project_dir} is not empty")

    def run_validation(self) -> None:
        self._check_port_conflicts()
        self._check_ports_availability()
        self._check_target_dir()
        self._check_project_dir()
