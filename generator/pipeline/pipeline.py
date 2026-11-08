from collections.abc import Callable
from typing import Self

from generator.planning.schema import GenerationPlan
from generator.settings.logger import get_logger

logger = get_logger(__name__)


class Pipeline:
    """
    Pipeline jest stałą listą kroków wykonywanych po kolei. Kroki dostają parametry z planu generacji. Decyzja, czy przejść dalej, podejmowana jest przez core.
    Odpowiedzialności pipeline'u:

    - definicja listy kroków
    - wykonywanie poszczególnych kroków
    - zwracanie wyniku kroku do core

    Pipeline wykonuje też krok finalizacji, ale decyzja, czy do niego dojść, należy do core.

    Kroki pipeline'u:
    1. Utworzenie katalogu stagingu i zapis śladu runa.
    2. Skopiowanie plików całościowych z template packów.
    3. Zapis plików .env z wartościami ze znormalizowanej konfiguracji, podmiana tokenów portów w .env.local.example i utworzenie .env.local.
    4. Złożenie plików składanych z contributions i zapis stałego .gitignore w roocie projektu.
    5. Zbudowanie obrazów przez Docker Compose.
    6. Uruchomienie projektu przez Docker Compose.
    7. Sprawdzenie, czy jednorazowe usługi inicjalizujące zakończyły się kodem 0, a backend osiągnął stan healthy.
    8. Uruchomienie testów kontraktu HTTP API na działającym backendzie.
    9. Uruchomienie testów frontendu i backendu.
    10. Uruchomienie testu happy path.
    11. Zatrzymanie projektu i usunięcie jego zasobów Dockera.
    12. Kopia projektu do katalogu tymczasowego w katalogu docelowym.
    13. Zmiana nazwy kopii na katalog projektu.
    14. Usunięcie katalogu stagingu.
    """

    def __init__(self, generation_plan: GenerationPlan):
        self.generation_plan = generation_plan
        self.pipeline_register: list[Callable[..., bool]] = []
        self.current_step = 0
        self.max_step: int
        self._init_register()

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> bool:
        if self.current_step >= self.max_step:
            raise StopIteration

        status = self.pipeline_register[self.current_step]()
        self.current_step += 1

        return status

    def _init_register(self) -> None:
        self.pipeline_register.append(self._step_1_create_staging)
        self.pipeline_register.append(self._step_2_render_full_files)
        self.pipeline_register.append(self._step_3_handle_env_files)
        self.pipeline_register.append(self._step_4_compose_contribution_files)
        self.pipeline_register.append(self._step_5_build_images)
        self.pipeline_register.append(self._step_6_start_project)
        self.pipeline_register.append(self._step_7_check_services_health)
        self.pipeline_register.append(self._step_8_run_api_contract_tests)
        self.pipeline_register.append(self._step_9_run_project_tests)
        self.pipeline_register.append(self._step_10_run_happy_path_test)
        self.pipeline_register.append(self._step_11_stop_project)
        self.pipeline_register.append(self._step_12_copy_to_temp_dir)
        self.pipeline_register.append(self._step_13_rename_to_project_dir)
        self.pipeline_register.append(self._step_14_remove_staging)
        self.max_step = len(self.pipeline_register)

    def _step_1_create_staging(self) -> bool:
        """
        Utworzenie katalogu stagingu i zapis śladu runa. Po potwierdzeniu, że katalog stagingu powstał, zostają tam zapisane
        dane potrzebne do cleanupu: nazwę projektu Docker Compose runa i ścieżkę kopii tymczasowej. Jeśli proces zostanie zabity,
        cleanup się nie wykona. Wtedy kolejne uruchomienie generatora najpierw sprząta po poprzednich runach na podstawie ich śladów,
        a dopiero potem zaczyna nowy run.
        """
        logger.info("Creating staging directory with run trace")
        return True

    def _step_2_render_full_files(self) -> bool:
        """
        Skopiowanie plików całościowych z template packów.
        """
        logger.info("Rendering full files from template packs")
        return True

    def _step_3_handle_env_files(self) -> bool:
        """
        Zapis plików .env z wartościami ze znormalizowanej konfiguracji, podmiana tokenów portów w .env.local.example i utworzenie .env.local.
        """
        logger.info("Saving .env files with config values, setting ports, creating .env.local")
        return True

    def _step_4_compose_contribution_files(self) -> bool:
        """
        Złożenie plików składanych z contributions i zapis stałego .gitignore w roocie projektu.
        """
        logger.info("Composing files from contributions, saving .gitignore")
        return True

    def _step_5_build_images(self) -> bool:
        """
        Zbudowanie obrazów przez Docker Compose.
        """
        logger.info("Building images with Docker Compose")
        return True

    def _step_6_start_project(self) -> bool:
        """
        Uruchomienie projektu przez Docker Compose.
        """
        logger.info("Starting project with Docker Compose")
        return True

    def _step_7_check_services_health(self) -> bool:
        """
        Sprawdzenie, czy jednorazowe usługi inicjalizujące zakończyły się kodem 0, a backend osiągnął stan healthy.
        """
        logger.info("Checking init services exit codes and backend health")
        return True

    def _step_8_run_api_contract_tests(self) -> bool:
        """
        Uruchomienie testów kontraktu HTTP API na działającym backendzie.
        """
        logger.info("Running HTTP API contract tests")
        return True

    def _step_9_run_project_tests(self) -> bool:
        """
        Uruchomienie testów frontendu i backendu.
        """
        logger.info("Running frontend and backend tests")
        return True

    def _step_10_run_happy_path_test(self) -> bool:
        """
        Uruchomienie testu happy path.
        """
        logger.info("Running happy path test")
        return True

    def _step_11_stop_project(self) -> bool:
        """
        Zatrzymanie projektu i usunięcie jego zasobów Dockera.
        """
        logger.info("Stopping project and removing its Docker resources")
        return True

    def _step_12_copy_to_temp_dir(self) -> bool:
        """
        Kopia projektu do katalogu tymczasowego w katalogu docelowym.
        """
        logger.info("Copying project to temporary directory in output directory")
        return True

    def _step_13_rename_to_project_dir(self) -> bool:
        """
        Zmiana nazwy kopii na katalog projektu.
        """
        logger.info("Renaming copy to project directory")
        return True

    def _step_14_remove_staging(self) -> bool:
        """
        Usunięcie katalogu stagingu.
        """
        logger.info("Removing staging directory")
        return True
