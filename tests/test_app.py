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

def test_get_cities_by_country():
    # Test getting cities for United States
    response = client.get("/countries/United%20States/cities")
    assert response.status_code == 200
    result = response.json()
    assert result["country"] == "United States"
    assert isinstance(result["cities"], list)
    assert "New York" in result["cities"]
    assert "Los Angeles" in result["cities"]
    assert len(result["cities"]) == 5

def test_get_cities_multiple_countries():
    # Test getting cities for different countries
    countries_to_test = [
        ("Japan", ["Tokyo", "Osaka"]),
        ("France", ["Paris", "Marseille"]),
        ("Canada", ["Toronto", "Vancouver"])
    ]
    
    for country, expected_cities in countries_to_test:
        response = client.get(f"/countries/{country}/cities")
        assert response.status_code == 200
        result = response.json()
        assert result["country"] == country
        for city in expected_cities:
            assert city in result["cities"]

def test_get_cities_nonexistent_country():
    # Test getting cities for a country that doesn't exist
    response = client.get("/countries/Atlantis/cities")
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Country not found" in result["detail"]

def test_max_participants_signup():
    # Test that a student cannot sign up if activity is at max capacity
    response = client.post("/activities/Tennis%20Club/signup?email=new_player@mergington.edu")
    assert response.status_code == 200
    
    # Tennis Club has max 10, currently has 1. Add 9 more to reach capacity
    for i in range(2, 10):
        client.post(f"/activities/Tennis%20Club/signup?email=player{i}@mergington.edu")
    
    # Try to exceed capacity
    response = client.post("/activities/Tennis%20Club/signup?email=over_capacity@mergington.edu")
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "at maximum capacity" in result["detail"].lower() or "max" in result["detail"].lower()

def test_signup_empty_email():
    # Test signup with empty email
    response = client.post("/activities/Chess%20Club/signup?email=")
    assert response.status_code == 422  # Validation error

def test_activity_name_case_sensitivity():
    # Test that activity names are case-sensitive
    response = client.post("/activities/chess%20club/signup?email=case_test@mergington.edu")
    assert response.status_code == 404

def test_get_activities_returns_all():
    # Verify all activities are returned
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == 9
    assert "Gym Class" in activities
    assert "Basketball Team" in activities
    assert "Tennis Club" in activities

def test_activity_participant_list_integrity():
    # Verify participants list maintains integrity after operations
    response = client.get("/activities")
    initial_count = len(response.json()["Drama Club"]["participants"])
    
    client.post("/activities/Drama%20Club/signup?email=integrity_test@mergington.edu")
    response = client.get("/activities")
    assert len(response.json()["Drama Club"]["participants"]) == initial_count + 1
    
    client.delete("/activities/Drama%20Club/unregister?email=integrity_test@mergington.edu")
    response = client.get("/activities")
    assert len(response.json()["Drama Club"]["participants"]) == initial_count

def test_countries_database_completeness():
    # Test that all countries in database have cities
    response = client.get("/countries/Germany/cities")
    assert response.status_code == 200
    result = response.json()
    assert result["country"] == "Germany"
    assert len(result["cities"]) == 5

def test_get_cities_australia():
    # Test getting cities for Australia
    response = client.get("/countries/Australia/cities")
    assert response.status_code == 200
    result = response.json()
    assert result["country"] == "Australia"
    assert "Sydney" in result["cities"]
    assert "Melbourne" in result["cities"]
    assert len(result["cities"]) == 5

def test_country_name_case_sensitivity():
    # Test that country names are case-sensitive
    response = client.get("/countries/united%20states/cities")
    assert response.status_code == 404

def test_special_characters_in_email():
    # Test signup with special characters in email
    response = client.post("/activities/Science%20Club/signup?email=test+tag@mergington.edu")
    assert response.status_code == 200
    result = response.json()
    assert "test+tag@mergington.edu" in result["message"]
