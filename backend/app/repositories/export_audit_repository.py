from __future__ import annotations

from typing import List

from app.domain.export_audit import ExportAudit


class ExportAuditRepository:
    """
    Temporary in-memory repository for export audit records.

    This will later be replaced by persistent database storage.
    """

    def __init__(self) -> None:
        self._records: List[ExportAudit] = []

    def save(self, record: ExportAudit) -> None:
        self._records.append(record)

    def list_all(self) -> List[ExportAudit]:
        return list(self._records)

    def list_by_user(
        self,
        user_id: str,
    ) -> List[ExportAudit]:
        return [
            record
            for record in self._records
            if record.user_id == user_id
        ]