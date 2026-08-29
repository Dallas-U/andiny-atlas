"""Development user seeding operations."""

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from pydantic import SecretStr

from app.core.constants import UserRole
from app.core.security import hash_password
from app.core.settings import settings
from app.domain import User
from app.repositories.user_repository import UserRepository


@dataclass(frozen=True, slots=True)
class SeedAccount:
    """Configuration for one development account."""

    full_name: str
    email: str
    password: SecretStr
    role: UserRole


@dataclass(frozen=True, slots=True)
class SeedSummary:
    """Summary of a development user seed operation."""

    created: int
    existing: int


def _ensure_seeding_is_allowed() -> None:
    """Prevent development seed data from being created accidentally."""

    environment = settings.environment.strip().lower()

    allowed_environments = {
        "development",
        "dev",
        "local",
        "test",
        "testing",
    }

    if environment not in allowed_environments:
        raise RuntimeError(
            "Development user seeding is not allowed in environment "
            f"'{settings.environment}'."
        )

    if not settings.allow_development_seed:
        raise RuntimeError(
            "Development user seeding is disabled. "
            "Set ALLOW_DEVELOPMENT_SEED=true to enable it."
        )


def _required_password(
    password: SecretStr | None,
    variable_name: str,
) -> SecretStr:
    """Return a configured seed password or raise a clear error."""

    if password is None:
        raise RuntimeError(f"{variable_name} must be configured before seeding users.")

    plain_password = password.get_secret_value()

    if len(plain_password) < 12:
        raise RuntimeError(f"{variable_name} must contain at least 12 characters.")

    return password


def _build_seed_accounts() -> tuple[SeedAccount, ...]:
    """Build the standard development account definitions."""

    return (
        SeedAccount(
            full_name=settings.seed_super_admin_name,
            email=settings.seed_super_admin_email.strip().lower(),
            password=_required_password(
                settings.seed_super_admin_password,
                "SEED_SUPER_ADMIN_PASSWORD",
            ),
            role=UserRole.SUPER_ADMIN,
        ),
        SeedAccount(
            full_name=settings.seed_admin_name,
            email=settings.seed_admin_email.strip().lower(),
            password=_required_password(
                settings.seed_admin_password,
                "SEED_ADMIN_PASSWORD",
            ),
            role=UserRole.ADMIN,
        ),
        SeedAccount(
            full_name=settings.seed_supervisor_name,
            email=settings.seed_supervisor_email.strip().lower(),
            password=_required_password(
                settings.seed_supervisor_password,
                "SEED_SUPERVISOR_PASSWORD",
            ),
            role=UserRole.SUPERVISOR,
        ),
        SeedAccount(
            full_name=settings.seed_agent_name,
            email=settings.seed_agent_email.strip().lower(),
            password=_required_password(
                settings.seed_agent_password,
                "SEED_AGENT_PASSWORD",
            ),
            role=UserRole.AGENT,
        ),
    )


def _seed_accounts(
    repository: UserRepository,
    accounts: tuple[SeedAccount, ...],
) -> SeedSummary:
    """Create accounts that do not already exist."""

    created = 0
    existing = 0

    for account in accounts:
        saved_user = repository.get_user_by_email(
            account.email,
        )

        if saved_user is not None:
            existing += 1

            print(f"[EXISTS] {account.email} (stored role: {saved_user.role.value})")

            if saved_user.role != account.role:
                print(
                    "         Warning: expected role "
                    f"'{account.role.value}', but the stored role is "
                    f"'{saved_user.role.value}'."
                )

            continue

        user = User(
            id=str(uuid4()),
            full_name=account.full_name.strip(),
            email=account.email,
            hashed_password=hash_password(
                account.password.get_secret_value(),
            ),
            role=account.role,
            is_active=True,
            created_at=datetime.now(tz=UTC),
        )

        repository.create_user(user)

        created += 1

        print(f"[CREATED] {account.email} (role: {account.role.value})")

    return SeedSummary(
        created=created,
        existing=existing,
    )


def seed_development_users() -> int:
    """Create the standard development users."""

    try:
        _ensure_seeding_is_allowed()

        accounts = _build_seed_accounts()
        repository = UserRepository()

        print("Seeding Andiny Atlas development users...")

        summary = _seed_accounts(
            repository,
            accounts,
        )

        print()
        print("Development user seed completed.")
        print(f"Created: {summary.created}")
        print(f"Already existed: {summary.existing}")
        print(f"Total processed: {summary.created + summary.existing}")

        return 0

    except RuntimeError as exc:
        print(f"Seed configuration error: {exc}")
        return 1

    except Exception as exc:
        print(f"Development user seeding failed: {type(exc).__name__}: {exc}")
        return 1
