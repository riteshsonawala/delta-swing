def test_create_team_member(client):
    resp = client.post(
        "/api/v1/team-members",
        json={"name": "Bob", "email": "bob@test.com"},
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Bob"
    assert resp.json()["team_id"] is None


def test_duplicate_email_rejected(client):
    client.post("/api/v1/team-members", json={"name": "A", "email": "dup@test.com"})
    resp = client.post("/api/v1/team-members", json={"name": "B", "email": "dup@test.com"})
    assert resp.status_code == 409


def test_assign_member_to_team(client):
    team_resp = client.post("/api/v1/teams", json={"name": "Team X"})
    team_id = team_resp.json()["id"]
    member_resp = client.post(
        "/api/v1/team-members", json={"name": "Carol", "email": "carol@test.com"}
    )
    member_id = member_resp.json()["id"]

    resp = client.patch(
        f"/api/v1/team-members/{member_id}", json={"team_id": team_id}
    )
    assert resp.status_code == 200
    assert resp.json()["team_id"] == team_id


def test_assign_lead(client):
    lead_resp = client.post(
        "/api/v1/team-members", json={"name": "Lead", "email": "lead@test.com"}
    )
    lead_id = lead_resp.json()["id"]
    member_resp = client.post(
        "/api/v1/team-members",
        json={"name": "Member", "email": "member@test.com", "lead_id": lead_id},
    )
    assert member_resp.status_code == 201
    assert member_resp.json()["lead_id"] == lead_id
