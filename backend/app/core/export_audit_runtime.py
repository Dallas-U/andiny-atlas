from app.repositories.export_audit_repository import (
    ExportAuditRepository,
)
from app.services.export_audit_service import (
    ExportAuditService,
)

# Singleton runtime instances for Phase 4.1.
# This will later be replaced by dependency injection.

export_audit_repository = ExportAuditRepository()

export_audit_service = ExportAuditService(
    export_audit_repository,
)