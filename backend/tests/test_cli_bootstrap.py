"""Tests for initial platform Super Admin bootstrap."""

from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from threading import Barrier

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.cli.bootstrap import create_initial_super_admin
from app.core.constants import UserRole
from app.core.security import hash_password, verify_password
from app.domain import User
from app.exceptions.exceptions import PersistenceDataException
from app.repositories.user_repository import UserRepository


def test_bootstrap_creates_platform_super_admin(
    test_session_factory,
):
    """Create an active, platform-level Super Admin with a hashed password."""
    repository = UserRepository(
        session_factory=test_session_factory,
    )

    password = "StrongTestPassword123!"

    created = create_initial_super_admin(
        repository=repository,
        full_name=" Platform Administrator ",
        email="  ADMIN@EXAMPLE.COM ",
        password=password,
    )

    assert created.full_name == "Platform Administrator"
    assert created.email == "admin@example.com"
    assert created.role == UserRole.SUPER_ADMIN
    assert created.organization_id is None
    assert created.is_active is True
    assert created.hashed_password != password
    assert verify_password(password, created.hashed_password)

    stored = repository.get_user_by_email("admin@example.com")

    assert stored is not None
    assert stored.id == created.id
    assert stored.role == UserRole.SUPER_ADMIN
    assert stored.organization_id is None
    assert repository.has_super_admin()


def test_bootstrap_refuses_when_super_admin_exists(
    test_session_factory,
):
    """Refuse to create a second Super Admin."""
    repository = UserRepository(
        session_factory=test_session_factory,
    )

    create_initial_super_admin(
        repository=repository,
        full_name="First Administrator",
        email="first@example.com",
        password="FirstStrongPassword123!",
    )

    with pytest.raises(
        RuntimeError,
        match="A Super Admin already exists",
    ):
        create_initial_super_admin(
            repository=repository,
            full_name="Second Administrator",
            email="second@example.com",
            password="SecondStrongPassword123!",
        )

    assert repository.get_user_by_email("second@example.com") is None


def test_bootstrap_refuses_existing_non_super_admin_email(
    test_session_factory,
):
    """Do not reuse an email already assigned to another user."""
    repository = UserRepository(
        session_factory=test_session_factory,
    )

    existing_user = User(
        id="existing-user-id",
        full_name="Existing Agent",
        email="agent@example.com",
        hashed_password=hash_password(
            "ExistingAgentPassword123!",
        ),
        role=UserRole.AGENT,
        is_active=True,
        created_at=datetime.now(tz=UTC),
        organization_id=None,
    )

    repository.create_user(existing_user)

    with pytest.raises(
        RuntimeError,
        match="email is already registered",
    ):
        create_initial_super_admin(
            repository=repository,
            full_name="Platform Administrator",
            email="AGENT@example.com",
            password="StrongTestPassword123!",
        )

    stored = repository.get_user_by_email("agent@example.com")

    assert stored is not None
    assert stored.id == existing_user.id
    assert stored.role == UserRole.AGENT
    assert verify_password(
        "ExistingAgentPassword123!",
        stored.hashed_password,
    )
    assert not repository.has_super_admin()


@pytest.mark.parametrize(
    ("full_name", "email", "password", "message"),
    [
        (
            "",
            "admin@example.com",
            "StrongTestPassword123!",
            "Full name is required",
        ),
        (
            "   ",
            "admin@example.com",
            "StrongTestPassword123!",
            "Full name is required",
        ),
        (
            "A" * 151,
            "admin@example.com",
            "StrongTestPassword123!",
            "must not exceed 150 characters",
        ),
        (
            "Platform Administrator",
            "invalid-email",
            "StrongTestPassword123!",
            "valid email address",
        ),
        (
            "Platform Administrator",
            "admin@example.com",
            "short",
            "at least 12 characters",
        ),
        (
            "Platform Administrator",
            "admin@example.com",
            " " * 12,
            "must not be empty",
        ),
    ],
)
def test_bootstrap_rejects_invalid_input(
    test_session_factory,
    full_name,
    email,
    password,
    message,
):
    """Reject invalid input before attempting account creation."""
    repository = UserRepository(
        session_factory=test_session_factory,
    )

    with pytest.raises(ValueError, match=message):
        create_initial_super_admin(
            repository=repository,
            full_name=full_name,
            email=email,
            password=password,
        )

    assert not repository.has_super_admin()


def test_bootstrap_fails_closed_when_atomic_query_fails(
    test_session_factory,
    monkeypatch,
):
    """Do not create an account when the atomic database query fails."""
    repository = UserRepository(
        session_factory=test_session_factory,
    )

    def fail_scalar(self, statement, *args, **kwargs):
        raise SQLAlchemyError("Simulated database query failure.")

    monkeypatch.setattr(Session, "scalar", fail_scalar)

    with pytest.raises(
        PersistenceDataException,
        match="Initial Super Admin creation failed",
    ):
        create_initial_super_admin(
            repository=repository,
            full_name="Platform Administrator",
            email="admin@example.com",
            password="StrongTestPassword123!",
        )

    # Restore normal query behavior before checking persistence.
    monkeypatch.undo()

    assert repository.get_user_by_email("admin@example.com") is None
    assert not repository.has_super_admin()


def test_concurrent_bootstrap_creates_only_one_super_admin(
    test_session_factory,
):
    """Only one simultaneous initial Super Admin bootstrap can succeed."""
    repository_one = UserRepository(
        session_factory=test_session_factory,
    )
    repository_two = UserRepository(
        session_factory=test_session_factory,
    )
    start_barrier = Barrier(2)

    def attempt_bootstrap(
        repository,
        full_name,
        email,
        password,
    ):
        start_barrier.wait(timeout=10)

        try:
            create_initial_super_admin(
                repository=repository,
                full_name=full_name,
                email=email,
                password=password,
            )
            return "created"
        except RuntimeError:
            return "refused"

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_one = executor.submit(
            attempt_bootstrap,
            repository_one,
            "First Administrator",
            "first@example.com",
            "FirstStrongPassword123!",
        )
        future_two = executor.submit(
            attempt_bootstrap,
            repository_two,
            "Second Administrator",
            "second@example.com",
            "SecondStrongPassword123!",
        )

        results = [
            future_one.result(timeout=30),
            future_two.result(timeout=30),
        ]

    assert results.count("created") == 1
    assert results.count("refused") == 1
    assert repository_one.has_super_admin()

    first_user = repository_one.get_user_by_email(
        "first@example.com",
    )
    second_user = repository_one.get_user_by_email(
        "second@example.com",
    )

    assert (first_user is None) != (second_user is None)
