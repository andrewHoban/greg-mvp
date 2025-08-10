from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_query_prepare_revenue():
    """Test query preparation for revenue-related questions."""
    response = client.post(
        "/query/prepare",
        json={"question": "What was the total revenue last month?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "proposed_sql" in data
    assert "explanation" in data
    assert "referenced_domains" in data
    assert "financials" in data["referenced_domains"]


def test_query_prepare_users():
    """Test query preparation for user-related questions."""
    response = client.post(
        "/query/prepare", 
        json={"question": "How many users signed up from the USA?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "proposed_sql" in data
    assert "explanation" in data
    assert "referenced_domains" in data


def test_query_execute():
    """Test SQL query execution."""
    response = client.post(
        "/query/execute",
        json={"sql": "SELECT COUNT(*) FROM users", "limit": 100}
    )
    assert response.status_code == 200
    data = response.json()
    assert "columns" in data
    assert "rows" in data
    assert "warning" in data