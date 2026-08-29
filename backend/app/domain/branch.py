from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Branch:
    """
    Domain representation of a branch within an organization.

    A branch represents a physical or operational location
    belonging to an organization tenant in the Andiny Atlas
    enterprise platform.
    """

    branch_id: str
    organization_id: str
    name: str
    code: str
    city: str
    state: str
    is_active: bool
    created_at: datetime