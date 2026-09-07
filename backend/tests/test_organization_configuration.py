from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.api.organizations import _get_organization_service
from app.dependencies import get_current_user
from app.domain import User, UserRole
from app.main import app
from app.repositories.organization_repository import (
    OrganizationRepository,
)
from app.services.organization_service import (
    OrganizationService,
)


@pytest.fixture
def organization_service(
    isolated_organization_repository: OrganizationRepository,
) -> OrganizationService:
    """Provide an isolated organization service."""

    return OrganizationService(
        isolated_organization_repository,
    )


@pytest.fixture
def super_admin_user() -> User:
    """Provide a Super Admin user."""

    return User(
        id="00000000-0000-4000-8000-000000000020",
        full_name="Platform Super Admin",
        email="superadmin-config@example.com",
        hashed_password="not-used-by-test-override",
        is_active=True,
        created_at=None,
        role=UserRole.SUPER_ADMIN,
    )


@pytest.fixture
def super_admin_client(
    organization_service: OrganizationService,
    super_admin_user: User,
) -> Generator[TestClient, None, None]:
    """Provide an authenticated Super Admin client."""

    app.dependency_overrides[
        _get_organization_service
    ] = lambda: organization_service

    app.dependency_overrides[
        get_current_user
    ] = lambda: super_admin_user

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def agent_user() -> User:
    """Provide an Agent user."""

    return User(
        id="00000000-0000-4000-8000-000000000021",
        full_name="Configuration Test Agent",
        email="agent-config@example.com",
        hashed_password="not-used-by-test-override",
        is_active=True,
        created_at=None,
        role=UserRole.AGENT,
    )


@pytest.fixture
def agent_client(
    organization_service: OrganizationService,
    agent_user: User,
) -> Generator[TestClient, None, None]:
    """Provide an authenticated Agent client."""

    app.dependency_overrides[
        _get_organization_service
    ] = lambda: organization_service

    app.dependency_overrides[
        get_current_user
    ] = lambda: agent_user

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.clear()


def create_test_organization(
    client: TestClient,
) -> dict:
    """Create an organization through the API."""

    response = client.post(
        "/organizations/",
        json={
            "name": "Configuration Test Organization",
            "code": "CONFIG_TEST",
            "industry": "Technology",
            "contact_email": "contact@config-test.com",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_super_admin_can_update_organization_configuration(
    super_admin_client: TestClient,
) -> None:
    """Super Admin can update organization configuration."""

    organization = create_test_organization(
        super_admin_client,
    )

    organization_id = organization["organization_id"]

    response = super_admin_client.patch(
        f"/organizations/{organization_id}/configuration",
        json={
            "name": "Updated Configuration Organization",
            "industry": "Financial Services",
            "contact_email": "updated@config-test.com",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["organization_id"] == organization_id
    assert body["name"] == (
        "Updated Configuration Organization"
    )
    assert body["industry"] == "Financial Services"
    assert body["contact_email"] == (
        "updated@config-test.com"
    )


def test_organization_code_remains_unchanged_after_configuration_update(
    super_admin_client: TestClient,
) -> None:
    """Organization identity code remains unchanged."""

    organization = create_test_organization(
        super_admin_client,
    )

    organization_id = organization["organization_id"]
    original_code = organization["code"]

    response = super_admin_client.patch(
        f"/organizations/{organization_id}/configuration",
        json={
            "name": "Updated Organization Name",
            "industry": "Healthcare",
            "contact_email": "health@config-test.com",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["code"] == original_code


def test_configuration_update_does_not_change_active_status(
    super_admin_client: TestClient,
) -> None:
    """Configuration update must not alter lifecycle state."""

    organization = create_test_organization(
        super_admin_client,
    )

    organization_id = organization["organization_id"]

    deactivate_response = super_admin_client.patch(
        f"/organizations/{organization_id}/deactivate",
    )

    assert deactivate_response.status_code == 200
    assert deactivate_response.json()["is_active"] is False

    response = super_admin_client.patch(
        f"/organizations/{organization_id}/configuration",
        json={
            "name": "Inactive Updated Organization",
            "industry": "Technology",
            "contact_email": "inactive@config-test.com",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["is_active"] is False


def test_updated_configuration_persists_after_retrieval(
    super_admin_client: TestClient,
) -> None:
    """Updated configuration persists after retrieval."""

    organization = create_test_organization(
        super_admin_client,
    )

    organization_id = organization["organization_id"]

    update_response = super_admin_client.patch(
        f"/organizations/{organization_id}/configuration",
        json={
            "name": "Persistent Configuration Organization",
            "industry": "Real Estate",
            "contact_email": "persistent@config-test.com",
        },
    )

    assert update_response.status_code == 200

    get_response = super_admin_client.get(
        f"/organizations/{organization_id}",
    )

    assert get_response.status_code == 200

    body = get_response.json()

    assert body["name"] == (
        "Persistent Configuration Organization"
    )
    assert body["industry"] == "Real Estate"
    assert body["contact_email"] == (
        "persistent@config-test.com"
    )


def test_update_unknown_organization_returns_404(
    super_admin_client: TestClient,
) -> None:
    """Updating an unknown organization returns 404."""

    response = super_admin_client.patch(
        "/organizations/unknown-organization/configuration",
        json={
            "name": "Unknown Organization",
            "industry": "Technology",
            "contact_email": "unknown@example.com",
        },
    )

    assert response.status_code == 404

    assert response.json()["detail"] == (
        "Organization not found."
    )


def test_agent_cannot_update_organization_configuration(
    agent_client: TestClient,
    organization_service: OrganizationService,
) -> None:
    """An Agent cannot update organization configuration."""

    organization = organization_service.create_organization(
        name="Agent Configuration Test Organization",
        code="AGENT_CONFIG_TEST",
        industry="Technology",
        contact_email="agent-org@example.com",
    )

    response = agent_client.patch(
        (
            f"/organizations/"
            f"{organization.organization_id}/configuration"
        ),
        json={
            "name": "Unauthorized Update",
            "industry": "Finance",
            "contact_email": "unauthorized@example.com",
        },
    )

    assert response.status_code == 403