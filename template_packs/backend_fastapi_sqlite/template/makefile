.PHONY: install lint format typecheck test check run migrate

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

check: lint typecheck test

run:
	$(PYTHON) -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

migrate:
	alembic upgrade head
