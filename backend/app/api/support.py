from fastapi import APIRouter, Depends

from app.database.models import User
from app.dependencies import (
    get_case_manager,
    get_current_user,
    get_workflow_engine,
)
from app.models.case_response import CaseResponse
from app.models.error_response import ErrorResponse
from app.models.pagination import PaginatedResponse
from app.models.query import CaseQuery
from app.models.statistics import Statistics
from app.models.support_case import SupportCase
from app.models.update_case import UpdateCaseRequest
from app.services.case_manager import CaseManager
from app.services.workflow_engine import WorkflowEngine

router = APIRouter(
    dependencies=[
        Depends(get_current_user),
    ],
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

    return case_manager.investigate_case(
        case,
        engine,
        current_user,
    )


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

    return case_manager.query_cases(query)


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

    return case_manager.query_cases(
        ownership_query,
    )


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

    return case_manager.get_case_by_id(
        case_id,
    )


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

    return case_manager.update_case(
        case_id=case_id,
        request=request,
        current_user=current_user,
    )


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
