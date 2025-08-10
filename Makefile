.PHONY: install run dev lint format test check export clean refresh

# Install dependencies
install:
	poetry install

# Run the application in production mode
run:
	poetry run uvicorn backend.app.main:app --host 127.0.0.1 --port 8000

# Run the application in development mode with auto-reload
dev:
	poetry run uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

# Lint code with ruff
lint:
	poetry run ruff check .

# Format code with black and isort
format:
	poetry run black .
	poetry run isort .
	poetry run ruff --fix .

# Run tests
test:
	poetry run pytest -q

# Run all checks (lint, format check, type check, tests)
check:
	poetry run ruff check .
	poetry run black --check .
	poetry run isort --check-only .
	poetry run mypy backend/
	poetry run pytest -q

# Export requirements.txt for deployment
export:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

# Clean build artifacts and cache
clean:
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

# Refresh: clean, install, and test
refresh: clean install test