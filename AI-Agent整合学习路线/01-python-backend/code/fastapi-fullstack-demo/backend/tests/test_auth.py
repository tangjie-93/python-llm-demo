def test_register_user(client):
    response = client.post("/api/auth/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "StrongPass1!"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "user_id" in data["data"]


def test_register_duplicate_username(client, test_user):
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "another@example.com",
        "password": "StrongPass1!"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False


def test_login_success(client, test_user):
    response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "Test1234!"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]


def test_login_wrong_password(client, test_user):
    response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "WrongPass1!"
    })
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post("/api/auth/login", data={
        "username": "nobody",
        "password": "Test1234!"
    })
    assert response.status_code == 401


def test_get_current_user(client, auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["username"] == "testuser"


def test_get_current_user_no_token(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_logout(client, auth_headers):
    response = client.post("/api/auth/logout", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
