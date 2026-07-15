from app.core.constants import InvestigationStatus
from app.models.query import (
    CaseQuery,
    CaseSortField,
    SortOrder,
)
from app.repositories.case_repository import CaseRepository


def build_case(
    case_id: str = "case-001",
    customer_name: str = "John Doe",
    phone_number: str = "08021234567",
    created_by: str = "user-001",
    status: str = "Resolved",
    timestamp: str = "2026-07-11T10:00:00+00:00",
) -> dict:
    """Build a repository test case."""

    return {
        "case_id": case_id,
        "timestamp": timestamp,
        "customer_name": customer_name,
        "phone_number": phone_number,
        "created_by": created_by,
        "result": {
            "status": status,
            "reason": "Repository test investigation.",
            "next_action": "No further action required.",
        },
    }


def test_get_all_cases_returns_empty_collection(
    isolated_repository: CaseRepository,
):

    cases = isolated_repository.get_all_cases()

    assert cases == []


def test_create_case_and_get_all_cases(
    isolated_repository: CaseRepository,
):

    expected_case = build_case()

    isolated_repository.create_case(expected_case)

    cases = isolated_repository.get_all_cases()

    assert cases == [expected_case]


def test_get_case_by_id(
    isolated_repository: CaseRepository,
):

    expected_case = build_case()

    isolated_repository.create_case(expected_case)

    case = isolated_repository.get_case_by_id("case-001")

    assert case == expected_case


def test_get_case_by_id_returns_none_when_missing(
    isolated_repository: CaseRepository,
):

    case = isolated_repository.get_case_by_id("unknown-id")

    assert case is None


def test_search_cases(
    isolated_repository: CaseRepository,
):

    first_case = build_case()

    second_case = build_case(
        case_id="case-002",
        customer_name="Jane Doe",
        phone_number="08029876543",
        status="Waiting",
    )

    isolated_repository.create_case(first_case)
    isolated_repository.create_case(second_case)

    results = isolated_repository.search_cases(
        customer_name="jane doe",
    )

    assert results == [second_case]


def test_query_cases_paginates_results(
    isolated_repository: CaseRepository,
):

    first_case = build_case(
        case_id="case-001",
        timestamp="2026-07-11T10:00:00+00:00",
    )

    second_case = build_case(
        case_id="case-002",
        timestamp="2026-07-11T11:00:00+00:00",
    )

    third_case = build_case(
        case_id="case-003",
        timestamp="2026-07-11T12:00:00+00:00",
    )

    isolated_repository.create_case(first_case)
    isolated_repository.create_case(second_case)
    isolated_repository.create_case(third_case)

    cases, total_records = isolated_repository.query_cases(
        CaseQuery(
            page=2,
            page_size=1,
            sort_by=CaseSortField.TIMESTAMP,
            sort_order=SortOrder.ASC,
        )
    )

    assert total_records == 3
    assert cases == [second_case]


def test_query_cases_returns_total_matching_records(
    isolated_repository: CaseRepository,
):

    isolated_repository.create_case(
        build_case(
            case_id="case-001",
            status="Resolved",
        )
    )

    isolated_repository.create_case(
        build_case(
            case_id="case-002",
            status="Resolved",
        )
    )

    isolated_repository.create_case(
        build_case(
            case_id="case-003",
            status="Waiting",
        )
    )

    cases, total_records = isolated_repository.query_cases(
        CaseQuery(
            page=1,
            page_size=1,
            status=InvestigationStatus.RESOLVED,
        )
    )

    assert total_records == 2
    assert len(cases) == 1


def test_query_cases_sorts_by_customer_name_ascending(
    isolated_repository: CaseRepository,
):

    charlie_case = build_case(
        case_id="case-001",
        customer_name="Charlie Doe",
    )

    alice_case = build_case(
        case_id="case-002",
        customer_name="Alice Doe",
    )

    bob_case = build_case(
        case_id="case-003",
        customer_name="Bob Doe",
    )

    isolated_repository.create_case(charlie_case)
    isolated_repository.create_case(alice_case)
    isolated_repository.create_case(bob_case)

    cases, total_records = isolated_repository.query_cases(
        CaseQuery(
            sort_by=CaseSortField.CUSTOMER_NAME,
            sort_order=SortOrder.ASC,
        )
    )

    assert total_records == 3
    assert [case["customer_name"] for case in cases] == [
        "Alice Doe",
        "Bob Doe",
        "Charlie Doe",
    ]


def test_query_cases_sorts_by_timestamp_descending(
    isolated_repository: CaseRepository,
):

    oldest_case = build_case(
        case_id="case-001",
        timestamp="2026-07-11T10:00:00+00:00",
    )

    newest_case = build_case(
        case_id="case-002",
        timestamp="2026-07-11T12:00:00+00:00",
    )

    middle_case = build_case(
        case_id="case-003",
        timestamp="2026-07-11T11:00:00+00:00",
    )

    isolated_repository.create_case(oldest_case)
    isolated_repository.create_case(newest_case)
    isolated_repository.create_case(middle_case)

    cases, total_records = isolated_repository.query_cases(
        CaseQuery(
            sort_by=CaseSortField.TIMESTAMP,
            sort_order=SortOrder.DESC,
        )
    )

    assert total_records == 3
    assert [case["case_id"] for case in cases] == [
        "case-002",
        "case-003",
        "case-001",
    ]


def test_query_cases_filters_by_status(
    isolated_repository: CaseRepository,
):

    resolved_case = build_case(
        case_id="case-001",
        status="Resolved",
    )

    waiting_case = build_case(
        case_id="case-002",
        status="Waiting",
    )

    isolated_repository.create_case(resolved_case)
    isolated_repository.create_case(waiting_case)

    cases, total_records = isolated_repository.query_cases(
        CaseQuery(
            status=InvestigationStatus.WAITING,
        )
    )

    assert total_records == 1
    assert cases == [waiting_case]


def test_query_cases_filters_by_created_by(
    isolated_repository: CaseRepository,
):

    first_user_case = build_case(
        case_id="case-001",
        created_by="user-001",
    )

    second_user_case = build_case(
        case_id="case-002",
        created_by="user-002",
    )

    isolated_repository.create_case(first_user_case)
    isolated_repository.create_case(second_user_case)

    cases, total_records = isolated_repository.query_cases(
        CaseQuery(
            created_by="user-002",
        )
    )

    assert total_records == 1
    assert cases == [second_user_case]


def test_query_cases_combines_filters(
    isolated_repository: CaseRepository,
):

    matching_case = build_case(
        case_id="case-001",
        customer_name="Jane Doe",
        phone_number="08029876543",
        created_by="user-002",
        status="Escalated",
    )

    wrong_status_case = build_case(
        case_id="case-002",
        customer_name="Jane Doe",
        phone_number="08029876543",
        created_by="user-002",
        status="Resolved",
    )

    other_user_case = build_case(
        case_id="case-003",
        customer_name="Jane Doe",
        phone_number="08029876543",
        created_by="user-003",
        status="Escalated",
    )

    isolated_repository.create_case(matching_case)
    isolated_repository.create_case(wrong_status_case)
    isolated_repository.create_case(other_user_case)

    cases, total_records = isolated_repository.query_cases(
        CaseQuery(
            customer_name="jane doe",
            phone_number="08029876543",
            created_by="user-002",
            status=InvestigationStatus.ESCALATED,
        )
    )

    assert total_records == 1
    assert cases == [matching_case]


def test_query_cases_returns_empty_page_beyond_available_results(
    isolated_repository: CaseRepository,
):

    isolated_repository.create_case(
        build_case(
            case_id="case-001",
        )
    )

    cases, total_records = isolated_repository.query_cases(
        CaseQuery(
            page=3,
            page_size=10,
        )
    )

    assert total_records == 1
    assert cases == []


def test_get_statistics(
    isolated_repository: CaseRepository,
):

    isolated_repository.create_case(
        build_case(
            case_id="case-001",
            status="Resolved",
        )
    )

    isolated_repository.create_case(
        build_case(
            case_id="case-002",
            status="Waiting",
        )
    )

    isolated_repository.create_case(
        build_case(
            case_id="case-003",
            status="Technical Investigation",
        )
    )

    isolated_repository.create_case(
        build_case(
            case_id="case-004",
            status="Escalated",
        )
    )

    statistics = isolated_repository.get_statistics()

    assert statistics == {
        "total_cases": 4,
        "resolved_cases": 1,
        "pending_cases": 2,
        "escalated_cases": 1,
    }
