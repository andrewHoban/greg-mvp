.PHONY: install run test versions lock clean env help

# Use bash shell for all commands
SHELL := /bin/bash

# Default target
help:
	@echo "Available commands:"
	@echo "  install  - Install dependencies and setup virtual environment"
	@echo "  run      - Start the FastAPI development server"
	@echo "  test     - Run tests (if available)"
	@echo "  versions - Show installed package versions"
	@echo "  lock     - Generate requirements.lock file"
	@echo "  clean    - Clean up generated files and cache"
	@echo "  env      - Create .env file from .env.example if missing"

# Install dependencies and setup virtual environment
install:
	@echo "🚀 Setting up development environment..."
	./scripts/dev_setup.sh

# Start the FastAPI development server
run: env
	@echo "🏃 Starting FastAPI development server..."
	@if [ -d "venv" ]; then \
		source venv/bin/activate && uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000; \
	else \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi

# Run tests (placeholder for future implementation)
test:
	@echo "🧪 Running tests..."
	@if [ -d "venv" ]; then \
		echo "No tests configured yet. Add your test command here."; \
	else \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi

# Show installed package versions
versions:
	@echo "📦 Installed package versions:"
	@if [ -d "venv" ]; then \
		source venv/bin/activate && pip list | grep -E "(fastapi|uvicorn|pydantic)"; \
	else \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
	fi

# Generate requirements.lock file with exact versions
lock:
	@echo "🔒 Generating requirements.lock file..."
	@if [ -d "venv" ]; then \
		source venv/bin/activate && pip freeze > requirements.lock; \
		echo "✅ requirements.lock generated"; \
	else \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi

# Clean up generated files and cache
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "*.pyo" -delete 2>/dev/null || true
	find . -name ".coverage" -delete 2>/dev/null || true
	rm -rf .pytest_cache 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Create .env file from .env.example if missing
env:
	@if [ ! -f ".env" ] && [ -f ".env.example" ]; then \
		echo "📄 Creating .env file from .env.example..."; \
		cp .env.example .env; \
		echo "✅ .env file created. Please update with your actual values."; \
	fi