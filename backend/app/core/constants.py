"""
Application-wide domain values.

This module centralizes values that are reused throughout the project,
preventing duplicated string literals and reducing the risk of invalid
investigation statuses.
"""

from enum import Enum


class InvestigationStatus(str, Enum):
    """Supported investigation case statuses."""

    RESOLVED = "Resolved"
    WAITING = "Waiting"
    TECHNICAL_INVESTIGATION = "Technical Investigation"
    ESCALATED = "Escalated"
