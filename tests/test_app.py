from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_and_delete_participant():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]

    delete_response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert delete_response.status_code == 200

    updated_activities = client.get("/activities").json()
    assert email not in updated_activities[activity_name]["participants"]


def test_duplicate_signup_returns_400():
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    duplicate_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert duplicate_response.status_code == 400
    assert "already signed up" in duplicate_response.json()["detail"]


def test_missing_activity_returns_404():
    response = client.get("/activities/Unknown Activity")
    assert response.status_code == 404


def test_delete_missing_participant_returns_404():
    response = client.delete("/activities/Chess Club/signup?email=missing@mergington.edu")
    assert response.status_code == 404
