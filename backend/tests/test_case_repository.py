from pathlib import Path

import pytest

from app.exceptions.exceptions import PersistenceDataException
from app.repositories.case_repository import CaseRepository


def test_load_cases_returns_empty_collection(
    isolated_repository: tuple[CaseRepository, Path],
):

    repository, _database = isolated_repository

    cases = repository.load_cases()

    assert cases == []


def test_save_and_load_cases(
    isolated_repository: tuple[CaseRepository, Path],
):

    repository, _database = isolated_repository

    expected_cases = [
        {
            "case_id": "case-001",
            "timestamp": "2026-07-11T10:00:00+00:00",
            "customer_name": "John Doe",
            "phone_number": "08021234567",
            "result": {
                "status": "Resolved",
                "reason": "Device should unlock successfully.",
                "next_action": "No further action required.",
            },
        }
    ]

    repository.save_cases(expected_cases)

    saved_cases = repository.load_cases()

    assert saved_cases == expected_cases


def test_corrupted_json_raises_persistence_exception(
    isolated_repository: tuple[CaseRepository, Path],
):

    repository, database = isolated_repository

    database.write_text(
        '{"result":',
        encoding="utf-8",
    )

    with pytest.raises(
        PersistenceDataException,
        match="Persisted investigation data is invalid and could not be read.",
    ):
        repository.load_cases()
