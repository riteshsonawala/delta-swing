def test_create_business_objective(client):
    resp = client.post(
        "/api/v1/business-objectives",
        json={"name": "Increase Revenue", "description": "Q1 revenue target"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Increase Revenue"
    assert data["id"] is not None


def test_list_business_objectives(client):
    client.post("/api/v1/business-objectives", json={"name": "BO 1"})
    client.post("/api/v1/business-objectives", json={"name": "BO 2"})
    resp = client.get("/api/v1/business-objectives")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_get_business_objective(client):
    create_resp = client.post("/api/v1/business-objectives", json={"name": "BO"})
    bo_id = create_resp.json()["id"]
    resp = client.get(f"/api/v1/business-objectives/{bo_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "BO"


def test_update_business_objective(client):
    create_resp = client.post("/api/v1/business-objectives", json={"name": "Old"})
    bo_id = create_resp.json()["id"]
    resp = client.patch(f"/api/v1/business-objectives/{bo_id}", json={"name": "New"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "New"


def test_delete_business_objective(client):
    create_resp = client.post("/api/v1/business-objectives", json={"name": "Delete me"})
    bo_id = create_resp.json()["id"]
    resp = client.delete(f"/api/v1/business-objectives/{bo_id}")
    assert resp.status_code == 204
    resp = client.get(f"/api/v1/business-objectives/{bo_id}")
    assert resp.status_code == 404


def test_get_nonexistent_bo(client):
    resp = client.get("/api/v1/business-objectives/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
