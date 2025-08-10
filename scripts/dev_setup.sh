#!/bin/bash
set -euo pipefail

echo "🚀 Setting up development environment..."

# Check Python version
PYTHON_VERSION=$(python3 --version 2>/dev/null || echo "Python not found")
echo "Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📈 Upgrading pip..."
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "📋 Installing requirements..."
    pip install -r requirements.txt
else
    echo "⚠️  requirements.txt not found, installing basic dependencies..."
    pip install fastapi uvicorn[standard] pydantic pydantic-settings python-multipart
fi

# Print installed versions
echo ""
echo "✅ Setup complete! Installed versions:"
echo "Python: $(python --version)"
echo "FastAPI: $(python -c 'import fastapi; print(fastapi.__version__)' 2>/dev/null || echo 'Not installed')"
echo "Pydantic: $(python -c 'import pydantic; print(pydantic.__version__)' 2>/dev/null || echo 'Not installed')"
echo "Uvicorn: $(python -c 'import uvicorn; print(uvicorn.__version__)' 2>/dev/null || echo 'Not installed')"

echo ""
echo "🎉 Development environment ready!"
echo "To start the server, run: make run"
echo "Or directly: source venv/bin/activate && uvicorn backend.app.main:app --reload"