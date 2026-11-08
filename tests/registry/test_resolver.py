import logging
from pathlib import Path

import pytest

from generator.registry.resolver import Resolver


def test_get_pack_dirs_returns_dirs_with_manifest(fake_template_packs):
    """Sprawdza, czy get_pack_dirs() zwraca słownik nazwa katalogu -> katalog packa dla każdego katalogu z manifestem."""
    resolver = Resolver()
    fake_pack_dirs = {
        "test_backend": fake_template_packs / "test_backend",
        "test_backend_without_database": fake_template_packs / "test_backend_without_database",
    }

    assert resolver.get_pack_dirs() == fake_pack_dirs


@pytest.mark.usefixtures("fake_template_packs")
def test_get_pack_dirs_skips_entries_without_manifest(caplog):
    """Sprawdza, czy get_pack_dirs() pomija z ostrzeżeniem katalog bez manifest.yaml, a luźny plik w katalogu packów bez ostrzeżenia."""
    resolver = Resolver()
    pack_dirs = resolver.get_pack_dirs()

    assert "test_pack_without_manifest" not in pack_dirs
    assert "random_file.txt" not in pack_dirs
    assert "test_pack_without_manifest is not a valid template pack. manifest.yaml missing." in caplog.text
    assert len([record for record in caplog.records if record.levelno == logging.WARNING]) == 1


def test_get_template_packs_returns_template_pack_for_valid_pack(fake_template_packs):
    """Sprawdza, czy get_template_packs() dla poprawnego packa zwraca TemplatePack z nazwą katalogu, ścieżką do katalogu template i wczytanym manifestem."""
    correct_path_name = "test_backend"
    correct_path = Path("test_backend/template")
    resolver = Resolver()
    template_packs = resolver.get_template_packs()

    assert correct_path_name in template_packs
    correct_pack = template_packs[correct_path_name]
    assert correct_pack.name == correct_path_name
    assert correct_pack.path == fake_template_packs / correct_path
    assert correct_pack.manifest.name == "Test Backend Correct"


def test_get_template_packs_skips_pack_with_missing_part_dir(fake_template_packs, caplog):
    """
    Sprawdza, czy get_template_packs() pomija z ostrzeżeniem pack, którego manifest deklaruje port części bez jej katalogu w template.
    Pozostałe packi z katalogu mają się wczytać normalnie.
    """


def test_get_template_packs_raises_on_invalid_manifest(tmp_path, monkeypatch):
    """
    Sprawdza, czy niepoprawny manifest przerywa tworzenie rejestru błędem InvalidTemplatePackError z nazwą packa.
    Pack z takim manifestem leży w osobnym katalogu packów, bo we wspólnym wywaliłby pozostałe testy resolvera.
    Pack musi mieć katalogi template i contributions, bo bez nich resolver pominie go przed wczytaniem manifestu.
    """
