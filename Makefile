.PHONY: install run dev lint format test check export clean refresh help

# Default target
help:
	@echo "Available commands:"
	@echo "  install  - Install dependencies using Poetry"
	@echo "  run      - Run the FastAPI server in production mode"
	@echo "  dev      - Run the FastAPI server in development mode with auto-reload"
	@echo "  lint     - Run linting (ruff)"
	@echo "  format   - Format code (black, isort)"
	@echo "  test     - Run tests (pytest)"
	@echo "  check    - Run all checks (lint + test)"
	@echo "  export   - Export requirements.txt from Poetry"
	@echo "  clean    - Clean up cache and temporary files"
	@echo "  refresh  - Clean install (clean + install)"

install:
	@echo "Installing dependencies with Poetry..."
	poetry install

run:
	@echo "Starting FastAPI server (production mode)..."
	poetry run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

dev:
	@echo "Starting FastAPI server (development mode with auto-reload)..."
	poetry run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

lint:
	@echo "Running linting..."
	poetry run ruff check .
	poetry run mypy backend/ || true

format:
	@echo "Formatting code..."
	poetry run black .
	poetry run isort .
	poetry run ruff check --fix .

test:
	@echo "Running tests..."
	poetry run pytest

check: lint test
	@echo "All checks completed."

export:
	@echo "Exporting requirements.txt..."
	poetry export -f requirements.txt --output requirements.txt --without-hashes

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true

refresh: clean install
	@echo "Refresh completed."