"""Test configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import create_app
from backend.app.services.knowledge_base import KnowledgeBase


@pytest.fixture
def app():
    """Create FastAPI app for testing."""
    app = create_app()
    # Initialize knowledge base for testing
    knowledge_base = KnowledgeBase()
    knowledge_base.load_domains()
    app.state.knowledge_base = knowledge_base
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)
