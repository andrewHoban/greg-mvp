"""Test main application."""

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient) -> None:
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "Greg MVP" in data["message"]


def test_docs_endpoint(client: TestClient) -> None:
    """Test docs endpoint is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema(client: TestClient) -> None:
    """Test OpenAPI schema is accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert schema["info"]["title"] == "Greg MVP - AI Product Manager Assistant"
