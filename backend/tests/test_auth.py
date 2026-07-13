from fastapi.testclient import TestClient


def test_register_user(auth_client: TestClient):

    payload = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "password": "MyPassword123",
    }

    response = auth_client.post(
        "/auth/register",
        json=payload,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["full_name"] == "John Doe"
    assert body["email"] == "john@example.com"
    assert body["is_active"] is True
    assert "id" in body
    assert "created_at" in body


def test_duplicate_email_returns_conflict(
    auth_client: TestClient,
):

    payload = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "password": "MyPassword123",
    }

    auth_client.post(
        "/auth/register",
        json=payload,
    )

    response = auth_client.post(
        "/auth/register",
        json=payload,
    )

    assert response.status_code == 409

    body = response.json()

    assert body["error"]["code"] == "USER_ALREADY_EXISTS"


def test_login_returns_access_token(
    auth_client: TestClient,
):

    register_payload = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "password": "MyPassword123",
    }

    auth_client.post(
        "/auth/register",
        json=register_payload,
    )

    login_payload = {
        "email": "john@example.com",
        "password": "MyPassword123",
    }

    response = auth_client.post(
        "/auth/login",
        json=login_payload,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["token_type"] == "bearer"
    assert isinstance(
        body["access_token"],
        str,
    )
    assert len(body["access_token"]) > 20


def test_login_rejects_wrong_password(
    auth_client: TestClient,
):

    register_payload = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "password": "MyPassword123",
    }

    auth_client.post(
        "/auth/register",
        json=register_payload,
    )

    response = auth_client.post(
        "/auth/login",
        json={
            "email": "john@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401

    body = response.json()

    assert body["error"]["code"] == "INVALID_CREDENTIALS"


def test_login_rejects_unknown_email(
    auth_client: TestClient,
):

    response = auth_client.post(
        "/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "MyPassword123",
        },
    )

    assert response.status_code == 401

    body = response.json()

    assert body["error"]["code"] == "INVALID_CREDENTIALS"


def register_and_login_user(
    auth_client: TestClient,
) -> str:
    """Register a user and return a valid access token."""

    auth_client.post(
        "/auth/register",
        json={
            "full_name": "John Doe",
            "email": "john@example.com",
            "password": "MyPassword123",
        },
    )

    response = auth_client.post(
        "/auth/login",
        json={
            "email": "john@example.com",
            "password": "MyPassword123",
        },
    )

    return response.json()["access_token"]


def test_get_me_returns_authenticated_user(
    auth_client: TestClient,
):

    token = register_and_login_user(auth_client)

    response = auth_client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["full_name"] == "John Doe"
    assert body["email"] == "john@example.com"
    assert body["is_active"] is True
    assert "id" in body
    assert "created_at" in body


def test_get_me_rejects_missing_token(
    auth_client: TestClient,
):

    response = auth_client.get("/auth/me")

    assert response.status_code == 401

    body = response.json()

    assert body["error"]["code"] == "INVALID_TOKEN"
    assert body["error"]["message"] == "Invalid or expired access token."


def test_get_me_rejects_invalid_token(
    auth_client: TestClient,
):

    response = auth_client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401

    body = response.json()

    assert body["error"]["code"] == "INVALID_TOKEN"
    assert body["error"]["message"] == "Invalid or expired access token."
