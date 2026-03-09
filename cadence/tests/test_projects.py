def test_create_project(client):
    resp = client.post(
        "/api/v1/projects",
        json={
            "name": "Project Alpha",
            "start_date": "2026-03-01",
            "end_date": "2026-05-01",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Project Alpha"
    assert resp.json()["status"] == "draft"


def test_create_project_invalid_dates(client):
    resp = client.post(
        "/api/v1/projects",
        json={
            "name": "Bad Dates",
            "start_date": "2026-05-01",
            "end_date": "2026-03-01",
        },
    )
    assert resp.status_code == 400


def test_commit_project_creates_baseline(client):
    create_resp = client.post(
        "/api/v1/projects",
        json={"name": "P1", "start_date": "2026-03-01", "end_date": "2026-05-01"},
    )
    project_id = create_resp.json()["id"]

    # Transition to committed
    client.patch(f"/api/v1/projects/{project_id}", json={"status": "committed"})

    # Check delay — baseline should exist with 0 delay
    delay_resp = client.get(f"/api/v1/projects/{project_id}/delay")
    assert delay_resp.status_code == 200
    delay = delay_resp.json()
    assert delay["start_delay_days"] == 0
    assert delay["end_delay_days"] == 0


def test_delay_after_date_change(client):
    create_resp = client.post(
        "/api/v1/projects",
        json={"name": "P2", "start_date": "2026-03-01", "end_date": "2026-05-01"},
    )
    project_id = create_resp.json()["id"]

    # Commit, then change end date
    client.patch(f"/api/v1/projects/{project_id}", json={"status": "committed"})
    client.patch(f"/api/v1/projects/{project_id}", json={"end_date": "2026-05-15"})

    delay_resp = client.get(f"/api/v1/projects/{project_id}/delay")
    delay = delay_resp.json()
    assert delay["end_delay_days"] == 14
    assert delay["start_delay_days"] == 0


def test_no_delay_before_commit(client):
    create_resp = client.post(
        "/api/v1/projects",
        json={"name": "P3", "start_date": "2026-03-01", "end_date": "2026-05-01"},
    )
    project_id = create_resp.json()["id"]
    delay_resp = client.get(f"/api/v1/projects/{project_id}/delay")
    assert delay_resp.status_code == 200
    assert delay_resp.json() is None


def test_project_tags(client):
    # Create project and tag
    project_resp = client.post(
        "/api/v1/projects",
        json={"name": "Tagged", "start_date": "2026-03-01", "end_date": "2026-05-01"},
    )
    project_id = project_resp.json()["id"]
    tag_resp = client.post("/api/v1/tags", json={"level": "SO", "value": "SO-42"})
    tag_id = tag_resp.json()["id"]

    # Tag the project
    resp = client.post(f"/api/v1/projects/{project_id}/tags/{tag_id}")
    assert resp.status_code == 204

    # Verify tag is listed
    tags = client.get(f"/api/v1/projects/{project_id}/tags").json()
    assert len(tags) == 1
    assert tags[0]["value"] == "SO-42"

    # Untag
    client.delete(f"/api/v1/projects/{project_id}/tags/{tag_id}")
    tags = client.get(f"/api/v1/projects/{project_id}/tags").json()
    assert len(tags) == 0


def test_project_external_references(client):
    project_resp = client.post(
        "/api/v1/projects",
        json={"name": "Ref Project", "start_date": "2026-03-01", "end_date": "2026-05-01"},
    )
    project_id = project_resp.json()["id"]

    # Add Jira reference
    ref_resp = client.post(
        f"/api/v1/projects/{project_id}/external-references",
        json={
            "reference_type": "jira_epic",
            "external_id": "JIRA-1234",
            "external_url": "https://jira.example.com/JIRA-1234",
        },
    )
    assert ref_resp.status_code == 201
    ref_id = ref_resp.json()["id"]

    # List references
    refs = client.get(f"/api/v1/projects/{project_id}/external-references").json()
    assert refs["total"] == 1

    # Delete reference
    client.delete(f"/api/v1/projects/{project_id}/external-references/{ref_id}")
    refs = client.get(f"/api/v1/projects/{project_id}/external-references").json()
    assert refs["total"] == 0


def test_project_detail_includes_everything(client):
    # Create BO, team, project, tag, reference
    bo_resp = client.post("/api/v1/business-objectives", json={"name": "BO-1"})
    bo_id = bo_resp.json()["id"]
    team_resp = client.post("/api/v1/teams", json={"name": "Team-1"})
    team_id = team_resp.json()["id"]

    project_resp = client.post(
        "/api/v1/projects",
        json={
            "name": "Full Project",
            "start_date": "2026-03-01",
            "end_date": "2026-05-01",
            "team_id": team_id,
            "business_objective_id": bo_id,
        },
    )
    project_id = project_resp.json()["id"]

    # Add tag
    tag_resp = client.post("/api/v1/tags", json={"level": "FE", "value": "FE-1"})
    tag_id = tag_resp.json()["id"]
    client.post(f"/api/v1/projects/{project_id}/tags/{tag_id}")

    # Add reference
    client.post(
        f"/api/v1/projects/{project_id}/external-references",
        json={"reference_type": "dod", "external_id": "DOD-99"},
    )

    # Commit to create baseline
    client.patch(f"/api/v1/projects/{project_id}", json={"status": "committed"})

    # Get detail
    detail = client.get(f"/api/v1/projects/{project_id}").json()
    assert detail["team_id"] == team_id
    assert detail["business_objective_id"] == bo_id
    assert detail["baseline"] is not None
    assert detail["delay"]["start_delay_days"] == 0
    assert len(detail["tags"]) == 1
    assert len(detail["external_references"]) == 1
