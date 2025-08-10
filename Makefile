.PHONY: install run dev lint format test check export clean refresh

install:
	poetry install

run:
	poetry run uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

dev:
	APP_ENV=dev poetry run uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

lint:
	poetry run ruff check .

format:
	poetry run ruff check --fix . && poetry run black . && poetry run isort .

test:
	poetry run pytest -q

check: lint test
	@echo "Running mypy (optional)..."
	-poetry run mypy backend/ || echo "mypy check completed with warnings/errors"

export:
	poetry export -f requirements.txt --without-hashes -o requirements.txt

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .mypy_cache .pytest_cache

refresh: clean install