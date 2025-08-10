#!/bin/bash
set -e

echo "🚀 Setting up greg-mvp development environment..."

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "📦 Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "📋 Poetry version:"
poetry --version

echo "🔧 Installing dependencies with Poetry..."
poetry install

echo "✅ Development environment setup complete!"
echo ""
echo "To start the server:"
echo "  make run"
echo ""
echo "To run in development mode with auto-reload:"
echo "  make dev"