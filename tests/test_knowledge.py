def test_tables(client):
    r = client.get("/knowledge/tables")
    assert r.status_code == 200
    assert "tables" in r.json()
