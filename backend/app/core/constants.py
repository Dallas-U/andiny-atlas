from enum import Enum


class InvestigationStatus(str, Enum):
    """Supported investigation workflow statuses."""

    RESOLVED = "Resolved"
    WAITING = "Waiting"
    TECHNICAL_INVESTIGATION = "Technical Investigation"
    ESCALATED = "Escalated"


class UserRole(str, Enum):
    """Supported application authorization roles."""

    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    SUPERVISOR = "supervisor"
    AGENT = "agent"