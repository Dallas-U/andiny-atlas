from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.core.constants import UserRole
from app.domain.branch import Branch
from app.exceptions.exceptions import (
    AuthorizationException,
    PersistenceDataException,
)
from app.repositories.branch_repository import BranchRepository
from app.repositories.organization_repository import OrganizationRepository


class BranchService:
    """
    Business logic for branch management within
    the Andiny Atlas enterprise platform.

    Tenant rule:

    - Customer users may only manage branches belonging
      to their authenticated organization.
    - Super Admin operates at platform scope and may manage
      branches across organizations where permitted.
    - Client-supplied organization_id must never override
      the authenticated tenant scope.
    """

    def __init__(
        self,
        branch_repository: BranchRepository,
        organization_repository: OrganizationRepository,
    ) -> None:
        self.branch_repository = branch_repository
        self.organization_repository = organization_repository

    def create_branch(
        self,
        *,
        organization_id: str,
        name: str,
        code: str,
        city: str,
        state: str,
        current_user_organization_id: str | None = None,
        current_user_role: UserRole | None = None,
    ) -> Branch:
        """
        Create a branch beneath an organization.

        Customer users must provide an organization_id matching
        their authenticated organization.

        Super Admin may provision a branch for any organization.
        """

        self._validate_organization_scope(
            requested_organization_id=organization_id,
            current_user_organization_id=current_user_organization_id,
            current_user_role=current_user_role,
        )

        organization = self.organization_repository.get_by_id(
            organization_id,
        )

        if organization is None:
            raise PersistenceDataException(
                "Organization does not exist."
            )

        if not organization.is_active:
            raise PersistenceDataException(
                "Organization is inactive."
            )

        existing = self.branch_repository.get_by_code(
            code.strip(),
        )

        if existing is not None:
            raise PersistenceDataException(
                "Branch code already exists."
            )

        branch = Branch(
            branch_id=str(uuid4()),
            organization_id=organization_id,
            name=name.strip(),
            code=code.strip(),
            city=city.strip(),
            state=state.strip(),
            is_active=True,
            created_at=datetime.now(UTC),
        )

        return self.branch_repository.create(branch)

    def list_branches(
        self,
        organization_id: str,
        *,
        current_user_organization_id: str | None = None,
        current_user_role: UserRole | None = None,
    ) -> list[Branch]:
        """
        Return branches belonging to an authorized organization.
        """

        self._validate_organization_scope(
            requested_organization_id=organization_id,
            current_user_organization_id=current_user_organization_id,
            current_user_role=current_user_role,
        )

        organization = self.organization_repository.get_by_id(
            organization_id,
        )

        if organization is None:
            raise PersistenceDataException(
                "Organization does not exist."
            )

        return self.branch_repository.list_by_organization(
            organization_id,
        )

    def get_branch(
        self,
        branch_id: str,
        *,
        current_user_organization_id: str | None = None,
        current_user_role: UserRole | None = None,
    ) -> Branch | None:
        """
        Return a branch only when it belongs to the
        authenticated user's organization.

        Super Admin may retrieve branches across organizations.
        """

        branch = self.branch_repository.get_by_id(
            branch_id,
        )

        if branch is None:
            return None

        self._validate_resource_scope(
            resource_organization_id=branch.organization_id,
            current_user_organization_id=current_user_organization_id,
            current_user_role=current_user_role,
        )

        return branch

    @staticmethod
    def _validate_organization_scope(
        *,
        requested_organization_id: str,
        current_user_organization_id: str | None,
        current_user_role: UserRole | None,
    ) -> None:
        """
        Enforce tenant ownership.

        Super Admin is platform-scoped and is therefore permitted
        to operate across organizations.

        Customer users must operate exclusively inside their own
        organization.
        """

        if current_user_role == UserRole.SUPER_ADMIN:
            return

        if current_user_organization_id is None:
            raise AuthorizationException()

        if requested_organization_id != current_user_organization_id:
            raise AuthorizationException()

    @staticmethod
    def _validate_resource_scope(
        *,
        resource_organization_id: str,
        current_user_organization_id: str | None,
        current_user_role: UserRole | None,
    ) -> None:
        """
        Ensure an existing resource belongs to the authenticated
        user's organization.
        """

        if current_user_role == UserRole.SUPER_ADMIN:
            return

        if current_user_organization_id is None:
            raise AuthorizationException()

        if resource_organization_id != current_user_organization_id:
            raise AuthorizationException()