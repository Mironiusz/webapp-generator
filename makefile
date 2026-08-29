.PHONY: install lint format typecheck test coverage deadcode deps security audit check run

PYTHON ?= python

install:
	pip install -e ".[dev]"

lint:
	ruff check .
	ruff format --check .

format:
	ruff format .
	ruff check --fix .

typecheck:
	mypy

test:
	pytest

coverage:
	pytest --cov --cov-report=term-missing

deadcode:
	vulture

deps:
	deptry .

security:
	bandit -r config core main.py

audit:
	pip-audit

check: lint typecheck deadcode deps security audit test
