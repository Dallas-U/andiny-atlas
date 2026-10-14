"""Explicit one-time platform Super Admin bootstrap."""

from datetime import UTC, datetime
from getpass import getpass
from uuid import uuid4

from app.core.constants import UserRole
from app.core.security import hash_password
from app.domain import User
from app.repositories.user_repository import UserRepository


MINIMUM_PASSWORD_LENGTH = 12


def create_initial_super_admin(
    repository: UserRepository,
    full_name: str,
    email: str,
    password: str,
) -> User:
    """Create the initial platform Super Admin if none exists."""

    normalized_name = full_name.strip()
    normalized_email = email.strip().lower()

    if not normalized_name:
        raise ValueError("Full name is required.")

    if len(normalized_name) > 150:
        raise ValueError("Full name must not exceed 150 characters.")

    if not normalized_email or len(normalized_email) > 255:
        raise ValueError("A valid email address is required.")

    email_parts = normalized_email.split("@")
    if (
        len(email_parts) != 2
        or not email_parts[0]
        or not email_parts[1]
        or "." not in email_parts[1]
        or email_parts[1].startswith(".")
        or email_parts[1].endswith(".")
    ):
        raise ValueError("A valid email address is required.")

    if len(password) < MINIMUM_PASSWORD_LENGTH:
        raise ValueError("Password must contain at least 12 characters.")

    if not password.strip():
        raise ValueError("Password must not be empty.")

    user = User(
        id=str(uuid4()),
        full_name=normalized_name,
        email=normalized_email,
        hashed_password=hash_password(password),
        role=UserRole.SUPER_ADMIN,
        is_active=True,
        created_at=datetime.now(tz=UTC),
        organization_id=None,
    )

    return repository.create_initial_super_admin_atomically(user)


def bootstrap_super_admin() -> int:
    """Run the interactive initial Super Admin bootstrap."""

    from app.core.settings import settings

    environment = settings.environment.strip().lower()

    print("Andiny Atlas - Initial Super Admin Bootstrap")
    print(f"Configured environment: {environment}")
    print()
    print(
        "This command will attempt to create the first "
        "platform-level Super Admin in the configured database."
    )
    print("It will not create a customer-tenant administrator.")
    print()

    confirmation = input(
        "Type BOOTSTRAP SUPER ADMIN to continue: "
    ).strip()

    if confirmation != "BOOTSTRAP SUPER ADMIN":
        print("Bootstrap cancelled.")
        return 1

    full_name = input("Super Admin full name: ").strip()
    email = input("Super Admin email: ").strip()
    password = getpass("Super Admin password: ")
    password_confirmation = getpass("Confirm password: ")

    if password != password_confirmation:
        print("Bootstrap failed: passwords do not match.")
        return 1

    try:
        repository = UserRepository()

        created_user = create_initial_super_admin(
            repository=repository,
            full_name=full_name,
            email=email,
            password=password,
        )

        print()
        print("Super Admin created successfully.")
        print(f"Account email: {created_user.email}")
        print(f"Role: {created_user.role.value}")
        print("Organization: platform-level (none)")
        print("Password was not displayed or logged.")
        return 0

    except (ValueError, RuntimeError) as exc:
        print(f"Bootstrap refused: {exc}")
        return 1

    except Exception as exc:
        # Avoid printing credentials or raw exception details.
        print(
            "Bootstrap failed. "
            f"Error type: {type(exc).__name__}. "
            "Check application logs and database health."
        )
        return 1
