from datetime import UTC, datetime

from app.core.constants import InvestigationStatus
from app.domain import (
    Case,
    CaseHistory,
    Customer,
    InvestigationResult,
)
from app.repositories.case_repository import CaseRepository


def build_case(
    case_id: str = "case-history-001",
    status: InvestigationStatus = InvestigationStatus.WAITING,
) -> Case:
    """Build a domain case for audit-history repository tests."""

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
            name="History Customer",
            phone_number="08021234567",
        ),
        created_by="user-001",
        result=InvestigationResult(
            status=status,
            reason="Awaiting customer confirmation.",
            next_action="Contact the customer again.",
        ),
    )


def build_history(
    history_id: str,
    case_id: str = "case-history-001",
    status: InvestigationStatus = InvestigationStatus.WAITING,
    reason: str = "Awaiting customer confirmation.",
    next_action: str = "Contact the customer again.",
    changed_by: str = "user-001",
    changed_at: datetime = datetime(
        2026,
        7,
        18,
        10,
        0,
        tzinfo=UTC,
    ),
) -> CaseHistory:
    """Build a domain audit-history entry."""

    return CaseHistory(
        id=history_id,
        case_id=case_id,
        status=status,
        reason=reason,
        next_action=next_action,
        changed_by=changed_by,
        changed_at=changed_at,
    )


def test_get_case_history_returns_empty_list_for_case_without_updates(
    isolated_repository: CaseRepository,
):
    isolated_repository.create_case(
        build_case()
    )

    history = isolated_repository.get_case_history(
        "case-history-001"
    )

    assert history == []


def test_update_case_with_history_persists_history_and_updated_case(
    isolated_repository: CaseRepository,
):
    original_case = build_case()

    isolated_repository.create_case(original_case)

    history_entry = build_history(
        history_id="history-001",
    )

    updated_case = isolated_repository.update_case_with_history(
        case_id=original_case.case_id,
        status=InvestigationStatus.RESOLVED,
        reason="Customer confirmed the issue is resolved.",
        next_action="Close the investigation.",
        history=history_entry,
    )

    assert updated_case is not None
    assert updated_case.result == InvestigationResult(
        status=InvestigationStatus.RESOLVED,
        reason="Customer confirmed the issue is resolved.",
        next_action="Close the investigation.",
    )

    persisted_history = isolated_repository.get_case_history(
        original_case.case_id
    )

    assert persisted_history == [history_entry]


def test_case_history_preserves_pre_update_state(
    isolated_repository: CaseRepository,
):
    original_case = build_case(
        status=InvestigationStatus.WAITING,
    )

    isolated_repository.create_case(original_case)

    history_entry = build_history(
        history_id="history-001",
        status=original_case.result.status,
        reason=original_case.result.reason,
        next_action=original_case.result.next_action,
    )

    isolated_repository.update_case_with_history(
        case_id=original_case.case_id,
        status=InvestigationStatus.ESCALATED,
        reason="Technical intervention is required.",
        next_action="Escalate to engineering.",
        history=history_entry,
    )

    persisted_history = isolated_repository.get_case_history(
        original_case.case_id
    )

    assert len(persisted_history) == 1
    assert persisted_history[0].status == InvestigationStatus.WAITING
    assert (
        persisted_history[0].reason
        == "Awaiting customer confirmation."
    )
    assert (
        persisted_history[0].next_action
        == "Contact the customer again."
    )


def test_get_case_history_returns_entries_in_chronological_order(
    isolated_repository: CaseRepository,
):
    case = build_case()

    isolated_repository.create_case(case)

    later_history = build_history(
        history_id="history-002",
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
        reason="Engineering assistance is required.",
        next_action="Assign the case to engineering.",
        history=later_history,
    )

    earlier_history = build_history(
        history_id="history-001",
        status=InvestigationStatus.ESCALATED,
        reason="Engineering assistance is required.",
        next_action="Assign the case to engineering.",
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

    history = isolated_repository.get_case_history(
        case.case_id
    )

    assert [entry.id for entry in history] == [
        "history-001",
        "history-002",
    ]


def test_update_case_with_history_returns_none_for_missing_case(
    isolated_repository: CaseRepository,
):
    history_entry = build_history(
        history_id="history-001",
        case_id="missing-case",
    )

    updated_case = isolated_repository.update_case_with_history(
        case_id="missing-case",
        status=InvestigationStatus.RESOLVED,
        reason="Investigation completed.",
        next_action="Close the investigation.",
        history=history_entry,
    )

    assert updated_case is None
    assert (
        isolated_repository.get_case_history("missing-case")
        == []
    )