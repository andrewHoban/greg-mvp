.PHONY: install run dev lint format test check export clean refresh

install:
	poetry install

run:
	poetry run uvicorn backend.app.main:app --host 127.0.0.1 --port 8000

dev:
	poetry run uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

lint:
	poetry run ruff check .
	poetry run mypy backend/

format:
	poetry run black .
	poetry run isort .
	poetry run ruff check --fix .

test:
	poetry run pytest -v

check:
	poetry run ruff check .
	poetry run mypy backend/
	poetry run pytest -v

export:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

refresh: clean
	poetry install
	make format
	make check