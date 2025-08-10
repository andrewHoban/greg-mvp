from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_query_prepare_with_revenue_question():
    """Test that revenue questions return deterministic revenue SQL."""
    request_data = {
        "question": "What is our total revenue this year?",
        "context": "Looking for annual revenue data"
    }

    response = client.post("/query/prepare", json=request_data)

    assert response.status_code == 200

    data = response.json()

    # Check that response has required fields
    assert "proposed_sql" in data
    assert "explanation" in data
    assert "referenced_domains" in data
    assert "confidence_score" in data

    # Check that revenue question generates SQL with SUM and total_revenue
    sql = data["proposed_sql"]
    assert "SUM" in sql, "Revenue query should contain SUM function"
    assert "total_revenue" in sql, "Revenue query should reference total_revenue"

    # Check that it references financials domain
    assert "financials" in data["referenced_domains"]

    # Check confidence score is reasonable
    assert 0.0 <= data["confidence_score"] <= 1.0


def test_query_prepare_with_non_revenue_question():
    """Test that non-revenue questions return simple SQL."""
    request_data = {
        "question": "Show me some test data"
    }

    response = client.post("/query/prepare", json=request_data)

    assert response.status_code == 200

    data = response.json()

    # Should get simple SELECT 1 query for non-revenue questions
    assert "SELECT 1" in data["proposed_sql"]
    assert data["referenced_domains"] == []


def test_query_prepare_response_structure():
    """Test that the query prepare endpoint returns the expected structure."""
    request_data = {
        "question": "Test question"
    }

    response = client.post("/query/prepare", json=request_data)

    assert response.status_code == 200

    data = response.json()
    required_fields = ["proposed_sql", "explanation", "referenced_domains", "confidence_score"]

    for field in required_fields:
        assert field in data, f"Missing required field: {field}"

    # Check types
    assert isinstance(data["proposed_sql"], str)
    assert isinstance(data["explanation"], str)
    assert isinstance(data["referenced_domains"], list)
    assert isinstance(data["confidence_score"], (int, float))
