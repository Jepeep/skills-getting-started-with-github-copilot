from src.app import activities


def test_get_activities_returns_all(client):
    # Arrange: initial state provided by fixture

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@example.com"
    assert email not in activities[activity]["participants"]

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    json_data = resp.json()
    assert "Signed up" in json_data.get("message", "")
    assert email in activities[activity]["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@example.com"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"


def test_signup_already_signed_up_returns_400(client):
    # Arrange
    activity = "Chess Club"
    existing_email = activities[activity]["participants"][0]

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": existing_email})

    # Assert
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant_success(client):
    # Arrange
    activity = "Programming Class"
    email = "emma@mergington.edu"
    assert email in activities[activity]["participants"]

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert "Removed" in resp.json().get("message", "")
    assert email not in activities[activity]["participants"]


def test_remove_participant_not_found_returns_404(client):
    # Arrange
    activity = "Art Club"
    email = "notregistered@example.com"
    assert email not in activities[activity]["participants"]

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Participant not found"
