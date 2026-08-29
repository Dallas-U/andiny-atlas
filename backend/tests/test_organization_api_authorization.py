from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_organization_creation_requires_authentication():
    response = client.post(
        "/organizations/",
        json={
            "name": "Unauthorized Organization",
            "code": "UNAUTH",
            "industry": "Technology",
            "contact_email": "unauthorized@test.com",
        },
    )

    assert response.status_code == 401


def test_organization_list_requires_authentication():
    response = client.get(
        "/organizations/",
    )

    assert response.status_code == 401


def test_organization_get_requires_authentication():
    response = client.get(
        "/organizations/org-001",
    )

    assert response.status_code == 401