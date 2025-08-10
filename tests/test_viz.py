def test_viz_suggest(client):
    plan = {
        "tables": ["sales"],
        "filters": [],
        "group_by": [],
        "metrics": ["COUNT(*) as total"],
        "sql": "SELECT COUNT(*) as total FROM sales",
    }
    r = client.post("/viz/suggest", json=plan)
    assert r.status_code == 200
    data = r.json()
    assert "suggestions" in data
    assert len(data["suggestions"]) >= 1
