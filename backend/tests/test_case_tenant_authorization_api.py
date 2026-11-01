from datetime import UTC, datetime
from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.constants import InvestigationStatus
from app.database.models import CaseHistory as ORMCaseHistory
from app.domain import Case, Customer
from app.domain import InvestigationResult as DomainInvestigationResult
from app.repositories.case_repository import CaseRepository
from app.services.case_manager import CaseManager


OTHER_ORGANIZATION_ID = "00000000-0000-4000-8000-000000000099"


def build_foreign_case(case_id: str, created_by: str) -> Case:
    return Case(
        case_id=case_id,
        timestamp=datetime(2026, 7, 11, 10, 0, tzinfo=UTC),
        customer=Customer(
            name="Foreign Tenant Customer",
            phone_number="08025550099",
        ),
        created_by=created_by,
        organization_id=OTHER_ORGANIZATION_ID,
        result=DomainInvestigationResult(
            status=InvestigationStatus.WAITING,
            reason="Original foreign-tenant reason.",
            next_action="Original foreign-tenant action.",
        ),
    )


def seed_foreign_case(
    repository: CaseRepository,
    case_id: str,
    created_by: str,
) -> Case:
    case = build_foreign_case(case_id, created_by)
    repository.create_case(case)
    return case


def test_cross_tenant_case_get_is_denied(
    supervisor_client: TestClient,
    isolated_repository: CaseRepository,
    supervisor_user,
):
    case_id = "foreign-tenant-get-case"

    seed_foreign_case(
        isolated_repository,
        case_id,
        supervisor_user.id,
    )

    response = supervisor_client.get(
        f"/support/cases/{case_id}",
    )

    assert response.status_code == 403


def test_cross_tenant_case_history_is_denied_before_history_read(
    supervisor_client: TestClient,
    isolated_repository: CaseRepository,
    supervisor_user,
    case_manager: CaseManager,
    monkeypatch,
):
    case_id = "foreign-tenant-history-case"

    seed_foreign_case(
        isolated_repository,
        case_id,
        supervisor_user.id,
    )

    history_reads = []
    original_get_case_history = case_manager.get_case_history

    def tracked_get_case_history(requested_case_id: str):
        history_reads.append(requested_case_id)
        return original_get_case_history(requested_case_id)

    monkeypatch.setattr(
        case_manager,
        "get_case_history",
        tracked_get_case_history,
    )

    response = supervisor_client.get(
        f"/support/cases/{case_id}/history",
    )

    assert response.status_code == 403
    assert history_reads == []


def test_cross_tenant_case_update_is_denied_without_mutating_case_or_history(
    supervisor_client: TestClient,
    isolated_repository: CaseRepository,
    supervisor_user,
    test_session_factory,
):
    case_id = "foreign-tenant-update-case"

    original_case = seed_foreign_case(
        isolated_repository,
        case_id,
        supervisor_user.id,
    )

    original_history = ORMCaseHistory(
        id=str(uuid4()),
        case_id=case_id,
        status=InvestigationStatus.WAITING.value,
        reason="Original audit reason.",
        next_action="Original audit action.",
        changed_by=supervisor_user.id,
        changed_at=datetime(2026, 7, 11, 10, 5, tzinfo=UTC),
    )

    with test_session_factory() as session:
        session.add(original_history)
        session.commit()

    response = supervisor_client.patch(
        f"/support/cases/{case_id}",
        json={
            "status": InvestigationStatus.RESOLVED.value,
            "reason": "Unauthorized attempted change.",
            "next_action": "Unauthorized attempted action.",
        },
    )

    assert response.status_code == 403

    persisted_case = isolated_repository.get_case_by_id(case_id)

    assert persisted_case is not None
    assert persisted_case.organization_id == OTHER_ORGANIZATION_ID
    assert persisted_case.created_by == supervisor_user.id
    assert persisted_case.result == original_case.result

    with test_session_factory() as session:
        persisted_history = (
            session.query(ORMCaseHistory)
            .filter(ORMCaseHistory.case_id == case_id)
            .all()
        )

        assert len(persisted_history) == 1
        assert persisted_history[0].id == original_history.id
        assert persisted_history[0].status == original_history.status
        assert persisted_history[0].reason == original_history.reason
        assert persisted_history[0].next_action == original_history.next_action
        assert persisted_history[0].changed_by == original_history.changed_by
