import subprocess
from collections.abc import Mapping
from pathlib import Path

import yaml

from generator.common.schema import ProjectPart
from generator.configuration.schema import NormalizedConfig
from generator.planning.schema import GenerationPlan
from generator.registry.resolver import TEMPLATE_PACK_CONTRIBUTIONS_NAME
from generator.registry.schema import TemplatePack, TemplatePackType
from generator.settings.logger import get_logger

logger = get_logger(__name__)

GIT_COMMAND_BASE = "git -C"
GIT_COMMAND_LIST_FILES = "ls-files -z --cached --others --exclude-standard --"
GIT_COMMAND_LIST_FILES_TO_EXCLUDE = "ls-files -z --deleted --"

EXCLUDED_FULL_FILES = {Path("docker-compose.yml")}


PACK_DIR_DEPTH = 2


class Planner:
    """
    Tutaj powstaje plan generacji.
    Planner przekłada język konfiguracji na docelowy plan wykonania, używający już konkretnych zasobów.
    Ta sama znormalizowana konfiguracja i te same template packi dają zawsze ten sam plan.
    """

    def __init__(self, config: NormalizedConfig, available_packs: dict[str, TemplatePack]) -> None:
        self.config = config
        self.available_packs = available_packs

    def _execute_command(self, target_dir: Path, command_type: str, project_part: ProjectPart | str = "") -> set[Path]:
        """Wykonuje podaną komendę i zwraca zbiór plików wypisanych przez komendę."""
        command = f"{GIT_COMMAND_BASE} {target_dir} {command_type} {project_part}".split()
        result_command = subprocess.run(command, capture_output=True, check=True, encoding="utf-8")
        return {Path(path) for path in result_command.stdout.split("\0") if path}

    def _list_files(self, target_dir: Path, excluded: set[Path] | None = None, project_part: ProjectPart | str = "") -> list[Path]:
        """
        Wywołuje dwie komendy:
        - wypisującą pliki obserwowane przez gita dla odpowiednich części projektu
        - wypisującą tylko usunięte pliki obserwowane przez gita dla odpowiednich części projektu
        Następnie tworzy zbiór plików w podanym katalogu wypisaną przez pierwszą komendę i odejmuje
        od niego zbiór plików wypisanych przez drugą komendę oraz zbiór plików wyłączonych z kopiowania.
        Zwraca ostateczną listę plików ze zbioru.
        """
        excluded_files = {project_part / file for file in excluded} if excluded is not None else set()
        files_to_keep = self._execute_command(target_dir, GIT_COMMAND_LIST_FILES, project_part)
        files_to_exclude = self._execute_command(target_dir, GIT_COMMAND_LIST_FILES_TO_EXCLUDE, project_part)

        return sorted(files_to_keep - files_to_exclude - excluded_files)

    def _get_full_files(self) -> Mapping[ProjectPart, list[Path]]:
        """
        Zbiera pliki całościowe wybranych template packów.
        Plikami całościowymi są pliki z katalogów części, które git śledzi, oraz nowe pliki, których git nie ignoruje, bez plików usuniętych z dysku.
        Lista jest posortowana, żeby plan był zawsze taki sam.
        """
        project_parts_path: dict[ProjectPart, Path] = {}
        project_parts_path[ProjectPart.FRONTEND] = self.available_packs[self.config.frontend].path
        project_parts_path[ProjectPart.BACKEND] = self.available_packs[self.config.backend].path
        if ProjectPart.DATABASE in self.config.ports:
            project_parts_path[ProjectPart.DATABASE] = self.available_packs[self.config.backend].path

        result_file_lists: dict[ProjectPart, list[Path]] = {}
        for project_part, project_part_path in project_parts_path.items():
            result_file_lists[project_part] = self._list_files(project_part_path, EXCLUDED_FULL_FILES, project_part)

        return result_file_lists

    def _get_contribution_files(self) -> Mapping[TemplatePackType, list[Path]]:
        """Zbiera pliki składane w roocie projektu razem z contributions wybranych template packów, z których powstają."""
        template_pack_contributions_dirs: dict[TemplatePackType, Path] = {}
        template_pack_contributions_dirs[TemplatePackType.FRONTEND] = self.available_packs[self.config.frontend].path.parent / TEMPLATE_PACK_CONTRIBUTIONS_NAME
        template_pack_contributions_dirs[TemplatePackType.BACKEND_DB] = self.available_packs[self.config.backend].path.parent / TEMPLATE_PACK_CONTRIBUTIONS_NAME

        result_file_lists: dict[TemplatePackType, list[Path]] = {}
        for template_pack_type, template_pack_contributions_dir in template_pack_contributions_dirs.items():
            result_file_lists[template_pack_type] = self._list_files(template_pack_contributions_dir)

        return result_file_lists

    def create_generation_plan(self) -> GenerationPlan:
        """Buduje plan generacji ze znormalizowanej konfiguracji i wybranych template packów."""

        generation_plan = GenerationPlan(
            project_dir=self.config.project.output_dir / self.config.project.name,
            frontend_template_pack=self.available_packs[self.config.frontend],
            backend_template_pack=self.available_packs[self.config.backend],
            full_files=self._get_full_files(),
            contribution_files=self._get_contribution_files(),
            ports=self.config.ports,
            envs=self.config.envs,
        )

        logger.debug("Generation plan created: \n%s", yaml.dump(generation_plan.model_dump(mode="json"), sort_keys=False, allow_unicode=True))

        return generation_plan
