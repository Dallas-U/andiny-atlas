from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ExportAudit:
    audit_id: str
    export_id: str

    user_id: str
    user_name: str
    role: str

    timestamp_utc: datetime

    source: str
    export_format: str

    file_name: str

    record_count: int

    processing_duration_ms: int

    status: str

    checksum: str | None = None

    failure_reason: str | None = None