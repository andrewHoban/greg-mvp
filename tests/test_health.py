"""Tests for health endpoint."""

from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient):
    """Test that the health endpoint returns correct status."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert data["status"] == "ok"
    assert "version" in data
    assert "timestamp" in data


def test_health_endpoint_structure(client: TestClient):
    """Test that the health endpoint returns expected JSON structure."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    # Check all required fields are present
    required_fields = ["status", "version", "timestamp"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"

    # Check data types
    assert isinstance(data["status"], str)
    assert isinstance(data["version"], str)
    assert isinstance(data["timestamp"], str)
