from __future__ import annotations

import time

from app.core.export_audit_runtime import export_audit_service


def record_export_runtime(
    *,
    user_id: str,
    user_name: str,
    role: str,
    source: str,
    export_format: str,
    file_name: str,
    record_count: int,
    content: bytes,
    started_at: float,
):
    """
    Helper used by export endpoints to create immutable
    Trust Ledger records.
    """

    duration_ms = int(
        (time.perf_counter() - started_at) * 1000
    )

    return export_audit_service.record_export(
        user_id=user_id,
        user_name=user_name,
        role=role,
        source=source,
        export_format=export_format,
        file_name=file_name,
        record_count=record_count,
        processing_duration_ms=duration_ms,
        status="Success",
        content=content,
    )