from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database.database import Base
from app.dependencies import (
    get_auth_service,
    get_case_manager,
)
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
def client(
    isolated_repository: CaseRepository,
) -> Generator[TestClient, None, None]:
    """Provide a test client for support endpoints."""

    case_manager = CaseManager(
        isolated_repository,
    )

    app.dependency_overrides[get_case_manager] = lambda: case_manager

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def auth_client(
    isolated_user_repository: UserRepository,
) -> Generator[TestClient, None, None]:
    """Provide a test client for authentication endpoints."""

    auth_service = AuthService(
        isolated_user_repository,
    )

    app.dependency_overrides[get_auth_service] = lambda: auth_service

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.clear()
