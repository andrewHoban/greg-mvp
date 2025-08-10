"""
Test the query preparation endpoint
"""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_query_prepare_endpoint():
    """Test that the query prepare endpoint returns deterministic results."""
    request_data = {
        "question": "What was the total revenue last quarter?"
    }
    
    response = client.post("/query/prepare", json=request_data)
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Check required fields are present
    assert "proposed_sql" in data
    assert "explanation" in data
    assert "referenced_domains" in data
    
    # Check data types and non-empty values
    assert isinstance(data["proposed_sql"], str)
    assert len(data["proposed_sql"]) > 0
    
    assert isinstance(data["explanation"], str)
    assert len(data["explanation"]) > 0
    
    assert isinstance(data["referenced_domains"], list)
    assert len(data["referenced_domains"]) > 0


def test_query_prepare_deterministic():
    """Test that the query prepare endpoint returns consistent results."""
    request_data = {
        "question": "Show me revenue trends"
    }
    
    # Make the same request twice
    response1 = client.post("/query/prepare", json=request_data)
    response2 = client.post("/query/prepare", json=request_data)
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    data1 = response1.json()
    data2 = response2.json()
    
    # Results should be identical for deterministic stub
    assert data1["proposed_sql"] == data2["proposed_sql"]
    assert data1["explanation"] == data2["explanation"]
    assert data1["referenced_domains"] == data2["referenced_domains"]


def test_query_prepare_sql_structure():
    """Test that the returned SQL has expected structure."""
    request_data = {
        "question": "Any revenue question"
    }
    
    response = client.post("/query/prepare", json=request_data)
    
    assert response.status_code == 200
    
    data = response.json()
    sql = data["proposed_sql"].upper()
    
    # Check for basic SQL structure
    assert "SELECT" in sql
    assert "FROM" in sql
    assert "FINANCIALS_TRANSACTIONS" in sql
    
    # Check that referenced domains match SQL content
    assert "financials" in data["referenced_domains"]


def test_query_prepare_invalid_input():
    """Test query prepare with invalid input."""
    request_data = {
        "question": ""  # Empty question
    }
    
    response = client.post("/query/prepare", json=request_data)
    
    # Should return validation error
    assert response.status_code == 422


def test_query_prepare_missing_field():
    """Test query prepare with missing required field."""
    request_data = {}  # Missing question field
    
    response = client.post("/query/prepare", json=request_data)
    
    # Should return validation error
    assert response.status_code == 422