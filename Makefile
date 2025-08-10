.PHONY: install run test lint

install:
	poetry install

run:
	poetry run uvicorn backend.app.main:app --reload

test:
	poetry run pytest -q

lint:
	poetry run ruff check .

type:
	poetry run mypy backend
