.PHONY: install run dev lint format test check export clean refresh help

# Default target
help:
	@echo "Available targets:"
	@echo "  install  - Install dependencies via Poetry"
	@echo "  run      - Run the FastAPI application in production mode"
	@echo "  dev      - Run the FastAPI application in development mode with hot reload"
	@echo "  lint     - Run linting with ruff"
	@echo "  format   - Format code with black and isort"
	@echo "  test     - Run tests with pytest"
	@echo "  check    - Run lint, format check, and tests"
	@echo "  export   - Export requirements.txt from Poetry lock"
	@echo "  clean    - Clean up cache and temporary files"
	@echo "  refresh  - Clean and reinstall dependencies"

install:
	@echo "Installing dependencies with Poetry..."
	poetry install

run:
	@echo "Running FastAPI application..."
	poetry run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

dev:
	@echo "Running FastAPI application in development mode..."
	poetry run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

lint:
	@echo "Running ruff linter..."
	poetry run ruff check .

format:
	@echo "Formatting code with black and isort..."
	poetry run black .
	poetry run isort .

test:
	@echo "Running tests with pytest..."
	poetry run pytest -v

check: lint test
	@echo "Running format check..."
	poetry run black --check .
	poetry run isort --check-only .
	@echo "All checks passed!"

export:
	@echo "Exporting requirements.txt..."
	poetry export -f requirements.txt --output requirements.txt

clean:
	@echo "Cleaning up cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -f .coverage
	rm -f requirements.txt

refresh: clean
	@echo "Refreshing dependencies..."
	poetry install --sync