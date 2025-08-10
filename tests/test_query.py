def test_preview_query(client):
    r = client.post("/query/", json={"question": "How many rows?", "preview_only": True})
    assert r.status_code == 200
    body = r.json()
    assert body["executed"] is False
    assert "sql" in body["plan"]

def test_execute_query(client):
    r = client.post("/query/", json={"question": "How many rows?", "preview_only": False})
    assert r.status_code == 200
    body = r.json()
    assert body["executed"] is True
    assert body["rows"][0]["total"] == 42
