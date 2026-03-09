def test_create_tag(client):
    resp = client.post(
        "/api/v1/tags",
        json={"level": "SO", "value": "SO-001", "description": "Strategic Objective 1"},
    )
    assert resp.status_code == 201
    assert resp.json()["level"] == "SO"
    assert resp.json()["value"] == "SO-001"


def test_duplicate_tag_rejected(client):
    client.post("/api/v1/tags", json={"level": "SO", "value": "SO-001"})
    resp = client.post("/api/v1/tags", json={"level": "SO", "value": "SO-001"})
    assert resp.status_code == 409


def test_list_tags_filter_by_level(client):
    client.post("/api/v1/tags", json={"level": "SO", "value": "SO-1"})
    client.post("/api/v1/tags", json={"level": "PE", "value": "PE-1"})
    client.post("/api/v1/tags", json={"level": "BO", "value": "BO-1"})

    resp = client.get("/api/v1/tags", params={"level": "SO"})
    assert resp.json()["total"] == 1
    assert resp.json()["items"][0]["level"] == "SO"


def test_delete_tag(client):
    create_resp = client.post("/api/v1/tags", json={"level": "FE", "value": "FE-1"})
    tag_id = create_resp.json()["id"]
    resp = client.delete(f"/api/v1/tags/{tag_id}")
    assert resp.status_code == 204
