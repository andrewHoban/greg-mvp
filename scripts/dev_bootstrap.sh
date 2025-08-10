#!/bin/bash
set -e

echo "🚀 Greg MVP Development Bootstrap"
echo "================================"

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "📦 Poetry not found. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Add Poetry to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    
    echo "✅ Poetry installed successfully"
else
    echo "✅ Poetry is already installed"
fi

# Install project dependencies
echo "📦 Installing project dependencies..."
poetry install

echo "✅ Dependencies installed successfully"

# Check if --no-run flag is provided
if [[ "$1" != "--no-run" ]]; then
    echo "🚀 Starting development server..."
    echo "Server will be available at http://127.0.0.1:8000"
    echo "Press Ctrl+C to stop the server"
    poetry run uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
else
    echo "🎉 Bootstrap complete! Run 'make dev' to start the development server."
fi