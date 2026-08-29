.PHONY: install lint format typecheck test coverage deadcode deps security audit check run

PYTHON ?= python

install:
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .

format:
	$(PYTHON) -m ruff format .
	$(PYTHON) -m ruff check --fix .

typecheck:
	$(PYTHON) -m mypy

test:
	$(PYTHON) -m pytest

coverage:
	$(PYTHON) -m pytest --cov --cov-report=term-missing

deadcode:
	$(PYTHON) -m vulture

deps:
	$(PYTHON) -m deptry .

security:
	$(PYTHON) -m bandit -r config core main.py

audit:
	$(PYTHON) -m pip_audit

check: lint typecheck deadcode deps security audit test

run:
	$(PYTHON) main.py
