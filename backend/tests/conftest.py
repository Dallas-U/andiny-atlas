from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_case_manager
from app.main import app
from app.repositories.case_repository import CaseRepository
from app.services.case_manager import CaseManager


@pytest.fixture
def isolated_repository(tmp_path: Path) -> tuple[CaseRepository, Path]:
    """Create a repository backed by temporary test storage."""

    database = tmp_path / "investigations.json"
    database.write_text(
        "[]",
        encoding="utf-8",
    )

    repository = CaseRepository()
    repository.database = database

    return repository, database


@pytest.fixture
def client(
    isolated_repository: tuple[CaseRepository, Path],
) -> Generator[TestClient, None, None]:
    """Provide a test client with isolated persistence."""

    repository, _database = isolated_repository
    case_manager = CaseManager(repository)

    app.dependency_overrides[get_case_manager] = lambda: case_manager

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.clear()
