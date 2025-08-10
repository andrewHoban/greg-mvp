"""
Test the health check endpoint.
"""
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint returns ok status."""
    response = client.get("/health")
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data