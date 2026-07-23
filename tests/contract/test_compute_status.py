def test_compute_node_is_explicitly_unavailable(client):
    response = client.get("/api/v1/system/compute-status/")
    assert response.status_code == 503
    assert response.json()["status"] == "unavailable"
    assert response.json()["code"] == "compute_node_unavailable"
    assert set(response.json()) == {"status", "code", "checked_at"}
