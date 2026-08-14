from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Organization:
    """
    Domain representation of an organization tenant within
    the Andiny Atlas enterprise platform.

    This model is intentionally aligned with the current
    ORM model and repository layer to preserve architectural
    consistency across Atlas.
    """

    organization_id: str
    name: str
    code: str
    industry: str
    contact_email: str
    is_active: bool
    created_at: datetime