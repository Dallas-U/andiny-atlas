from dataclasses import dataclass
from datetime import datetime

from app.core.constants import UserRole


@dataclass(frozen=True, slots=True)
class User:
    """Represents an application user in the domain layer."""

    id: str
    full_name: str
    email: str
    hashed_password: str
    is_active: bool
    created_at: datetime
    role: UserRole = UserRole.AGENT