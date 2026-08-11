from __future__ import annotations

import hashlib
import time

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.report import InvestigationReportResponse
from app.repositories.export_audit_repository import ExportAuditRepository
from app.services.export_audit_service import ExportAuditService
from app.services.export_generation_service import ExportGenerationService

router = APIRouter()


@router.get(
    "/history",
    summary="Export history",
    description="Return Trust Ledger export audit history.",
)
async def get_export_history():
    audit_service = ExportAuditService(
        ExportAuditRepository(),
    )

    return audit_service.get_history()


def _record_export(
    *,
    report: InvestigationReportResponse,
    content: bytes,
    export_format: str,
    filename: str,
    processing_duration_ms: int,
):
    checksum = hashlib.sha256(
        content,
    ).hexdigest()

    audit_service = ExportAuditService(
        ExportAuditRepository(),
    )

    audit_service.record_export(
        user_id="backend-export-service",
        user_name="Backend Export Service",
        role="System",
        source="reports",
        export_format=export_format,
        file_name=filename,
        record_count=len(report.items),
        processing_duration_ms=processing_duration_ms,
        status="Success",
        checksum=checksum,
    )

    return checksum


@router.post(
    "/report/csv",
    summary="Generate report CSV",
)
async def generate_report_csv(
    report: InvestigationReportResponse,
):
    started_at = time.perf_counter()

    csv_bytes = ExportGenerationService.generate_csv(
        report,
    )

    filename = (
        f"investigation-report-{report.end_date}.csv"
    )

    checksum = _record_export(
        report=report,
        content=csv_bytes,
        export_format="csv",
        filename=filename,
        processing_duration_ms=int(
            (time.perf_counter() - started_at)
            * 1000
        ),
    )

    return StreamingResponse(
        iter([csv_bytes]),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            ),
            "X-Andiny-Checksum": checksum,
            "X-Andiny-Checksum-Algorithm": "SHA-256",
        },
    )


@router.post(
    "/report/excel",
    summary="Generate report Excel",
)
async def generate_report_excel(
    report: InvestigationReportResponse,
):
    started_at = time.perf_counter()

    excel_bytes = ExportGenerationService.generate_excel(
        report,
    )

    filename = (
        f"investigation-report-{report.end_date}.xlsx"
    )

    checksum = _record_export(
        report=report,
        content=excel_bytes,
        export_format="excel",
        filename=filename,
        processing_duration_ms=int(
            (time.perf_counter() - started_at)
            * 1000
        ),
    )

    return StreamingResponse(
        iter([excel_bytes]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            ),
            "X-Andiny-Checksum": checksum,
            "X-Andiny-Checksum-Algorithm": "SHA-256",
        },
    )


@router.post(
    "/report/pdf",
    summary="Generate report PDF",
)
async def generate_report_pdf(
    report: InvestigationReportResponse,
):
    started_at = time.perf_counter()

    pdf_bytes = ExportGenerationService.generate_pdf(
        report,
    )

    filename = (
        f"investigation-report-{report.end_date}.pdf"
    )

    checksum = _record_export(
        report=report,
        content=pdf_bytes,
        export_format="pdf",
        filename=filename,
        processing_duration_ms=int(
            (time.perf_counter() - started_at)
            * 1000
        ),
    )

    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            ),
            "X-Andiny-Checksum": checksum,
            "X-Andiny-Checksum-Algorithm": "SHA-256",
        },
    )