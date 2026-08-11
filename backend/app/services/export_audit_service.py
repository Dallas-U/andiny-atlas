from __future__ import annotations

import hashlib
import time
from datetime import datetime
from uuid import uuid4

from app.domain.export_audit import ExportAudit
from app.repositories.export_audit_repository import (
    ExportAuditRepository,
)


class ExportAuditService:
    """
    Business logic for the Atlas Trust Ledger export audit system.
    """

    def __init__(
        self,
        repository: ExportAuditRepository,
    ) -> None:
        self.repository = repository

    @staticmethod
    def generate_checksum(
        content: bytes,
    ) -> str:
        return hashlib.sha256(content).hexdigest()

    def record_export(
        self,
        *,
        user_id: str,
        user_name: str,
        role: str,
        source: str,
        export_format: str,
        file_name: str,
        record_count: int,
        processing_duration_ms: int,
        status: str,
        content: bytes | None = None,
        failure_reason: str | None = None,
    ) -> ExportAudit:

        checksum = (
            self.generate_checksum(content)
            if content is not None
            else None
        )

        record = ExportAudit(
            audit_id=str(uuid4()),
            export_id=str(uuid4()),
            user_id=user_id,
            user_name=user_name,
            role=role,
            timestamp_utc=datetime.utcnow(),
            source=source,
            export_format=export_format,
            file_name=file_name,
            record_count=record_count,
            processing_duration_ms=processing_duration_ms,
            status=status,
            checksum=checksum,
            failure_reason=failure_reason,
        )

        self.repository.save(record)

        return record

    def get_history(self):
        return self.repository.list_all()