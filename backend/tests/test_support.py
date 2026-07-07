from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_investigate_case():

    payload = {
        "customer_name": "John Doe",
        "phone_number": "08021234567",
        "country": "Nigeria",
        "payment_verified": True,
        "extension_triggered": True,
        "api_success": True,
        "skg_success": True,
        "device_online": True,
        "sim_slot_one": True,
        "mobile_data_on": True,
    }

    response = client.post(
        "/support/investigate",
        json=payload,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["customer_name"] == "John Doe"
    assert body["phone_number"] == "08021234567"
    assert body["result"]["status"] == "Resolved"


def test_get_unknown_case():

    response = client.get("/support/cases/unknown-id")

    assert response.status_code == 404

    body = response.json()

    assert body["error"]["code"] == "CASE_NOT_FOUND"

    assert "unknown-id" in body["error"]["message"]


def test_get_statistics():

    response = client.get("/support/statistics")

    assert response.status_code == 200

    body = response.json()

    assert "total_cases" in body
    assert "resolved_cases" in body
    assert "pending_cases" in body
    assert "escalated_cases" in body
