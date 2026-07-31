# tests/integration/test_user_routes.py


def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "username": "davidtest",
            "email": "davidtest@example.com",
            "password": "SecurePassword123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "davidtest"
    assert data["email"] == "davidtest@example.com"
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_user(client):
    payload = {
        "username": "duplicate",
        "email": "duplicate@example.com",
        "password": "SecurePassword123",
    }

    first_response = client.post(
        "/users/register",
        json=payload,
    )

    second_response = client.post(
        "/users/register",
        json=payload,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_login_user(client):
    user_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "SecurePassword123",
    }

    client.post(
        "/users/register",
        json=user_data,
    )

    response = client.post(
        "/users/login",
        json={
            "username": user_data["username"],
            "password": user_data["password"],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Login successful"
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 20
    assert data["user"]["username"] == user_data["username"]


def test_login_with_wrong_password(client):
    client.post(
        "/users/register",
        json={
            "username": "wrongpassword",
            "email": "wrongpassword@example.com",
            "password": "SecurePassword123",
        },
    )

    response = client.post(
        "/users/login",
        json={
            "username": "wrongpassword",
            "password": "IncorrectPassword",
        },
    )

    assert response.status_code == 401


def test_registration_rejects_invalid_email(client):
    response = client.post(
        "/users/register",
        json={
            "username": "invalidemail",
            "email": "not-an-email",
            "password": "SecurePassword123",
        },
    )

    assert response.status_code == 422