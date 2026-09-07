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
    """Provide a Super Admin user for lifecycle tests."""

    return User(
        id="00000000-0000-4000-8000-000000000010",
        full_name="Platform Super Admin",
        email="superadmin@example.com",
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
    """Provide an Agent user for authorization tests."""

    return User(
        id="00000000-0000-4000-8000-000000000011",
        full_name="Support Agent",
        email="agent-lifecycle@example.com",
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
    """Create a test organization through the API."""

    response = client.post(
        "/organizations/",
        json={
            "name": "Lifecycle Test Organization",
            "code": "LIFECYCLE_TEST",
            "industry": "Technology",
            "contact_email": "contact@lifecycle-test.com",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_super_admin_can_deactivate_organization(
    super_admin_client: TestClient,
) -> None:
    """Super Admin can deactivate an organization."""

    organization = create_test_organization(
        super_admin_client,
    )

    organization_id = organization["organization_id"]

    response = super_admin_client.patch(
        f"/organizations/{organization_id}/deactivate",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["organization_id"] == organization_id
    assert body["is_active"] is False


def test_super_admin_can_reactivate_organization(
    super_admin_client: TestClient,
) -> None:
    """Super Admin can reactivate a deactivated organization."""

    organization = create_test_organization(
        super_admin_client,
    )

    organization_id = organization["organization_id"]

    deactivate_response = super_admin_client.patch(
        f"/organizations/{organization_id}/deactivate",
    )

    assert deactivate_response.status_code == 200
    assert deactivate_response.json()["is_active"] is False

    activate_response = super_admin_client.patch(
        f"/organizations/{organization_id}/activate",
    )

    assert activate_response.status_code == 200

    body = activate_response.json()

    assert body["organization_id"] == organization_id
    assert body["is_active"] is True


def test_deactivate_unknown_organization_returns_404(
    super_admin_client: TestClient,
) -> None:
    """Deactivating an unknown organization returns 404."""

    response = super_admin_client.patch(
        "/organizations/unknown-organization/deactivate",
    )

    assert response.status_code == 404

    assert response.json()["detail"] == (
        "Organization not found."
    )


def test_activate_unknown_organization_returns_404(
    super_admin_client: TestClient,
) -> None:
    """Activating an unknown organization returns 404."""

    response = super_admin_client.patch(
        "/organizations/unknown-organization/activate",
    )

    assert response.status_code == 404

    assert response.json()["detail"] == (
        "Organization not found."
    )


def test_agent_cannot_deactivate_organization(
    agent_client: TestClient,
    organization_service: OrganizationService,
) -> None:
    """An Agent cannot deactivate an organization."""

    organization = organization_service.create_organization(
        name="Agent Access Test Organization",
        code="AGENT_ACCESS_TEST",
        industry="Technology",
        contact_email="agent-access@example.com",
    )

    response = agent_client.patch(
        (
            f"/organizations/"
            f"{organization.organization_id}/deactivate"
        ),
    )

    assert response.status_code == 403


def test_agent_cannot_activate_organization(
    agent_client: TestClient,
    organization_service: OrganizationService,
) -> None:
    """An Agent cannot activate an organization."""

    organization = organization_service.create_organization(
        name="Agent Activate Test Organization",
        code="AGENT_ACTIVATE_TEST",
        industry="Technology",
        contact_email="agent-activate@example.com",
    )

    response = agent_client.patch(
        (
            f"/organizations/"
            f"{organization.organization_id}/activate"
        ),
    )


def test_super_admin_can_update_organization_configuration(
    super_admin_client: TestClient,
) -> None:
    """Super Admin can update configurable organization fields."""

    organization = create_test_organization(
        super_admin_client,
    )

    organization_id = organization["organization_id"]

    response = super_admin_client.patch(
        f"/organizations/{organization_id}/configuration",
        json={
            "name": "Updated Lifecycle Organization",
            "industry": "Financial Services",
            "contact_email": "updated@lifecycle-test.com",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["organization_id"] == organization_id
    assert body["name"] == (
        "Updated Lifecycle Organization"
    )
    assert body["industry"] == "Financial Services"
    assert body["contact_email"] == (
        "updated@lifecycle-test.com"
    )


def test_organization_configuration_preserves_code_and_status(
    super_admin_client: TestClient,
) -> None:
    """
    Updating configuration must not modify organization
    identity, code, or lifecycle state.
    """

    organization = create_test_organization(
        super_admin_client,
    )

    organization_id = organization["organization_id"]
    original_code = organization["code"]

    response = super_admin_client.patch(
        f"/organizations/{organization_id}/configuration",
        json={
            "name": "Configuration Preserved Organization",
            "industry": "Healthcare",
            "contact_email": "config@lifecycle-test.com",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["organization_id"] == organization_id
    assert body["code"] == original_code
    assert body["is_active"] is True


def test_organization_configuration_persists(
    super_admin_client: TestClient,
) -> None:
    """Updated organization configuration persists."""

    organization = create_test_organization(
        super_admin_client,
    )

    organization_id = organization["organization_id"]

    update_response = super_admin_client.patch(
        f"/organizations/{organization_id}/configuration",
        json={
            "name": "Persisted Configuration Organization",
            "industry": "Telecommunications",
            "contact_email": "persisted@lifecycle-test.com",
        },
    )

    assert update_response.status_code == 200

    get_response = super_admin_client.get(
        f"/organizations/{organization_id}",
    )

    assert get_response.status_code == 200

    body = get_response.json()

    assert body["name"] == (
        "Persisted Configuration Organization"
    )
    assert body["industry"] == "Telecommunications"
    assert body["contact_email"] == (
        "persisted@lifecycle-test.com"
    )


def test_update_unknown_organization_configuration_returns_404(
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
    """
    An Agent cannot update organization configuration.
    """

    organization = organization_service.create_organization(
        name="Agent Configuration Test Organization",
        code="AGENT_CONFIG_TEST",
        industry="Technology",
        contact_email="agent-config@example.com",
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