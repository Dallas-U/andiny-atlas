from fastapi import APIRouter, Depends

from app.core.constants import UserRole
from app.dependencies import (
    get_case_manager,
    get_current_user,
    get_workflow_engine,
    require_all_cases_viewer,
    require_case_editor,
    require_case_history_viewer,
    require_case_investigator,
    require_own_case_viewer,
    require_statistics_viewer,
)
from app.domain import (
    Case,
    CaseHistory,
    User,
)
from app.exceptions.exceptions import AuthorizationException
from app.models.case_response import (
    CaseResponse,
    InvestigationResult,
)
from app.models.error_response import ErrorResponse
from app.models.history_response import CaseHistoryResponse
from app.models.pagination import (
    PaginatedResponse,
    PaginationMetadata,
)
from app.models.query import CaseQuery
from app.models.statistics import Statistics
from app.models.support_case import SupportCase
from app.models.update_case import UpdateCaseRequest
from app.services.case_manager import (
    CaseManager,
    CasePage,
)
from app.services.workflow_engine import WorkflowEngine

router = APIRouter()


def _case_to_response(
    case: Case,
) -> CaseResponse:
    """Convert a domain case into an API response DTO."""

    return CaseResponse(
        case_id=case.case_id,
        timestamp=case.timestamp.isoformat(),
        customer_name=case.customer.name,
        phone_number=case.customer.phone_number,
        created_by=case.created_by,
        organization_id=case.organization_id,
        branch_id=case.branch_id,
        department_id=case.department_id,
        result=InvestigationResult(
            status=case.result.status,
            reason=case.result.reason,
            next_action=case.result.next_action,
        ),
    )


def _history_to_response(
    history: CaseHistory,
) -> CaseHistoryResponse:
    """Convert a domain history entry into an API response DTO."""

    if history.id is None:
        raise ValueError("A persisted case history entry must have an ID.")

    return CaseHistoryResponse(
        id=history.id,
        case_id=history.case_id,
        status=history.status,
        reason=history.reason,
        next_action=history.next_action,
        changed_by=history.changed_by,
        changed_at=history.changed_at,
    )


def _page_to_response(
    page: CasePage,
) -> PaginatedResponse[CaseResponse]:
    """Convert an application case page into an API response DTO."""

    return PaginatedResponse[CaseResponse](
        metadata=PaginationMetadata(
            page=page.page,
            page_size=page.page_size,
            total_records=page.total_records,
            total_pages=page.total_pages,
            returned_records=page.returned_records,
        ),
        items=[_case_to_response(case) for case in page.cases],
    )


def _organization_scope(
    current_user: User,
    requested_organization_id: str | None = None,
) -> str | None:
    """
    Resolve the organization scope for an operational case request.

    Super Admin operates at platform scope and may explicitly request
    an organization.

    Customer users are always restricted to their authenticated
    organization. A client-supplied organization ID cannot override
    that tenant boundary.
    """

    if current_user.role == UserRole.SUPER_ADMIN:
        return requested_organization_id

    if current_user.organization_id is None:
        raise AuthorizationException()

    if (
        requested_organization_id is not None
        and requested_organization_id != current_user.organization_id
    ):
        raise AuthorizationException()

    return current_user.organization_id


def _authorize_case_access(
    case: Case,
    current_user: User,
) -> None:
    """
    Enforce organization ownership for direct case access.

    Super Admin is platform-scoped.

    Customer users may access only cases belonging to their
    authenticated organization.

    Legacy cases without an organization are not accessible to
    tenant-bound users because they cannot be safely attributed
    to the authenticated organization.
    """

    if current_user.role == UserRole.SUPER_ADMIN:
        return

    if current_user.organization_id is None:
        raise AuthorizationException()

    if case.organization_id != current_user.organization_id:
        raise AuthorizationException()


@router.post(
    "/investigate",
    response_model=CaseResponse,
    dependencies=[
        Depends(require_case_investigator),
    ],
    summary="Investigate Support Case",
    description=(
        "Investigates a customer support case and records the authenticated "
        "user as its creator."
    ),
)
def investigate(
    case: SupportCase,
    engine: WorkflowEngine = Depends(get_workflow_engine),
    case_manager: CaseManager = Depends(get_case_manager),
    current_user: User = Depends(get_current_user),
):
    """
    Investigate a support case within the authenticated user's
    organization scope.
    """

    organization_id = _organization_scope(
        current_user=current_user,
        requested_organization_id=case.organization_id,
    )

    if current_user.role != UserRole.SUPER_ADMIN:
        if case.organization_id is None:
            raise AuthorizationException()

        if case.organization_id != organization_id:
            raise AuthorizationException()

    domain_case = case_manager.investigate_case(
        support_case=case,
        engine=engine,
        created_by=current_user.id,
    )

    return _case_to_response(domain_case)


@router.get(
    "/cases",
    response_model=PaginatedResponse[CaseResponse],
    dependencies=[
        Depends(require_all_cases_viewer),
    ],
    summary="Query Investigation Cases",
    description=("Returns filtered, sorted, and paginated investigation cases."),
)
def get_cases(
    query: CaseQuery = Depends(CaseQuery),
    case_manager: CaseManager = Depends(get_case_manager),
    current_user: User = Depends(get_current_user),
):
    """
    Query investigation cases within the authenticated user's
    organization scope.
    """

    organization_id = _organization_scope(
        current_user=current_user,
        requested_organization_id=query.organization_id,
    )

    scoped_query = query.model_copy(
        update={
            "organization_id": organization_id,
        }
    )

    page = case_manager.query_cases(scoped_query)

    return _page_to_response(page)


@router.get(
    "/my-cases",
    response_model=PaginatedResponse[CaseResponse],
    dependencies=[
        Depends(require_own_case_viewer),
    ],
    summary="Query My Investigation Cases",
    description=(
        "Returns filtered, sorted, and paginated investigation cases "
        "created by the authenticated user."
    ),
)
def get_my_cases(
    query: CaseQuery = Depends(CaseQuery),
    case_manager: CaseManager = Depends(get_case_manager),
    current_user: User = Depends(get_current_user),
):
    """
    Return cases created by the authenticated user while enforcing
    the authenticated user's organization boundary.
    """

    organization_id = _organization_scope(
        current_user=current_user,
        requested_organization_id=query.organization_id,
    )

    ownership_query = query.model_copy(
        update={
            "created_by": current_user.id,
            "organization_id": organization_id,
        }
    )

    page = case_manager.query_cases(
        ownership_query,
    )

    return _page_to_response(page)


@router.get(
    "/cases/{case_id}/history",
    response_model=list[CaseHistoryResponse],
    dependencies=[
        Depends(require_case_history_viewer),
    ],
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Case not found",
        }
    },
    summary="Get Investigation Audit History",
    description=(
        "Returns the immutable audit history for an investigation in "
        "chronological order."
    ),
)
def get_case_history(
    case_id: str,
    case_manager: CaseManager = Depends(get_case_manager),
    current_user: User = Depends(get_current_user),
):
    """
    Return audit history only when the authenticated user is authorized
    to access the associated case.
    """

    domain_case = case_manager.get_case_by_id(case_id)

    _authorize_case_access(
        case=domain_case,
        current_user=current_user,
    )

    history = case_manager.get_case_history(case_id)

    return [_history_to_response(entry) for entry in history]


@router.get(
    "/cases/{case_id}",
    response_model=CaseResponse,
    dependencies=[
        Depends(require_all_cases_viewer),
    ],
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Case not found",
        }
    },
    summary="Get Investigation Case",
    description="Returns one investigation case by its unique ID.",
)
def get_case(
    case_id: str,
    case_manager: CaseManager = Depends(get_case_manager),
    current_user: User = Depends(get_current_user),
):
    """
    Return one investigation case only when it belongs to the
    authenticated customer's organization or the requester is
    Super Admin.
    """

    domain_case = case_manager.get_case_by_id(case_id)

    _authorize_case_access(
        case=domain_case,
        current_user=current_user,
    )

    return _case_to_response(domain_case)


@router.patch(
    "/cases/{case_id}",
    response_model=CaseResponse,
    dependencies=[
        Depends(require_case_editor),
    ],
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Case not found",
        }
    },
    summary="Update Investigation Case",
    description=(
        "Updates an investigation owned by the authenticated user and "
        "records its previous state in the audit history."
    ),
)
def update_case(
    case_id: str,
    request: UpdateCaseRequest,
    case_manager: CaseManager = Depends(get_case_manager),
    current_user: User = Depends(get_current_user),
):
    """
    Update an investigation through the existing ownership-aware
    CaseManager workflow.
    """

    domain_case = case_manager.update_case(
        case_id=case_id,
        status=request.status,
        reason=request.reason,
        next_action=request.next_action,
        current_user_id=current_user.id,
    )

    _authorize_case_access(
        case=domain_case,
        current_user=current_user,
    )

    return _case_to_response(domain_case)


@router.get(
    "/statistics",
    response_model=Statistics,
    dependencies=[
        Depends(require_statistics_viewer),
    ],
    summary="Get Investigation Statistics",
    description="Returns summary statistics for all investigations.",
)
def get_statistics(
    case_manager: CaseManager = Depends(get_case_manager),
):
    return case_manager.get_statistics()