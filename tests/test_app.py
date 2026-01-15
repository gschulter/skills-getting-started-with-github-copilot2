import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities

    # Check structure of an activity
    chess_club = activities["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_for_activity():
    # Test successful signup
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert "Signed up test@mergington.edu for Chess Club" in result["message"]

    # Verify the participant was added
    response = client.get("/activities")
    activities = response.json()
    assert "test@mergington.edu" in activities["Chess Club"]["participants"]

def test_signup_duplicate():
    # Try to sign up the same email again
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "already signed up" in result["detail"]

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Activity not found" in result["detail"]

def test_unregister_from_activity():
    # First sign up
    client.post("/activities/Programming%20Class/signup?email=unregister_test@mergington.edu")

    # Then unregister
    response = client.delete("/activities/Programming%20Class/unregister?email=unregister_test@mergington.edu")
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert "Unregistered unregister_test@mergington.edu from Programming Class" in result["message"]

    # Verify the participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert "unregister_test@mergington.edu" not in activities["Programming Class"]["participants"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess%20Club/unregister?email=not_signed_up@mergington.edu")
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "not signed up" in result["detail"]

def test_unregister_nonexistent_activity():
    response = client.delete("/activities/Nonexistent%20Activity/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Activity not found" in result["detail"]

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    # FastAPI's RedirectResponse might be handled differently in tests
    # The root endpoint redirects to /static/index.html