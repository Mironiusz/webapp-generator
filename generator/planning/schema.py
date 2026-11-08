from collections.abc import Mapping
from pathlib import Path

from generator.common.schema import EnvName, EnvValue, Port, ProjectPart, StrictModel
from generator.registry.schema import TemplatePack, TemplatePackType


class GenerationPlan(StrictModel):
    """
    Plan generacji, czyli parametry dla stałej listy kroków pipeline'u.
    Plan określa, skąd pochodzi każdy plik projektu: czy jest kopiowany z template packa, czy składany z contributions.
    """

    project_dir: Path
    frontend_template_pack: TemplatePack
    backend_template_pack: TemplatePack
    full_files: Mapping[ProjectPart, list[Path]]
    contribution_files: Mapping[TemplatePackType, list[Path]]
    ports: Mapping[ProjectPart, Port]
    envs: Mapping[ProjectPart, Mapping[EnvName, EnvValue]]
