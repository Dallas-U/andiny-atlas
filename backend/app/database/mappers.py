from datetime import UTC, datetime

from app.core.constants import (
    InvestigationStatus,
    UserRole,
)
from app.database.models import (
    CaseHistory as ORMCaseHistory,
)
from app.database.models import (
    Investigation,
    User as ORMUser,
)
from app.domain import (
    Case,
    CaseHistory,
    Customer,
    User,
)
from app.domain import InvestigationResult as DomainInvestigationResult


def _ensure_timezone(
    timestamp: datetime,
) -> datetime:
    """Ensure a datetime has timezone information."""

    if timestamp.tzinfo is None:
        return timestamp.replace(tzinfo=UTC)

    return timestamp


def _to_investigation_status(
    status: InvestigationStatus | str,
) -> InvestigationStatus:
    """Convert a persisted or domain status into an enum value."""

    if isinstance(status, InvestigationStatus):
        return status

    return InvestigationStatus(status)


def _to_user_role(
    role: UserRole | str | None,
) -> UserRole:
    """
    Convert a persisted or domain role into an enum value.

    Users without a stored role are treated as agents. This supports
    legacy records and transient ORM objects whose SQLAlchemy defaults
    have not yet been applied during a database flush.
    """

    if role is None:
        return UserRole.AGENT

    if isinstance(role, UserRole):
        return role

    return UserRole(role)


def investigation_to_case(
    investigation: Investigation,
) -> Case:
    """Convert an ORM investigation into a domain case."""

    return Case(
        case_id=investigation.case_id,
        timestamp=_ensure_timezone(
            investigation.timestamp,
        ),
        customer=Customer(
            name=investigation.customer_name,
            phone_number=investigation.phone_number,
        ),
        created_by=investigation.created_by,
        result=DomainInvestigationResult(
            status=_to_investigation_status(
                investigation.status,
            ),
            reason=investigation.reason,
            next_action=investigation.next_action,
        ),
    )


def case_to_investigation(
    case: Case,
) -> Investigation:
    """Convert a domain case into an ORM investigation."""

    return Investigation(
        case_id=case.case_id,
        timestamp=case.timestamp,
        customer_name=case.customer.name,
        phone_number=case.customer.phone_number,
        created_by=case.created_by,
        status=case.result.status.value,
        reason=case.result.reason,
        next_action=case.result.next_action,
    )


def orm_case_history_to_domain(
    history: ORMCaseHistory,
) -> CaseHistory:
    """Convert an ORM history record into a domain history entry."""

    return CaseHistory(
        id=history.id,
        case_id=history.case_id,
        status=_to_investigation_status(
            history.status,
        ),
        reason=history.reason,
        next_action=history.next_action,
        changed_by=history.changed_by,
        changed_at=_ensure_timezone(
            history.changed_at,
        ),
    )


def domain_case_history_to_orm(
    history: CaseHistory,
) -> ORMCaseHistory:
    """Convert a domain history entry into an ORM history record."""

    if history.id is None:
        raise ValueError(
            "A persisted case history entry must have an ID."
        )

    return ORMCaseHistory(
        id=history.id,
        case_id=history.case_id,
        status=history.status.value,
        reason=history.reason,
        next_action=history.next_action,
        changed_by=history.changed_by,
        changed_at=history.changed_at,
    )


def orm_user_to_domain(
    user: ORMUser,
) -> User:
    """Convert an ORM user into a domain user."""

    return User(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        hashed_password=user.hashed_password,
        is_active=user.is_active,
        created_at=_ensure_timezone(
            user.created_at,
        ),
        role=_to_user_role(
            user.role,
        ),
    )


def domain_user_to_orm(
    user: User,
) -> ORMUser:
    """Convert a domain user into an ORM user."""

    return ORMUser(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        hashed_password=user.hashed_password,
        role=user.role.value,
        is_active=user.is_active,
        created_at=user.created_at,
    )