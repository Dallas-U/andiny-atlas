from fastapi import APIRouter, Depends

from app.dependencies import (
    get_current_user,
    get_report_service,
    require_statistics_viewer,
)
from app.domain import Case, User
from app.models.case_response import (
    CaseResponse,
    InvestigationResult,
)
from app.models.report import (
    InvestigationReportQuery,
    InvestigationReportResponse,
    InvestigationReportSummary,
)
from app.services.report_service import ReportService

router = APIRouter()


def _case_to_response(
    case: Case,
) -> CaseResponse:

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


@router.get(
    "/investigation-summary",
    response_model=InvestigationReportResponse,
    dependencies=[
        Depends(require_statistics_viewer),
    ],
    summary="Generate Investigation Summary Report",
    description=(
        "Returns tenant-scoped investigation totals and matching cases."
    ),
)
def get_investigation_summary_report(
    query: InvestigationReportQuery = Depends(
        InvestigationReportQuery,
    ),
    current_user: User = Depends(
        get_current_user,
    ),
    service: ReportService = Depends(
        get_report_service,
    ),
):

    cases, summary = service.get_investigation_summary(
        start_date=query.start_date,
        end_date=query.end_date,
        status=query.status,
        current_user=current_user,
    )

    return InvestigationReportResponse(
        start_date=query.start_date,
        end_date=query.end_date,
        applied_status=query.status,
        summary=InvestigationReportSummary(
            **summary,
        ),
        items=[
            _case_to_response(case)
            for case in cases
        ],
    )