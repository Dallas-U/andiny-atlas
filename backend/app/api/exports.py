from fastapi import APIRouter
from pydantic import BaseModel

from app.core.export_audit_runtime import export_audit_service
from app.models.export_audit import ExportAuditRecord

router = APIRouter()


class ExportAuditRequest(BaseModel):
    user_id: str
    user_name: str
    role: str
    source: str
    export_format: str
    file_name: str
    record_count: int
    processing_duration_ms: int
    status: str = "Success"


@router.get(
    "/history",
    response_model=list[ExportAuditRecord],
    summary="Export History",
    description="Returns immutable export audit records.",
)
def get_export_history():
    records = export_audit_service.get_history()

    return [
        ExportAuditRecord(
            audit_id=record.audit_id,
            export_id=record.export_id,
            user_id=record.user_id,
            user_name=record.user_name,
            role=record.role,
            timestamp_utc=record.timestamp_utc,
            source=record.source,
            export_format=record.export_format,
            file_name=record.file_name,
            record_count=record.record_count,
            processing_duration_ms=record.processing_duration_ms,
            status=record.status,
            checksum=record.checksum,
            failure_reason=record.failure_reason,
        )
        for record in records
    ]


@router.post(
    "/audit",
    response_model=ExportAuditRecord,
    summary="Record Export Audit",
    description="Creates an immutable Trust Ledger record for an export operation.",
)
def record_export_audit(request: ExportAuditRequest):
    record = export_audit_service.record_export(
        user_id=request.user_id,
        user_name=request.user_name,
        role=request.role,
        source=request.source,
        export_format=request.export_format,
        file_name=request.file_name,
        record_count=request.record_count,
        processing_duration_ms=request.processing_duration_ms,
        status=request.status,
        content=None,
    )

    return ExportAuditRecord(
        audit_id=record.audit_id,
        export_id=record.export_id,
        user_id=record.user_id,
        user_name=record.user_name,
        role=record.role,
        timestamp_utc=record.timestamp_utc,
        source=record.source,
        export_format=record.export_format,
        file_name=record.file_name,
        record_count=record.record_count,
        processing_duration_ms=record.processing_duration_ms,
        status=record.status,
        checksum=record.checksum,
        failure_reason=record.failure_reason,
    )