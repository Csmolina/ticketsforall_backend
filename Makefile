create-venv:
	python3 -m venv .venv

activate-venv:
	source .venv/bin/activate

install-dependencies:
	poetry install --with dev --no-root

activate-pre-commit:
	pre-commit install

run-lint:
	poetry run autoflake --remove-all-unused-imports --remove-unused-variables --recursive --in-place . --exclude=__init__.py,venv,.ven,conftest.py
	poetry run flake8
	black adapters api core factories infrastructure --check

run-tests:
	poetry run pytest

start-app-first-time:
	docker compose up --build