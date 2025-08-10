"""Tests for query endpoints."""

from fastapi.testclient import TestClient


def test_query_prepare_endpoint(client: TestClient):
    """Test that the query prepare endpoint returns correct structure."""
    request_data = {"question": "What was our total revenue last month?"}

    response = client.post("/query/prepare", json=request_data)

    assert response.status_code == 200
    data = response.json()

    # Check all required fields are present
    required_fields = ["proposed_sql", "explanation", "referenced_domains"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"

    # Check data types
    assert isinstance(data["proposed_sql"], str)
    assert isinstance(data["explanation"], str)
    assert isinstance(data["referenced_domains"], list)

    # Check content makes sense
    assert len(data["proposed_sql"]) > 0
    assert len(data["explanation"]) > 0


def test_query_prepare_revenue_question(client: TestClient):
    """Test that revenue questions generate expected SQL."""
    request_data = {"question": "Show me monthly revenue trends"}

    response = client.post("/query/prepare", json=request_data)

    assert response.status_code == 200
    data = response.json()

    # Should contain the deterministic SQL from requirements
    sql = data["proposed_sql"].lower()
    assert "select" in sql
    assert "date_trunc" in sql
    assert "sum(amount)" in sql
    assert "financials_transactions" in sql
    assert "group by" in sql


def test_query_prepare_validation(client: TestClient):
    """Test that query prepare validates input."""
    # Empty question should fail
    response = client.post("/query/prepare", json={"question": ""})
    assert response.status_code == 422  # Validation error

    # Missing question should fail
    response = client.post("/query/prepare", json={})
    assert response.status_code == 422  # Validation error


def test_query_execute_endpoint(client: TestClient):
    """Test that the query execute endpoint returns correct structure."""
    request_data = {
        "sql": "SELECT * FROM financials_transactions LIMIT 10",
        "limit": 10,
    }

    response = client.post("/query/execute", json=request_data)

    assert response.status_code == 200
    data = response.json()

    # Check all required fields are present
    required_fields = ["data", "row_count", "warning"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"

    # Check data types
    assert isinstance(data["data"], list)
    assert isinstance(data["row_count"], int)
    assert data["warning"] is None or isinstance(data["warning"], str)

    # Should have warning about stub implementation
    assert data["warning"] is not None
    assert "synthetic" in data["warning"].lower()


def test_query_execute_validation(client: TestClient):
    """Test that query execute validates input."""
    # Empty SQL should fail
    response = client.post("/query/execute", json={"sql": ""})
    assert response.status_code == 422  # Validation error

    # Missing SQL should fail
    response = client.post("/query/execute", json={})
    assert response.status_code == 422  # Validation error

    # Invalid limit should fail
    response = client.post("/query/execute", json={"sql": "SELECT 1", "limit": 0})
    assert response.status_code == 422  # Validation error

    response = client.post("/query/execute", json={"sql": "SELECT 1", "limit": 1001})
    assert response.status_code == 422  # Validation error
