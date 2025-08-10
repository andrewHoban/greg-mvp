"""
Test the health endpoint
"""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test that the health endpoint returns OK status."""
    response = client.get("/health/")
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data
    assert "version" in data


def test_health_endpoint_structure():
    """Test the structure of health endpoint response."""
    response = client.get("/health/")
    
    data = response.json()
    expected_keys = {"status", "service", "version"}
    
    assert set(data.keys()) == expected_keys
    assert data["service"] == "greg-mvp-backend"
    assert data["version"] == "0.1.0"