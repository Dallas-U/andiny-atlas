from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


ExportSource = Literal[
    "reports",
    "analytics",
    "investigations",
]

ExportFormat = Literal[
    "csv",
    "excel",
    "pdf",
]

ExportStatus = Literal[
    "Success",
    "Failed",
]


class ExportAuditRecord(BaseModel):
    """
    Immutable audit record for every exported artifact.
    This is the first implementation of the Andiny Trust Ledger.
    """

    audit_id: str

    export_id: str

    user_id: str

    user_name: str

    role: str

    timestamp_utc: datetime = Field(default_factory=datetime.utcnow)

    source: ExportSource

    export_format: ExportFormat

    file_name: str

    record_count: int

    processing_duration_ms: int

    status: ExportStatus

    checksum: str | None = None

    failure_reason: str | None = None