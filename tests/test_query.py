"""Test query endpoint."""

from fastapi.testclient import TestClient


def test_query_endpoint(client: TestClient) -> None:
    """Test query processing endpoint."""
    request_data = {"question": "How many users signed up last month?"}
    response = client.post("/api/query", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert "sql" in data
    assert "explanation" in data
    assert "confidence" in data
    assert "suggested_visualizations" in data
    assert 0.0 <= data["confidence"] <= 1.0


def test_query_endpoint_invalid_data(client: TestClient) -> None:
    """Test query endpoint with invalid data."""
    response = client.post("/api/query", json={"question": ""})
    assert response.status_code == 422  # Validation error
