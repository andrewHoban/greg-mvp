#!/bin/bash

# scripts/dev_bootstrap.sh - Development environment bootstrap script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Poetry is installed
check_poetry() {
    if ! command -v poetry &> /dev/null; then
        print_warning "Poetry not found. Installing Poetry..."
        curl -sSL https://install.python-poetry.org | python3 - || {
            print_warning "Failed to install via official installer. Trying pip..."
            pip3 install --user poetry
        }
        export PATH="$HOME/.local/bin:$PATH"
        if ! command -v poetry &> /dev/null; then
            print_error "Poetry installation failed. Please install Poetry manually."
            exit 1
        fi
    fi
    print_status "Poetry is available: $(poetry --version)"
}

# Install dependencies
install_dependencies() {
    print_status "Installing project dependencies..."
    poetry install
    print_status "Dependencies installed successfully!"
}

# Start the server (optional)
start_server() {
    if [[ "$1" != "--no-run" ]]; then
        print_status "Starting development server..."
        print_status "Server will be available at http://127.0.0.1:8000"
        print_status "Use Ctrl+C to stop the server"
        poetry run uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
    else
        print_status "Skipping server start (--no-run flag provided)"
        print_status "To start the server manually, run: make run"
    fi
}

# Main execution
main() {
    print_status "Starting development environment bootstrap..."
    
    # Check if we're in the right directory
    if [[ ! -f "pyproject.toml" ]]; then
        print_error "pyproject.toml not found. Please run this script from the project root."
        exit 1
    fi
    
    check_poetry
    install_dependencies
    
    print_status "Environment setup complete!"
    print_status "Available commands:"
    print_status "  make run    - Start the development server"
    print_status "  make dev    - Start with APP_ENV=dev"
    print_status "  make test   - Run tests"
    print_status "  make lint   - Run linting"
    print_status "  make format - Format code"
    
    start_server "$@"
}

# Run main function with all arguments
main "$@"