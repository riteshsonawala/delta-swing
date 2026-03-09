def test_create_team(client):
    resp = client.post("/api/v1/teams", json={"name": "Alpha Team"})
    assert resp.status_code == 201
    assert resp.json()["name"] == "Alpha Team"
    assert resp.json()["is_active"] is True


def test_deactivate_team_unassigns_members(client):
    # Create team and member
    team_resp = client.post("/api/v1/teams", json={"name": "Temp Team"})
    team_id = team_resp.json()["id"]
    member_resp = client.post(
        "/api/v1/team-members",
        json={"name": "Alice", "email": "alice@test.com", "team_id": team_id},
    )
    member_id = member_resp.json()["id"]

    # Deactivate team
    resp = client.patch(f"/api/v1/teams/{team_id}", json={"is_active": False})
    assert resp.status_code == 200
    assert resp.json()["is_active"] is False

    # Member should be unassigned
    member = client.get(f"/api/v1/team-members/{member_id}").json()
    assert member["team_id"] is None


def test_soft_delete_team(client):
    team_resp = client.post("/api/v1/teams", json={"name": "Delete Team"})
    team_id = team_resp.json()["id"]
    client.delete(f"/api/v1/teams/{team_id}")

    # Team still exists but is inactive
    team = client.get(f"/api/v1/teams/{team_id}").json()
    assert team["is_active"] is False
