from collections.abc import Callable

from app.services.onboarding_service import OnboardingService
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.constants import UserRole
from app.core.jwt import decode_access_token
from app.domain import User
from app.exceptions.exceptions import (
    AuthorizationException,
    InactiveUserException,
    InvalidTokenException,
)
from app.repositories.case_repository import CaseRepository
from app.repositories.user_repository import UserRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.analytics_repository import AnalyticsRepository
from app.services.analytics_service import AnalyticsService
from app.services.auth_service import AuthService
from app.services.case_manager import CaseManager
from app.services.report_service import ReportService
from app.services.user_administration_service import (
    UserAdministrationService,
)
from app.services.workflow_engine import WorkflowEngine

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    auto_error=False,
)


ROLE_HIERARCHY: dict[UserRole, int] = {
    UserRole.AGENT: 1,
    UserRole.SUPERVISOR: 2,
    UserRole.ADMIN: 3,
    UserRole.SUPER_ADMIN: 4,
}


def get_workflow_engine() -> WorkflowEngine:
    return WorkflowEngine()


def get_case_repository() -> CaseRepository:
    return CaseRepository()


def get_case_manager() -> CaseManager:
    repository = get_case_repository()
    return CaseManager(repository)


def get_report_repository() -> ReportRepository:
    """Create the repository used for reporting queries."""

    return ReportRepository()


def get_report_service() -> ReportService:
    """Create the application service used for reports and analytics."""

    repository = get_report_repository()

    return ReportService(
        repository=repository,
    )

def get_analytics_repository() -> AnalyticsRepository:
    """Create the repository used for analytics queries."""

    return AnalyticsRepository()


def get_analytics_service() -> AnalyticsService:
    """Create the application service used for analytics."""

    repository = get_analytics_repository()

    return AnalyticsService(
        repository=repository,
    )


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_auth_service() -> AuthService:
    repository = get_user_repository()
    return AuthService(repository)

def get_onboarding_service() -> OnboardingService:
    """Create the application service used for customer onboarding."""

    return OnboardingService(
        organization_repository=OrganizationRepository(),
        user_repository=UserRepository(),
    )


def get_user_administration_service() -> UserAdministrationService:
    """Create the application service used for user administration."""

    repository = get_user_repository()

    return UserAdministrationService(
        repository=repository,
    )


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    """Resolve the authenticated user from a bearer token."""

    if token is None:
        raise InvalidTokenException()

    try:
        payload = decode_access_token(token)
    except ValueError as exc:
        raise InvalidTokenException() from exc

    user_id = payload.get("sub")

    if not isinstance(user_id, str) or not user_id:
        raise InvalidTokenException()

    user = auth_service.get_user_by_id(user_id)

    if user is None:
        raise InvalidTokenException()

    if not user.is_active:
        raise InactiveUserException()

    return user


def _has_required_role(
    current_role: UserRole,
    required_role: UserRole,
) -> bool:
    """Return whether a role satisfies the required hierarchy level."""

    current_level = ROLE_HIERARCHY.get(current_role)
    required_level = ROLE_HIERARCHY.get(required_role)

    if current_level is None or required_level is None:
        return False

    return current_level >= required_level


def require_roles(
    *roles: UserRole,
) -> Callable[[User], User]:
    """
    Create a hierarchical role authorization dependency.

    Access is granted when the authenticated user's role satisfies at least
    one of the supplied role requirements.
    """

    if not roles:
        raise ValueError("At least one required role must be provided.")

    def dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        is_authorized = any(
            _has_required_role(
                current_role=current_user.role,
                required_role=required_role,
            )
            for required_role in roles
        )

        if not is_authorized:
            raise AuthorizationException()

        return current_user

    return dependency


def require_super_admin(
    current_user: User = Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
        )
    ),
) -> User:
    """Require Super Admin access."""

    return current_user


def require_admin(
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
        )
    ),
) -> User:
    """Require Admin access or higher."""

    return current_user


def require_supervisor(
    current_user: User = Depends(
        require_roles(
            UserRole.SUPERVISOR,
        )
    ),
) -> User:
    """Require Supervisor access or higher."""

    return current_user


def require_agent(
    current_user: User = Depends(
        require_roles(
            UserRole.AGENT,
        )
    ),
) -> User:
    """Require Agent access or higher."""

    return current_user


def require_admin_or_supervisor(
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
        )
    ),
) -> User:
    """Require Supervisor access or higher."""

    return current_user


def require_case_investigator(
    current_user: User = Depends(
        require_agent,
    ),
) -> User:
    """
    Require permission to investigate support cases.

    Current policy:
    Agent or higher.
    """

    return current_user


def require_own_case_viewer(
    current_user: User = Depends(
        require_agent,
    ),
) -> User:
    """
    Require permission to view cases owned by the authenticated user.

    Current policy:
    Agent or higher.
    """

    return current_user


def require_all_cases_viewer(
    current_user: User = Depends(
        require_supervisor,
    ),
) -> User:
    """
    Require permission to view all investigation cases.

    Current policy:
    Supervisor or higher.
    """

    return current_user


def require_case_history_viewer(
    current_user: User = Depends(
        require_supervisor,
    ),
) -> User:
    """
    Require permission to view case audit history.

    Current policy:
    Supervisor or higher.
    """

    return current_user


def require_case_editor(
    current_user: User = Depends(
        require_agent,
    ),
) -> User:
    """
    Require permission to update an investigation case.

    Current policy:
    Agent or higher.

    Case ownership remains enforced by the application service.
    """

    return current_user


def require_statistics_viewer(
    current_user: User = Depends(
        require_supervisor,
    ),
) -> User:
    """
    Require permission to view investigation statistics.

    Current policy:
    Supervisor or higher.
    """

    return current_user


def require_user_administrator(
    current_user: User = Depends(
        require_admin,
    ),
) -> User:
    """
    Require permission to perform user administration.

    Current policy:
    Admin or higher.
    """

    return current_user


def require_system_governor(
    current_user: User = Depends(
        require_super_admin,
    ),
) -> User:
    """
    Require permission to perform system governance operations.

    Current policy:
    Super Admin only.
    """

    return current_user

def require_tenant_user(
    current_user: User = Depends(
        get_current_user,
    ),
) -> User:
    """
    Require an authenticated tenant-bound user.

    Customer users must have an organization.
    Super Admin is the platform-level exception.
    """

    if (
        current_user.role != UserRole.SUPER_ADMIN
        and current_user.organization_id is None
    ):
        raise AuthorizationException()

    return current_user
