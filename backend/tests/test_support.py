import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.core.constants import InvestigationStatus
from app.dependencies import get_case_manager
from app.exceptions.exceptions import PersistenceDataException
from app.main import app
from app.models.case_response import InvestigationResult
from app.repositories.case_repository import CaseRepository
from app.services.case_manager import CaseManager


def test_investigate_case(client: TestClient):

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
    assert body["result"]["status"] == InvestigationStatus.RESOLVED.value


def test_get_unknown_case(client: TestClient):

    response = client.get("/support/cases/unknown-id")

    assert response.status_code == 404

    body = response.json()

    assert body["error"]["code"] == "CASE_NOT_FOUND"
    assert "unknown-id" in body["error"]["message"]


def test_get_statistics(client: TestClient):

    response = client.get("/support/statistics")

    assert response.status_code == 200

    assert response.json() == {
        "total_cases": 0,
        "resolved_cases": 0,
        "pending_cases": 0,
        "escalated_cases": 0,
    }


def test_invalid_investigation_status_is_rejected():

    with pytest.raises(ValidationError):
        InvestigationResult(
            status="Invalid Status",
            reason="Invalid investigation result.",
            next_action="No action.",
        )


def test_persistence_failure_returns_controlled_error(
    isolated_repository: CaseRepository,
    monkeypatch: pytest.MonkeyPatch,
):

    def fail_to_get_statistics():
        raise PersistenceDataException(
            "Persisted investigation data is invalid and could not be read."
        )

    monkeypatch.setattr(
        isolated_repository,
        "get_statistics",
        fail_to_get_statistics,
    )

    case_manager = CaseManager(isolated_repository)

    app.dependency_overrides[get_case_manager] = lambda: case_manager

    try:
        with TestClient(
            app,
            raise_server_exceptions=False,
        ) as error_client:
            response = error_client.get("/support/statistics")

    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 500

    assert response.json() == {
        "error": {
            "code": "PERSISTENCE_DATA_ERROR",
            "message": (
                "Persisted investigation data is invalid and could not be read."
            ),
        }
    }
