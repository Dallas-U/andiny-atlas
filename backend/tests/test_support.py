import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.core.constants import InvestigationStatus
from app.exceptions.exceptions import PersistenceDataException
from app.models.case_response import InvestigationResult
from app.repositories.case_repository import CaseRepository


def build_investigation_payload(
    customer_name: str = "John Doe",
    phone_number: str = "08021234567",
) -> dict:
    """Build a valid investigation API payload."""

    return {
        "customer_name": customer_name,
        "phone_number": phone_number,
        "country": "Nigeria",
        "payment_verified": True,
        "extension_triggered": True,
        "api_success": True,
        "skg_success": True,
        "device_online": True,
        "sim_slot_one": True,
        "mobile_data_on": True,
    }


def build_repository_case(
    case_id: str,
    customer_name: str,
    phone_number: str,
    created_by: str,
    status: str,
    timestamp: str,
) -> dict:
    """Build a persisted investigation record for API tests."""

    return {
        "case_id": case_id,
        "timestamp": timestamp,
        "customer_name": customer_name,
        "phone_number": phone_number,
        "created_by": created_by,
        "result": {
            "status": status,
            "reason": "Support API test investigation.",
            "next_action": "No further action required.",
        },
    }


def build_update_payload(
    status: str = "Escalated",
    reason: str = "Additional technical review is required.",
    next_action: str = "Escalate to the engineering team.",
) -> dict:
    """Build a valid investigation update payload."""

    return {
        "status": status,
        "reason": reason,
        "next_action": next_action,
    }


def test_investigate_case(client: TestClient):

    response = client.post(
        "/support/investigate",
        json=build_investigation_payload(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["customer_name"] == "John Doe"
    assert body["phone_number"] == "08021234567"
    assert body["result"]["status"] == InvestigationStatus.RESOLVED.value
    assert "created_by" in body


def test_get_cases_returns_paginated_response(
    client: TestClient,
):

    response = client.get("/support/cases")

    assert response.status_code == 200

    assert response.json() == {
        "metadata": {
            "page": 1,
            "page_size": 20,
            "total_records": 0,
            "total_pages": 0,
            "returned_records": 0,
        },
        "items": [],
    }


def test_get_cases_returns_pagination_metadata(
    client: TestClient,
    isolated_repository: CaseRepository,
):

    isolated_repository.create_case(
        build_repository_case(
            case_id="case-001",
            customer_name="Alice Doe",
            phone_number="08020000001",
            created_by="user-001",
            status="Resolved",
            timestamp="2026-07-11T10:00:00+00:00",
        )
    )

    isolated_repository.create_case(
        build_repository_case(
            case_id="case-002",
            customer_name="Bob Doe",
            phone_number="08020000002",
            created_by="user-002",
            status="Waiting",
            timestamp="2026-07-11T11:00:00+00:00",
        )
    )

    isolated_repository.create_case(
        build_repository_case(
            case_id="case-003",
            customer_name="Charlie Doe",
            phone_number="08020000003",
            created_by="user-003",
            status="Escalated",
            timestamp="2026-07-11T12:00:00+00:00",
        )
    )

    response = client.get(
        "/support/cases",
        params={
            "page": 2,
            "page_size": 2,
            "sort_by": "timestamp",
            "sort_order": "asc",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["metadata"] == {
        "page": 2,
        "page_size": 2,
        "total_records": 3,
        "total_pages": 2,
        "returned_records": 1,
    }

    assert len(body["items"]) == 1
    assert body["items"][0]["case_id"] == "case-003"


def test_get_cases_filters_by_status(
    client: TestClient,
    isolated_repository: CaseRepository,
):

    isolated_repository.create_case(
        build_repository_case(
            case_id="case-001",
            customer_name="John Doe",
            phone_number="08020000001",
            created_by="user-001",
            status="Resolved",
            timestamp="2026-07-11T10:00:00+00:00",
        )
    )

    isolated_repository.create_case(
        build_repository_case(
            case_id="case-002",
            customer_name="Jane Doe",
            phone_number="08020000002",
            created_by="user-002",
            status="Waiting",
            timestamp="2026-07-11T11:00:00+00:00",
        )
    )

    response = client.get(
        "/support/cases",
        params={
            "status": InvestigationStatus.WAITING.value,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["metadata"]["total_records"] == 1
    assert body["metadata"]["returned_records"] == 1
    assert body["items"][0]["case_id"] == "case-002"
    assert body["items"][0]["result"]["status"] == "Waiting"


def test_get_cases_sorts_by_customer_name(
    client: TestClient,
    isolated_repository: CaseRepository,
):

    isolated_repository.create_case(
        build_repository_case(
            case_id="case-001",
            customer_name="Charlie Doe",
            phone_number="08020000001",
            created_by="user-001",
            status="Resolved",
            timestamp="2026-07-11T10:00:00+00:00",
        )
    )

    isolated_repository.create_case(
        build_repository_case(
            case_id="case-002",
            customer_name="Alice Doe",
            phone_number="08020000002",
            created_by="user-002",
            status="Resolved",
            timestamp="2026-07-11T11:00:00+00:00",
        )
    )

    isolated_repository.create_case(
        build_repository_case(
            case_id="case-003",
            customer_name="Bob Doe",
            phone_number="08020000003",
            created_by="user-003",
            status="Resolved",
            timestamp="2026-07-11T12:00:00+00:00",
        )
    )

    response = client.get(
        "/support/cases",
        params={
            "sort_by": "customer_name",
            "sort_order": "asc",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert [case["customer_name"] for case in body["items"]] == [
        "Alice Doe",
        "Bob Doe",
        "Charlie Doe",
    ]


def test_get_my_cases_returns_only_authenticated_users_cases(
    client: TestClient,
    isolated_repository: CaseRepository,
):

    current_user_response = client.get("/auth/me")

    assert current_user_response.status_code == 200

    current_user_id = current_user_response.json()["id"]

    investigation_response = client.post(
        "/support/investigate",
        json=build_investigation_payload(
            customer_name="Owned Case",
            phone_number="08021111111",
        ),
    )

    assert investigation_response.status_code == 200

    isolated_repository.create_case(
        build_repository_case(
            case_id="other-user-case",
            customer_name="Other User Case",
            phone_number="08022222222",
            created_by="another-user-id",
            status="Resolved",
            timestamp="2026-07-11T12:00:00+00:00",
        )
    )

    response = client.get("/support/my-cases")

    assert response.status_code == 200

    body = response.json()

    assert body["metadata"]["total_records"] == 1
    assert body["metadata"]["returned_records"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0]["customer_name"] == "Owned Case"
    assert body["items"][0]["created_by"] == current_user_id


def test_my_cases_ignores_supplied_created_by_filter(
    client: TestClient,
    isolated_repository: CaseRepository,
):

    current_user_response = client.get("/auth/me")

    assert current_user_response.status_code == 200

    current_user_id = current_user_response.json()["id"]

    investigation_response = client.post(
        "/support/investigate",
        json=build_investigation_payload(
            customer_name="Current User Case",
            phone_number="08023333333",
        ),
    )

    assert investigation_response.status_code == 200

    isolated_repository.create_case(
        build_repository_case(
            case_id="other-user-case",
            customer_name="Other User Case",
            phone_number="08024444444",
            created_by="another-user-id",
            status="Resolved",
            timestamp="2026-07-11T13:00:00+00:00",
        )
    )

    response = client.get(
        "/support/my-cases",
        params={
            "created_by": "another-user-id",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["metadata"]["total_records"] == 1
    assert body["items"][0]["created_by"] == current_user_id
    assert body["items"][0]["customer_name"] == "Current User Case"


def test_get_cases_rejects_invalid_page(
    client: TestClient,
):

    response = client.get(
        "/support/cases",
        params={
            "page": 0,
        },
    )

    assert response.status_code == 422


def test_get_cases_rejects_invalid_page_size(
    client: TestClient,
):

    response = client.get(
        "/support/cases",
        params={
            "page_size": 101,
        },
    )

    assert response.status_code == 422


def test_get_cases_rejects_invalid_sort_field(
    client: TestClient,
):

    response = client.get(
        "/support/cases",
        params={
            "sort_by": "unsupported_field",
        },
    )

    assert response.status_code == 422


def test_get_unknown_case(client: TestClient):

    response = client.get("/support/cases/unknown-id")

    assert response.status_code == 404

    body = response.json()

    assert body["error"]["code"] == "CASE_NOT_FOUND"
    assert "unknown-id" in body["error"]["message"]


def test_update_case_by_owner(
    client: TestClient,
):

    investigation_response = client.post(
        "/support/investigate",
        json=build_investigation_payload(
            customer_name="Update Owner",
            phone_number="08025550001",
        ),
    )

    assert investigation_response.status_code == 200

    original_case = investigation_response.json()
    case_id = original_case["case_id"]

    response = client.patch(
        f"/support/cases/{case_id}",
        json=build_update_payload(
            status=InvestigationStatus.ESCALATED.value,
            reason="A deeper technical investigation is required.",
            next_action="Escalate the issue to engineering.",
        ),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["case_id"] == case_id
    assert body["result"] == {
        "status": InvestigationStatus.ESCALATED.value,
        "reason": "A deeper technical investigation is required.",
        "next_action": "Escalate the issue to engineering.",
    }


def test_update_case_preserves_immutable_fields(
    client: TestClient,
):

    investigation_response = client.post(
        "/support/investigate",
        json=build_investigation_payload(
            customer_name="Immutable Customer",
            phone_number="08025550002",
        ),
    )

    assert investigation_response.status_code == 200

    original_case = investigation_response.json()

    response = client.patch(
        f"/support/cases/{original_case['case_id']}",
        json=build_update_payload(
            status=InvestigationStatus.WAITING.value,
            reason="Waiting for additional customer information.",
            next_action="Contact the customer for more details.",
        ),
    )

    assert response.status_code == 200

    updated_case = response.json()

    assert updated_case["case_id"] == original_case["case_id"]
    assert updated_case["timestamp"] == original_case["timestamp"]
    assert updated_case["customer_name"] == original_case["customer_name"]
    assert updated_case["phone_number"] == original_case["phone_number"]
    assert updated_case["created_by"] == original_case["created_by"]


def test_update_case_persists_for_subsequent_get(
    client: TestClient,
):

    investigation_response = client.post(
        "/support/investigate",
        json=build_investigation_payload(
            customer_name="Persistent Update",
            phone_number="08025550003",
        ),
    )

    assert investigation_response.status_code == 200

    case_id = investigation_response.json()["case_id"]

    update_response = client.patch(
        f"/support/cases/{case_id}",
        json=build_update_payload(
            status=InvestigationStatus.RESOLVED.value,
            reason="The customer confirmed that the issue is resolved.",
            next_action="Close the investigation.",
        ),
    )

    assert update_response.status_code == 200

    get_response = client.get(
        f"/support/cases/{case_id}",
    )

    assert get_response.status_code == 200

    persisted_case = get_response.json()

    assert persisted_case["result"] == {
        "status": InvestigationStatus.RESOLVED.value,
        "reason": "The customer confirmed that the issue is resolved.",
        "next_action": "Close the investigation.",
    }


def test_update_unknown_case_returns_not_found(
    client: TestClient,
):

    response = client.patch(
        "/support/cases/unknown-id",
        json=build_update_payload(),
    )

    assert response.status_code == 404

    body = response.json()

    assert body["error"]["code"] == "CASE_NOT_FOUND"
    assert "unknown-id" in body["error"]["message"]


def test_update_case_owned_by_another_user_returns_not_found(
    client: TestClient,
    isolated_repository: CaseRepository,
):

    isolated_repository.create_case(
        build_repository_case(
            case_id="another-users-case",
            customer_name="Another User",
            phone_number="08025550004",
            created_by="another-user-id",
            status=InvestigationStatus.WAITING.value,
            timestamp="2026-07-11T15:00:00+00:00",
        )
    )

    response = client.patch(
        "/support/cases/another-users-case",
        json=build_update_payload(
            status=InvestigationStatus.RESOLVED.value,
            reason="Attempted update by a non-owner.",
            next_action="Close the investigation.",
        ),
    )

    assert response.status_code == 404

    body = response.json()

    assert body["error"]["code"] == "CASE_NOT_FOUND"
    assert "another-users-case" in body["error"]["message"]

    persisted_case = isolated_repository.get_case_by_id(
        "another-users-case",
    )

    assert persisted_case is not None
    assert persisted_case["result"] == {
        "status": InvestigationStatus.WAITING.value,
        "reason": "Support API test investigation.",
        "next_action": "No further action required.",
    }


def test_update_case_rejects_invalid_payload(
    client: TestClient,
):

    investigation_response = client.post(
        "/support/investigate",
        json=build_investigation_payload(
            customer_name="Invalid Update",
            phone_number="08025550005",
        ),
    )

    assert investigation_response.status_code == 200

    case_id = investigation_response.json()["case_id"]

    response = client.patch(
        f"/support/cases/{case_id}",
        json={
            "status": "Unsupported Status",
            "reason": "",
            "next_action": "",
        },
    )

    assert response.status_code == 422


def test_get_statistics(client: TestClient):

    response = client.get("/support/statistics")

    assert response.status_code == 200

    assert response.json() == {
        "total_cases": 0,
        "resolved_cases": 0,
        "pending_cases": 0,
        "escalated_cases": 0,
    }


def test_support_endpoint_requires_authentication(
    unauthenticated_client: TestClient,
):

    response = unauthenticated_client.get(
        "/support/statistics",
    )

    assert response.status_code == 401

    assert response.json() == {
        "error": {
            "code": "INVALID_TOKEN",
            "message": "Invalid or expired access token.",
        }
    }


def test_invalid_investigation_status_is_rejected():

    with pytest.raises(ValidationError):
        InvestigationResult(
            status="Invalid Status",
            reason="Invalid investigation result.",
            next_action="No action.",
        )


def test_persistence_failure_returns_controlled_error(
    client: TestClient,
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

    response = client.get("/support/statistics")

    assert response.status_code == 500

    assert response.json() == {
        "error": {
            "code": "PERSISTENCE_DATA_ERROR",
            "message": (
                "Persisted investigation data is invalid and could not be read."
            ),
        }
    }
