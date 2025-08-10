"""Test visualization endpoint."""

from fastapi.testclient import TestClient


def test_visualization_suggestions_endpoint(client: TestClient) -> None:
    """Test visualization suggestions endpoint."""
    request_data = {
        "query": "SELECT country, COUNT(*) FROM users GROUP BY country",
    }
    response = client.post("/api/visualization-suggestions", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)
    assert len(data["suggestions"]) > 0

    # Check structure of first suggestion
    suggestion = data["suggestions"][0]
    assert "type" in suggestion
    assert "title" in suggestion
    assert "description" in suggestion
    assert "confidence" in suggestion
    assert 0.0 <= suggestion["confidence"] <= 1.0


def test_visualization_suggestions_time_series(client: TestClient) -> None:
    """Test visualization suggestions for time series data."""
    request_data = {
        "query": "SELECT date, revenue FROM sales WHERE date > '2024-01-01'",
    }
    response = client.post("/api/visualization-suggestions", json=request_data)
    assert response.status_code == 200

    data = response.json()
    suggestions = data["suggestions"]

    # Should suggest line chart for time series
    suggestion_types = [s["type"] for s in suggestions]
    assert "line_chart" in suggestion_types
