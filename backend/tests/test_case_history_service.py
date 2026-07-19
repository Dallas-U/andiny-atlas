from datetime import UTC, datetime
from unittest.mock import Mock

import pytest

from app.core.constants import InvestigationStatus
from app.domain import (
    Case,
    CaseHistory,
    Customer,
    InvestigationResult,
)
from app.exceptions.exceptions import CaseNotFoundException
from app.repositories.case_repository import CaseRepository
from app.services.case_manager import CaseManager


def build_case(
    case_id: str = "case-service-001",
    created_by: str = "user-001",
    status: InvestigationStatus = InvestigationStatus.WAITING,
    reason: str = "Awaiting customer confirmation.",
    next_action: str = "Contact the customer again.",
) -> Case:
    """Build a domain case for case-manager audit tests."""

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
            name="Service Customer",
            phone_number="08029876543",
        ),
        created_by=created_by,
        result=InvestigationResult(
            status=status,
            reason=reason,
            next_action=next_action,
        ),
    )


def test_update_case_creates_history_from_pre_update_state():
    repository = Mock(spec=CaseRepository)
    manager = CaseManager(repository)

    original_case = build_case()

    expected_updated_case = build_case(
        status=InvestigationStatus.RESOLVED,
        reason="Customer confirmed successful resolution.",
        next_action="Close the investigation.",
    )

    repository.get_case_by_id.return_value = original_case
    repository.update_case_with_history.return_value = (
        expected_updated_case
    )

    updated_case = manager.update_case(
        case_id=original_case.case_id,
        status=InvestigationStatus.RESOLVED,
        reason="  Customer confirmed successful resolution.  ",
        next_action="  Close the investigation.  ",
        current_user_id="user-001",
    )

    assert updated_case == expected_updated_case

    repository.update_case_with_history.assert_called_once()

    call_arguments = (
        repository.update_case_with_history.call_args.kwargs
    )

    history = call_arguments["history"]

    assert isinstance(history, CaseHistory)
    assert history.id is not None
    assert history.case_id == original_case.case_id
    assert history.status == InvestigationStatus.WAITING
    assert history.reason == original_case.result.reason
    assert history.next_action == original_case.result.next_action
    assert history.changed_by == "user-001"
    assert history.changed_at.tzinfo is not None

    assert call_arguments["case_id"] == original_case.case_id
    assert (
        call_arguments["status"]
        == InvestigationStatus.RESOLVED
    )
    assert (
        call_arguments["reason"]
        == "Customer confirmed successful resolution."
    )
    assert (
        call_arguments["next_action"]
        == "Close the investigation."
    )


def test_update_case_rejects_update_from_non_owner():
    repository = Mock(spec=CaseRepository)
    manager = CaseManager(repository)

    repository.get_case_by_id.return_value = build_case(
        created_by="owner-001",
    )

    with pytest.raises(CaseNotFoundException):
        manager.update_case(
            case_id="case-service-001",
            status=InvestigationStatus.RESOLVED,
            reason="Investigation completed.",
            next_action="Close the investigation.",
            current_user_id="different-user",
        )

    repository.update_case_with_history.assert_not_called()


def test_update_case_raises_when_case_does_not_exist():
    repository = Mock(spec=CaseRepository)
    manager = CaseManager(repository)

    repository.get_case_by_id.return_value = None

    with pytest.raises(CaseNotFoundException):
        manager.update_case(
            case_id="missing-case",
            status=InvestigationStatus.RESOLVED,
            reason="Investigation completed.",
            next_action="Close the investigation.",
            current_user_id="user-001",
        )

    repository.update_case_with_history.assert_not_called()


def test_get_case_history_returns_repository_history():
    repository = Mock(spec=CaseRepository)
    manager = CaseManager(repository)

    case = build_case()

    expected_history = [
        CaseHistory(
            id="history-001",
            case_id=case.case_id,
            status=case.result.status,
            reason=case.result.reason,
            next_action=case.result.next_action,
            changed_by="user-001",
            changed_at=datetime(
                2026,
                7,
                18,
                10,
                0,
                tzinfo=UTC,
            ),
        )
    ]

    repository.get_case_by_id.return_value = case
    repository.get_case_history.return_value = expected_history

    history = manager.get_case_history(case.case_id)

    assert history == expected_history

    repository.get_case_by_id.assert_called_once_with(
        case.case_id
    )
    repository.get_case_history.assert_called_once_with(
        case.case_id
    )


def test_get_case_history_returns_empty_list_for_existing_case():
    repository = Mock(spec=CaseRepository)
    manager = CaseManager(repository)

    case = build_case()

    repository.get_case_by_id.return_value = case
    repository.get_case_history.return_value = []

    history = manager.get_case_history(case.case_id)

    assert history == []


def test_get_case_history_raises_when_case_does_not_exist():
    repository = Mock(spec=CaseRepository)
    manager = CaseManager(repository)

    repository.get_case_by_id.return_value = None

    with pytest.raises(CaseNotFoundException):
        manager.get_case_history("missing-case")

    repository.get_case_history.assert_not_called()