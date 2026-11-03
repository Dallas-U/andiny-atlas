from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from app.core.constants import InvestigationStatus, UserRole
from app.dependencies import get_case_manager, get_current_user
from app.domain import Case, Customer, InvestigationResult, User
from app.domain.organization import Organization
from app.main import app
from app.repositories.case_repository import CaseRepository


TEST_ORGANIZATION_ID = "00000000-0000-4000-8000-000000000001"
OTHER_ORGANIZATION_ID = "00000000-0000-4000-8000-000000000002"
EMPTY_ORGANIZATION_ID = "00000000-0000-4000-8000-000000000003"


def make_user(role: UserRole, organization_id: str | None) -> User:
    return User(
        id=f"statistics-{role.value}",
        full_name="Statistics Test User",
        email=f"statistics-{role.value}@example.com",
        hashed_password="not-used-by-test",
        is_active=True,
        created_at=datetime.now(UTC),
        role=role,
        organization_id=organization_id,
    )


def make_case(
    case_id: str,
    organization_id: str | None,
    status: InvestigationStatus,
) -> Case:
    return Case(
        case_id=case_id,
        timestamp=datetime.now(UTC),
        customer=Customer(
            name=f"Customer {case_id}",
            phone_number="08020000001",
        ),
        created_by="statistics-test",
        organization_id=organization_id,
        result=InvestigationResult(
            status=status,
            reason="Statistics tenant-scope regression test.",
            next_action="No further action required.",
        ),
    )


@pytest.fixture
def statistics_test_data(
    isolated_repository: CaseRepository,
    isolated_organization_repository,
):
    isolated_organization_repository.create(
        Organization(
            organization_id=TEST_ORGANIZATION_ID,
            name="Test Statistics Organization",
            code="TEST-STAT-ORG",
            industry="Other",
            contact_email="test-statistics@example.com",
            is_active=True,
            created_at=datetime.now(UTC),
        )
    )

    isolated_organization_repository.create(
        Organization(
            organization_id=OTHER_ORGANIZATION_ID,
            name="Other Statistics Organization",
            code="OTHER-STAT-ORG",
            industry="Other",
            contact_email="other-statistics@example.com",
            is_active=True,
            created_at=datetime.now(UTC),
        )
    )

    cases = [
        make_case(
            "stat-tenant-resolved",
            TEST_ORGANIZATION_ID,
            InvestigationStatus.RESOLVED,
        ),
        make_case(
            "stat-tenant-pending",
            TEST_ORGANIZATION_ID,
            InvestigationStatus.WAITING,
        ),
        make_case(
            "stat-other-escalated",
            OTHER_ORGANIZATION_ID,
            InvestigationStatus.ESCALATED,
        ),
        make_case(
            "stat-unassigned-resolved",
            None,
            InvestigationStatus.RESOLVED,
        ),
    ]

    for case in cases:
        isolated_repository.create_case(case)

    return isolated_repository


@pytest.fixture
def statistics_client(
    case_manager,
    auth_service,
):
    app.dependency_overrides[get_case_manager] = lambda: case_manager
    app.dependency_overrides[get_current_user] = lambda: make_user(
        UserRole.SUPERVISOR,
        TEST_ORGANIZATION_ID,
    )

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()


def test_supervisor_statistics_are_organization_scoped(
    statistics_client: TestClient,
    statistics_test_data,
):
    response = statistics_client.get("/support/statistics")

    assert response.status_code == 200
    assert response.json() == {
        "total_cases": 2,
        "resolved_cases": 1,
        "pending_cases": 1,
        "escalated_cases": 0,
    }


def test_admin_statistics_are_organization_scoped(
    statistics_client: TestClient,
    statistics_test_data,
):
    app.dependency_overrides[get_current_user] = lambda: make_user(
        UserRole.ADMIN,
        TEST_ORGANIZATION_ID,
    )

    response = statistics_client.get("/support/statistics")

    assert response.status_code == 200
    assert response.json() == {
        "total_cases": 2,
        "resolved_cases": 1,
        "pending_cases": 1,
        "escalated_cases": 0,
    }


def test_super_admin_statistics_are_platform_wide(
    statistics_client: TestClient,
    statistics_test_data,
):
    app.dependency_overrides[get_current_user] = lambda: make_user(
        UserRole.SUPER_ADMIN,
        None,
    )

    response = statistics_client.get("/support/statistics")

    assert response.status_code == 200
    assert response.json() == {
        "total_cases": 4,
        "resolved_cases": 2,
        "pending_cases": 1,
        "escalated_cases": 1,
    }


def test_admin_without_organization_is_denied_statistics_access(
    statistics_client: TestClient,
    statistics_test_data,
):
    app.dependency_overrides[get_current_user] = lambda: make_user(
        UserRole.ADMIN,
        None,
    )

    response = statistics_client.get("/support/statistics")

    assert response.status_code == 403


def test_empty_tenant_receives_zero_statistics(
    statistics_client: TestClient,
):
    app.dependency_overrides[get_current_user] = lambda: make_user(
        UserRole.SUPERVISOR,
        EMPTY_ORGANIZATION_ID,
    )

    response = statistics_client.get("/support/statistics")

    assert response.status_code == 200
    assert response.json() == {
        "total_cases": 0,
        "resolved_cases": 0,
        "pending_cases": 0,
        "escalated_cases": 0,
    }
