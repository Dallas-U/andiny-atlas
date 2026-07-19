from collections.abc import Generator
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database.database import Base
from app.dependencies import (
    get_auth_service,
    get_case_manager,
    get_current_user,
)
from app.domain import User, UserRole
from app.main import app
from app.repositories.case_repository import CaseRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.case_manager import CaseManager


@pytest.fixture
def test_session_factory(
    tmp_path: Path,
) -> Generator[sessionmaker, None, None]:
    """Provide an isolated SQLite session factory."""

    database = tmp_path / "andiny_atlas_test.db"

    engine = create_engine(
        f"sqlite:///{database.as_posix()}",
        connect_args={
            "check_same_thread": False,
        },
    )

    session_factory = sessionmaker(
        bind=engine,
        class_=Session,
        autoflush=False,
        expire_on_commit=False,
    )

    Base.metadata.create_all(bind=engine)

    try:
        yield session_factory

    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def isolated_repository(
    test_session_factory: sessionmaker,
) -> CaseRepository:
    """Provide an isolated case repository."""

    return CaseRepository(
        session_factory=test_session_factory,
    )


@pytest.fixture
def isolated_user_repository(
    test_session_factory: sessionmaker,
) -> UserRepository:
    """Provide an isolated user repository."""

    return UserRepository(
        session_factory=test_session_factory,
    )


@pytest.fixture
def auth_service(
    isolated_user_repository: UserRepository,
) -> AuthService:
    """Provide an authentication service with isolated persistence."""

    return AuthService(
        isolated_user_repository,
    )


@pytest.fixture
def case_manager(
    isolated_repository: CaseRepository,
) -> CaseManager:
    """Provide a case manager with isolated persistence."""

    return CaseManager(
        isolated_repository,
    )


@pytest.fixture
def supervisor_user() -> User:
    """Provide a Supervisor domain user for authorization tests."""

    return User(
        id="00000000-0000-4000-8000-000000000002",
        full_name="Support Supervisor",
        email="supervisor@example.com",
        hashed_password="not-used-by-test-override",
        is_active=True,
        created_at=datetime(
            2026,
            7,
            19,
            12,
            0,
            tzinfo=UTC,
        ),
        role=UserRole.SUPERVISOR,
    )

@pytest.fixture
def unauthenticated_client(
    case_manager: CaseManager,
    auth_service: AuthService,
) -> Generator[TestClient, None, None]:
    """Provide a client without an authorization token."""

    app.dependency_overrides[get_case_manager] = lambda: case_manager
    app.dependency_overrides[get_auth_service] = lambda: auth_service

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def client(
    case_manager: CaseManager,
    auth_service: AuthService,
) -> Generator[TestClient, None, None]:
    """Provide an authenticated Agent client."""

    app.dependency_overrides[get_case_manager] = lambda: case_manager
    app.dependency_overrides[get_auth_service] = lambda: auth_service

    try:
        with TestClient(app) as test_client:
            registration_response = test_client.post(
                "/auth/register",
                json={
                    "full_name": "Support Agent",
                    "email": "agent@example.com",
                    "password": "MyPassword123",
                },
            )

            assert registration_response.status_code == 201

            login_response = test_client.post(
                "/auth/login",
                json={
                    "email": "agent@example.com",
                    "password": "MyPassword123",
                },
            )

            assert login_response.status_code == 200

            access_token = login_response.json()["access_token"]

            test_client.headers.update(
                {
                    "Authorization": f"Bearer {access_token}",
                }
            )

            yield test_client

    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def supervisor_client(
    case_manager: CaseManager,
    auth_service: AuthService,
    supervisor_user: User,
) -> Generator[TestClient, None, None]:
    """Provide an authenticated Supervisor client."""

    app.dependency_overrides[get_case_manager] = lambda: case_manager
    app.dependency_overrides[get_auth_service] = lambda: auth_service
    app.dependency_overrides[get_current_user] = lambda: supervisor_user

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def auth_client(
    auth_service: AuthService,
) -> Generator[TestClient, None, None]:
    """Provide a test client for authentication endpoints."""

    app.dependency_overrides[get_auth_service] = lambda: auth_service

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.clear()