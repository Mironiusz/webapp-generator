from config.logger import get_logger

logger = get_logger(__name__)


class Core:
    def __init__(self):
        print("Core created")

    def _run_config(self):
        print("[mock] Config loaded")

    def _run_normalizer(self):
        print("[mock] Config normalized")

    def _run_validator(self):
        print("[mock] Config validated")

    def _run_pipeline(self):
        print("[mock] Pipeline ran")

    def _pass_result(self):
        print("[mock] Result project passed")

    def _show_stats(self):
        print("[mock] Stats shown")

    def run_generator(self):
        self._run_config()
        self._run_normalizer()
        self._run_validator()
        self._run_pipeline()
        self._pass_result()
        self._show_stats()
