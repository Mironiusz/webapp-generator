from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def fake_template_packs(monkeypatch) -> Path:
    """Patchuje ścieżkę do template packów ścieżką do testowych template packów."""
    fake_path = Path(__file__).resolve().parents[1] / "data" / "template_packs"
    monkeypatch.setattr("generator.registry.resolver.TEMPLATE_PACKS_PATH", fake_path)
    return fake_path
