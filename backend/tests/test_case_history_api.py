from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.core.constants import InvestigationStatus
from app.domain import (
    Case,
    CaseHistory,
    Customer,
    InvestigationResult,
)
from app.repositories.case_repository import CaseRepository


def build_case(
    case_id: str = "case-api-history-001",
) -> Case:
    """Build a domain case for history API tests."""

    return Case(
        case_id=case_id,
        timestamp=datetime(
            2026,
            7,
            18,
            9,
            0,
            tzinfo=UTC,
        ),
        customer=Customer(
            name="API History Customer",
            phone_number="08021234567",
        ),
        created_by="user-api-001",
        result=InvestigationResult(
            status=InvestigationStatus.WAITING,
            reason="Awaiting customer confirmation.",
            next_action="Contact the customer again.",
        ),
    )


def build_history(
    case_id: str = "case-api-history-001",
) -> CaseHistory:
    """Build an audit-history entry for API tests."""

    return CaseHistory(
        id="history-api-001",
        case_id=case_id,
        status=InvestigationStatus.WAITING,
        reason="Awaiting customer confirmation.",
        next_action="Contact the customer again.",
        changed_by="user-api-001",
        changed_at=datetime(
            2026,
            7,
            18,
            10,
            30,
            tzinfo=UTC,
        ),
    )


def test_get_case_history_returns_empty_list_for_case_without_updates(
    supervisor_client: TestClient,
    isolated_repository: CaseRepository,
):
    case = build_case()

    isolated_repository.create_case(case)

    response = supervisor_client.get(
        f"/support/cases/{case.case_id}/history"
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_case_history_returns_audit_entries(
    supervisor_client: TestClient,
    isolated_repository: CaseRepository,
):
    case = build_case()
    history = build_history(case.case_id)

    isolated_repository.create_case(case)

    isolated_repository.update_case_with_history(
        case_id=case.case_id,
        status=InvestigationStatus.RESOLVED,
        reason="Customer confirmed successful resolution.",
        next_action="Close the investigation.",
        history=history,
    )

    response = supervisor_client.get(
        f"/support/cases/{case.case_id}/history"
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "history-api-001",
            "case_id": case.case_id,
            "status": InvestigationStatus.WAITING.value,
            "reason": "Awaiting customer confirmation.",
            "next_action": "Contact the customer again.",
            "changed_by": "user-api-001",
            "changed_at": "2026-07-18T10:30:00Z",
        }
    ]


def test_get_case_history_returns_entries_in_chronological_order(
    supervisor_client: TestClient,
    isolated_repository: CaseRepository,
):
    case = build_case()

    isolated_repository.create_case(case)

    later_history = CaseHistory(
        id="history-api-002",
        case_id=case.case_id,
        status=InvestigationStatus.WAITING,
        reason="Awaiting customer confirmation.",
        next_action="Contact the customer again.",
        changed_by="user-api-001",
        changed_at=datetime(
            2026,
            7,
            18,
            12,
            0,
            tzinfo=UTC,
        ),
    )

    isolated_repository.update_case_with_history(
        case_id=case.case_id,
        status=InvestigationStatus.ESCALATED,
        reason="Technical intervention is required.",
        next_action="Escalate to engineering.",
        history=later_history,
    )

    earlier_history = CaseHistory(
        id="history-api-001",
        case_id=case.case_id,
        status=InvestigationStatus.ESCALATED,
        reason="Technical intervention is required.",
        next_action="Escalate to engineering.",
        changed_by="user-api-001",
        changed_at=datetime(
            2026,
            7,
            18,
            11,
            0,
            tzinfo=UTC,
        ),
    )

    isolated_repository.update_case_with_history(
        case_id=case.case_id,
        status=InvestigationStatus.RESOLVED,
        reason="Engineering resolved the issue.",
        next_action="Close the investigation.",
        history=earlier_history,
    )

    response = supervisor_client.get(
        f"/support/cases/{case.case_id}/history"
    )

    assert response.status_code == 200
    assert [
        entry["id"]
        for entry in response.json()
    ] == [
        "history-api-001",
        "history-api-002",
    ]


def test_get_case_history_returns_not_found_for_unknown_case(
    supervisor_client: TestClient,
):
    response = supervisor_client.get(
        "/support/cases/missing-case/history"
    )

    assert response.status_code == 404

    response_body = response.json()

    assert "error" in response_body
    assert "code" in response_body["error"]
    assert "message" in response_body["error"]


def test_get_case_history_requires_authentication(
    unauthenticated_client: TestClient,
):
    response = unauthenticated_client.get(
        "/support/cases/case-api-history-001/history"
    )

    assert response.status_code == 401