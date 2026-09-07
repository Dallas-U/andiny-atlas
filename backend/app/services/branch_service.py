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

        normalized_name = name.strip()
        normalized_code = code.strip().upper()
        normalized_city = city.strip()
        normalized_state = state.strip()

        if not normalized_name:
            raise PersistenceDataException(
                "Branch name is required."
            )

        if not normalized_code:
            raise PersistenceDataException(
                "Branch code is required."
            )

        if not normalized_city:
            raise PersistenceDataException(
                "Branch city is required."
            )

        if not normalized_state:
            raise PersistenceDataException(
                "Branch state is required."
            )

        existing = self.branch_repository.get_by_code(
            normalized_code,
        )

        if existing is not None:
            raise PersistenceDataException(
                "Branch code already exists."
            )

        branch = Branch(
            branch_id=str(uuid4()),
            organization_id=organization_id,
            name=normalized_name,
            code=normalized_code,
            city=normalized_city,
            state=normalized_state,
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

    def activate_branch(
        self,
        branch_id: str,
        *,
        current_user_organization_id: str | None = None,
        current_user_role: UserRole | None = None,
    ) -> Branch:
        """
        Activate a branch within the authenticated tenant scope.
        """

        branch = self._get_authorized_branch(
            branch_id=branch_id,
            current_user_organization_id=current_user_organization_id,
            current_user_role=current_user_role,
        )

        if branch.is_active:
            return branch

        updated_branch = self.branch_repository.update_status(
            branch_id,
            is_active=True,
        )

        if updated_branch is None:
            raise PersistenceDataException(
                "Branch could not be activated."
            )

        return updated_branch

    def deactivate_branch(
        self,
        branch_id: str,
        *,
        current_user_organization_id: str | None = None,
        current_user_role: UserRole | None = None,
    ) -> Branch:
        """
        Deactivate a branch within the authenticated tenant scope.

        Tenant ownership is validated before the status is changed.
        """

        branch = self._get_authorized_branch(
            branch_id=branch_id,
            current_user_organization_id=current_user_organization_id,
            current_user_role=current_user_role,
        )

        if not branch.is_active:
            return branch

        updated_branch = self.branch_repository.update_status(
            branch_id,
            is_active=False,
        )

        if updated_branch is None:
            raise PersistenceDataException(
                "Branch could not be deactivated."
            )

        return updated_branch

    def _get_authorized_branch(
        self,
        *,
        branch_id: str,
        current_user_organization_id: str | None,
        current_user_role: UserRole | None,
    ) -> Branch:
        """
        Load a branch and enforce tenant ownership.
        """

        branch = self.branch_repository.get_by_id(
            branch_id,
        )

        if branch is None:
            raise PersistenceDataException(
                "Branch not found."
            )

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