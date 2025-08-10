from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test that the health endpoint returns OK status."""
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert data["version"] == "0.1.0"


def test_health_endpoint_response_structure():
    """Test that the health endpoint returns the expected response structure."""
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()
    required_fields = ["status", "timestamp", "version"]

    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
