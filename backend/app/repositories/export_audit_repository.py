from __future__ import annotations

from typing import List

from app.domain.export_audit import ExportAudit


class ExportAuditRepository:
    """
    Shared in-memory repository for Trust Ledger export audit records.

    The repository is intentionally shared across all requests so that
    export history remains available while the application is running.

    During Sprint 4.3 this repository will be replaced with persistent
    database storage without changing the service layer.
    """

    _ledger: List[ExportAudit] = []

    def save(
        self,
        record: ExportAudit,
    ) -> None:
        self.__class__._ledger.append(
            record,
        )

    def list_all(self) -> List[ExportAudit]:
        return list(
            self.__class__._ledger,
        )

    def list_by_user(
        self,
        user_id: str,
    ) -> List[ExportAudit]:
        return [
            record
            for record in self.__class__._ledger
            if record.user_id == user_id
        ]