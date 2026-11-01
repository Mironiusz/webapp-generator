from collections.abc import Mapping
from pathlib import Path

from generator.common.schema import EnvName, EnvValue, Port, ProjectRealm
from generator.registry.schema import Manifest


class GenerationPlan:
    """Schemat planu generacji"""

    project_dir: Path
    frontend_template_pack: Manifest
    backend_template_pack: Manifest
    ports: Mapping[ProjectRealm, Port]
    envs: Mapping[ProjectRealm, Mapping[EnvName, EnvValue]]
