from dataclasses import dataclass
from datetime import UTC, datetime
from math import ceil
from uuid import uuid4

from app.core.constants import UserRole
from app.core.security import hash_password
from app.domain import User
from app.exceptions.exceptions import (
    AuthorizationException,
    PersistenceDataException,
    UserAlreadyExistsException,
)
from app.models.admin import CreateAdminUserRequest
from app.repositories.user_repository import UserRepository


@dataclass(frozen=True, slots=True)
class PaginatedUsers:
    """Domain-friendly result for a paginated user query."""

    users: tuple[User, ...]
    page: int
    page_size: int
    total: int
    total_pages: int


class UserAdministrationService:
    """Application service responsible for user administration."""

    def __init__(
        self,
        repository: UserRepository,
    ):
        self._repository = repository

    def list_users(
        self,
        *,
        current_user: User,
        page: int,
        page_size: int,
    ) -> PaginatedUsers:
        """
        Return users visible to the authenticated administrator.

        Customer administrators are always restricted to their own
        organization.

        Super Admin is platform-scoped and may view users across
        organizations.
        """

        if page < 1:
            raise ValueError(
                "Page must be greater than or equal to 1."
            )

        if page_size < 1:
            raise ValueError(
                "Page size must be greater than or equal to 1."
            )

        organization_id = self._organization_scope(
            current_user,
        )

        offset = (page - 1) * page_size

        users, total = self._repository.list_users(
            offset=offset,
            limit=page_size,
            organization_id=organization_id,
        )

        total_pages = (
            ceil(total / page_size)
            if total > 0
            else 0
        )

        return PaginatedUsers(
            users=tuple(users),
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        )

    def create_user(
        self,
        request: CreateAdminUserRequest,
        *,
        current_user: User,
    ) -> User:
        """
        Provision a new Atlas application user.

        Tenant scope is determined server-side.

        Customer Admin:
            organization_id comes exclusively from current_user.

        Super Admin:
            may explicitly provision a customer user into an
            organization.

        A customer administrator cannot create a Super Admin.
        """

        target_organization_id = self._resolve_creation_scope(
            request=request,
            current_user=current_user,
        )

        normalized_email = request.email.strip().lower()

        existing_user = self._repository.get_user_by_email(
            normalized_email,
            organization_id=target_organization_id,
        )

        if existing_user is not None:
            raise UserAlreadyExistsException(
                normalized_email,
            )

        user = User(
            id=str(uuid4()),
            full_name=request.full_name.strip(),
            email=normalized_email,
            hashed_password=hash_password(
                request.password,
            ),
            is_active=True,
            created_at=datetime.now(UTC),
            role=request.role,
            organization_id=target_organization_id,
        )

        return self._repository.create_user(user)

    def get_user(
        self,
        *,
        user_id: str,
        current_user: User,
    ) -> User | None:
        """
        Return a user within the authenticated user's organization.

        Super Admin is platform-scoped.
        """

        organization_id = self._organization_scope(
            current_user,
        )

        return self._repository.get_user_by_id(
            user_id,
            organization_id=organization_id,
        )

    def change_role(
        self,
        *,
        user_id: str,
        role: UserRole,
        current_user_id: str,
        current_user: User,
    ) -> User:
        """
        Change a user's authorization role.

        Only Super Admin may perform role governance.

        A Super Admin cannot change their own role.
        """

        if current_user.role != UserRole.SUPER_ADMIN:
            raise AuthorizationException()

        if user_id == current_user_id:
            raise AuthorizationException()

        user = self._repository.get_user_by_id(
            user_id,
            organization_id=None,
        )

        if user is None:
            raise PersistenceDataException(
                "User not found."
            )

        updated_user = User(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            created_at=user.created_at,
            role=role,
            organization_id=user.organization_id,
        )

        return self._repository.update_user(
            updated_user,
            organization_id=None,
        )

    def activate_user(
        self,
        *,
        user_id: str,
        current_user: User,
    ) -> User:
        """
        Activate a user within the authenticated administrator's
        organization.
        """

        organization_id = self._organization_scope(
            current_user,
        )

        return self._set_active_state(
            user_id=user_id,
            is_active=True,
            organization_id=organization_id,
        )

    def deactivate_user(
        self,
        *,
        user_id: str,
        current_user_id: str,
        current_user: User,
    ) -> User:
        """
        Deactivate a user.

        A user cannot deactivate their own account.

        Customer administrators can only deactivate users in their
        own organization.
        """

        if user_id == current_user_id:
            raise AuthorizationException()

        organization_id = self._organization_scope(
            current_user,
        )

        return self._set_active_state(
            user_id=user_id,
            is_active=False,
            organization_id=organization_id,
        )

    def _set_active_state(
        self,
        *,
        user_id: str,
        is_active: bool,
        organization_id: str | None,
    ) -> User:
        user = self._repository.get_user_by_id(
            user_id,
            organization_id=organization_id,
        )

        if user is None:
            raise PersistenceDataException(
                "User not found."
            )

        updated_user = User(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=is_active,
            created_at=user.created_at,
            role=user.role,
            organization_id=user.organization_id,
        )

        return self._repository.update_user(
            updated_user,
            organization_id=organization_id,
        )

    @staticmethod
    def _organization_scope(
        current_user: User,
    ) -> str | None:
        """
        Determine server-side tenant scope.

        Customer users are always scoped to their authenticated
        organization.

        Super Admin is platform-scoped.
        """

        if current_user.role == UserRole.SUPER_ADMIN:
            return None

        if not current_user.organization_id:
            raise AuthorizationException()

        return current_user.organization_id

    @staticmethod
    def _resolve_creation_scope(
        *,
        request: CreateAdminUserRequest,
        current_user: User,
    ) -> str | None:
        """
        Resolve the organization for a newly provisioned user.

        Customer administrators cannot choose their tenant.

        Super Admin may provision:
            - a Super Admin without an organization
            - a customer user into an explicit organization
        """

        if current_user.role == UserRole.SUPER_ADMIN:
            if request.role == UserRole.SUPER_ADMIN:
                return None

            if not request.organization_id:
                raise AuthorizationException()

            return request.organization_id

        if not current_user.organization_id:
            raise AuthorizationException()

        if request.role == UserRole.SUPER_ADMIN:
            raise AuthorizationException()

        return current_user.organization_id