#!/bin/bash
set -e

echo "🚀 Greg MVP Development Bootstrap Script"
echo "========================================="

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "📦 Poetry not found. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
    echo "✅ Poetry installed successfully!"
else
    echo "✅ Poetry is already installed"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔧 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please update it with your actual configuration."
else
    echo "✅ .env file already exists"
fi

# Install dependencies
echo "📦 Installing dependencies..."
poetry install

echo ""
echo "🎉 Bootstrap completed successfully!"
echo ""
echo "To start the development server:"
echo "  make dev"
echo ""
echo "To run tests:"
echo "  make test"
echo ""
echo "To see all available commands:"
echo "  make help"
echo ""
echo "The API will be available at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"