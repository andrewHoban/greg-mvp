"""Test knowledge endpoint."""

from fastapi.testclient import TestClient


def test_knowledge_endpoint(client: TestClient) -> None:
    """Test knowledge base endpoint."""
    response = client.get("/api/knowledge")
    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "per_page" in data
    assert isinstance(data["items"], list)


def test_knowledge_endpoint_with_pagination(client: TestClient) -> None:
    """Test knowledge base endpoint with pagination."""
    response = client.get("/api/knowledge?page=1&per_page=5")
    assert response.status_code == 200

    data = response.json()
    assert data["page"] == 1
    assert data["per_page"] == 5


def test_knowledge_endpoint_with_category_filter(client: TestClient) -> None:
    """Test knowledge base endpoint with category filter."""
    response = client.get("/api/knowledge?category=sql")
    assert response.status_code == 200

    data = response.json()
    # All returned items should have the filtered category
    for item in data["items"]:
        assert item["category"] == "sql"
