from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database.database import Base
from app.dependencies import get_case_manager
from app.main import app
from app.repositories.case_repository import CaseRepository
from app.services.case_manager import CaseManager


@pytest.fixture
def isolated_repository(
    tmp_path: Path,
) -> Generator[CaseRepository, None, None]:
    """Create a repository backed by an isolated SQLite database."""

    database = tmp_path / "andiny_atlas_test.db"

    engine = create_engine(
        f"sqlite:///{database.as_posix()}",
        connect_args={
            "check_same_thread": False,
        },
    )

    test_session_factory = sessionmaker(
        bind=engine,
        class_=Session,
        autoflush=False,
        expire_on_commit=False,
    )

    Base.metadata.create_all(bind=engine)

    repository = CaseRepository(
        session_factory=test_session_factory,
    )

    try:
        yield repository

    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def client(
    isolated_repository: CaseRepository,
) -> Generator[TestClient, None, None]:
    """Provide a test client with isolated SQLite persistence."""

    case_manager = CaseManager(isolated_repository)

    app.dependency_overrides[get_case_manager] = lambda: case_manager

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.clear()
