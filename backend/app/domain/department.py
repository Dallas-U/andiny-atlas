from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Department:
    """
    Domain representation of a department within a branch.

    A department represents an operational unit belonging
    to a branch inside an organization tenant.
    """

    department_id: str
    organization_id: str
    branch_id: str
    name: str
    code: str
    is_active: bool
    created_at: datetime