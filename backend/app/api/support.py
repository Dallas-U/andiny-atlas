from fastapi import APIRouter, Depends

from app.database.models import User
from app.dependencies import (
    get_case_manager,
    get_current_user,
    get_workflow_engine,
)
from app.domain import Case
from app.models.case_response import (
    CaseResponse,
    InvestigationResult,
)
from app.models.error_response import ErrorResponse
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

router = APIRouter(
    dependencies=[
        Depends(get_current_user),
    ],
)


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
        result=InvestigationResult(
            status=case.result.status,
            reason=case.result.reason,
            next_action=case.result.next_action,
        ),
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


@router.post(
    "/investigate",
    response_model=CaseResponse,
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
    domain_case = case_manager.investigate_case(
        support_case=case,
        engine=engine,
        created_by=current_user.id,
    )

    return _case_to_response(domain_case)


@router.get(
    "/cases",
    response_model=PaginatedResponse[CaseResponse],
    summary="Query Investigation Cases",
    description=("Returns filtered, sorted, and paginated investigation cases."),
)
def get_cases(
    query: CaseQuery = Depends(CaseQuery),
    case_manager: CaseManager = Depends(get_case_manager),
):
    page = case_manager.query_cases(query)

    return _page_to_response(page)


@router.get(
    "/my-cases",
    response_model=PaginatedResponse[CaseResponse],
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
    ownership_query = query.model_copy(
        update={
            "created_by": current_user.id,
        }
    )

    page = case_manager.query_cases(
        ownership_query,
    )

    return _page_to_response(page)


@router.get(
    "/cases/{case_id}",
    response_model=CaseResponse,
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
):
    domain_case = case_manager.get_case_by_id(
        case_id,
    )

    return _case_to_response(domain_case)


@router.patch(
    "/cases/{case_id}",
    response_model=CaseResponse,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Case not found",
        }
    },
    summary="Update Investigation Case",
    description=("Updates an investigation owned by the authenticated user."),
)
def update_case(
    case_id: str,
    request: UpdateCaseRequest,
    case_manager: CaseManager = Depends(get_case_manager),
    current_user: User = Depends(get_current_user),
):
    domain_case = case_manager.update_case(
        case_id=case_id,
        status=request.status,
        reason=request.reason,
        next_action=request.next_action,
        current_user_id=current_user.id,
    )

    return _case_to_response(domain_case)


@router.get(
    "/statistics",
    response_model=Statistics,
    summary="Get Investigation Statistics",
    description="Returns summary statistics for all investigations.",
)
def get_statistics(
    case_manager: CaseManager = Depends(get_case_manager),
):
    return case_manager.get_statistics()
