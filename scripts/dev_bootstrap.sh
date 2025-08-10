#!/bin/bash
set -e

echo "🚀 Greg MVP Development Bootstrap"
echo "================================="

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "📦 Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Add Poetry to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    
    echo "✅ Poetry installed successfully!"
else
    echo "✅ Poetry already installed"
fi

# Verify Poetry is accessible
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry not found in PATH. Please restart your shell or run:"
    echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
    exit 1
fi

# Install dependencies
echo "📚 Installing dependencies..."
poetry install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔧 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file. Please update it with your actual configuration values."
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Bootstrap complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your configuration"
echo "2. Run 'make run' to start the server"
echo "3. Visit http://localhost:8000/health to verify it's working"
echo "4. View API docs at http://localhost:8000/docs"
echo ""
echo "Available commands:"
echo "  make install  - Install dependencies"
echo "  make run      - Run production server"
echo "  make dev      - Run development server with auto-reload"
echo "  make test     - Run tests"
echo "  make lint     - Run linting"
echo "  make format   - Format code"
echo ""

# Start the development server
echo "🏁 Starting development server..."
poetry run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload