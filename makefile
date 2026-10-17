.PHONY: install lint lint-python lint-docs format typecheck test coverage deadcode deps security audit check run

PYTHON ?= python

install:
	$(PYTHON) -m pip install -e ".[dev]"

lint: lint-python lint-docs

lint-python:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .

lint-docs:
	npx --no-install prettier --check "**/*.md"

format:
	$(PYTHON) -m ruff format .
	$(PYTHON) -m ruff check --fix .
	npx --no-install prettier --write "**/*.md"

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
	$(PYTHON) -m bandit -r generator main.py

audit:
	$(PYTHON) -m pip_audit

check: lint typecheck deadcode deps security audit test

run:
	$(PYTHON) main.py
