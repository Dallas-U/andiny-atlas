from app.repositories.case_repository import CaseRepository


def build_case(
    case_id: str = "case-001",
    customer_name: str = "John Doe",
    phone_number: str = "08021234567",
    status: str = "Resolved",
) -> dict:
    """Build a repository test case."""

    return {
        "case_id": case_id,
        "timestamp": "2026-07-11T10:00:00+00:00",
        "customer_name": customer_name,
        "phone_number": phone_number,
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
