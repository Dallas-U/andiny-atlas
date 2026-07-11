# Engineering Handbook

# Volume III – Sprint Journal

**Version:** 1.3 (Living Document)

**Project:** Andiny Atlas

**Author:** Dallas Uzo

---

# Purpose

This volume records the engineering history of Andiny Atlas.

Unlike the other handbook volumes, which describe permanent engineering principles and architecture, this journal documents the evolution of the project one sprint at a time.

Each sprint captures:

- Objectives
- Features implemented
- Architectural improvements
- Challenges encountered
- Lessons learned
- Engineering milestones
- Git commit
- Release tag

Together, these entries provide a complete engineering timeline of the project.

---

# Table of Contents

1. Sprint 10
2. Sprint 11
3. Sprint 12
4. Sprint 13
5. Sprint 14
6. Sprint 15
7. Sprint 16
8. Sprint 17

---

# Sprint 10

## Objectives

- Introduce typed workflow responses using Pydantic.
- Add investigation statistics endpoint.
- Improve service-layer type safety.
- Expand automated API testing.

---

## Features Implemented

- Added `InvestigationResult` model.
- Replaced dictionary workflow responses with typed objects.
- Added `/support/statistics` endpoint.
- Added `Statistics` response model.
- Updated `CaseManager` to serialize models using `model_dump()`.
- Migrated timestamps to timezone-aware UTC.

---

## Architectural Improvements

- Stronger contract between the service layer and API layer.
- Reduced use of raw dictionaries.
- Improved response consistency.
- Better preparation for future database migration.

---

## Challenges Encountered

- Diagnosed JSON corruption caused by an incomplete investigation record.
- Learned to troubleshoot `JSONDecodeError`.
- Corrected serialization using `model_dump()`.

---

## Lessons Learned

- Pydantic models are preferable to raw dictionaries.
- Type safety significantly reduces defects.
- Pytest stack traces identify failures precisely.
- Data persistence must always produce valid JSON.

---

## Sprint Outcome

✅ Sprint completed successfully.

---

## Engineering Milestone

At the completion of Sprint 10, Andiny Atlas included:

- FastAPI
- Dependency Injection
- Repository Pattern
- Business Services
- Exception Handling
- Custom Error Models
- Search API
- Statistics API
- Automated Testing
- Black Formatter
- Git Workflow
- Engineering Handbook
- Typed Service Layer
- Release Tags

---

## Commit

```text
feat(sprint-10): introduce typed workflow responses and statistics endpoint
```

---

## Release Tag

```text
v0.10.0
```

---

# Sprint 11

## Objectives

- Introduce centralized application logging.
- Improve backend observability.
- Record business decisions during investigations.
- Improve operational visibility without changing business behavior.

---

## Features Implemented

- Added centralized logger.
- Added repository logging.
- Added Case Manager logging.
- Added Workflow Engine logging.
- Standardized INFO-level log messages.
- Verified functionality using automated tests.

---

## Architectural Improvements

- Introduced structured logging across all application layers.
- Improved traceability of business operations.
- Increased production readiness through better observability.

---

## Challenges Encountered

- Corrected logging placement within service methods.
- Fixed indentation issues introduced during implementation.
- Resolved syntax issues detected by automated testing.

---

## Lessons Learned

- Logging is part of application architecture.
- Clear logs dramatically simplify debugging.
- Operational visibility is as important as clean code.

---

## Sprint Outcome

✅ Sprint completed successfully.

---

## Engineering Milestone

At the completion of Sprint 11, Andiny Atlas included:

- Layered Architecture
- Dependency Injection
- Repository Pattern
- Structured Exception Handling
- Automated Testing
- Centralized Logging

These capabilities established a strong foundation for future production deployment.

---

## Commit

```text
feat(sprint-11): add structured logging across application
```

---

## Release Tag

```text
v0.11.0
```

---

# Sprint 12

## Objectives

- Centralize application configuration.
- Introduce environment variable support.
- Remove hard-coded configuration.
- Improve deployment readiness.

---

## Features Implemented

- Added centralized `Settings` model.
- Introduced `.env` configuration.
- Added application environment support.
- Centralized FastAPI metadata.
- Centralized database configuration.
- Repository now retrieves configuration through the settings layer.

---

## Architectural Improvements

- Configuration separated from business logic.
- Single source of truth for application settings.
- Improved deployment flexibility.
- Better preparation for cloud environments.

---

## Challenges Encountered

- Reviewed existing configuration to eliminate duplication.
- Preserved compatibility with existing application behavior.
- Updated configuration without affecting automated tests.

---

## Lessons Learned

- Configuration is infrastructure.
- Environment variables improve deployment flexibility.
- Infrastructure concerns should remain separate from business logic.
- Centralized configuration simplifies long-term maintenance.

---

## Sprint Outcome

✅ Sprint completed successfully.

---

## Engineering Milestone

At the completion of Sprint 12, Andiny Atlas now includes:

- FastAPI
- Layered Architecture
- Dependency Injection
- Repository Pattern
- Service Layer
- Structured Exception Handling
- Typed Pydantic Models
- Automated Testing
- Structured Logging
- Centralized Configuration
- Environment Variable Support
- Engineering Handbook

The project now follows many of the architectural practices used in modern production backend systems.

---

## Commit

```text
feat(sprint-12): introduce centralized configuration
```

---

## Release Tag

```text
v0.12.0
```

---

# Sprint 13

## Objectives

- Centralize domain-level investigation status values.
- Introduce a service composition container.
- Reduce duplicated business strings across the codebase.
- Improve readability through shared type aliases.
- Prepare the project for future workflow expansion.

---

## Features Implemented

- Added `app/core/constants.py`.
- Added centralized investigation status constants.
- Added `app/core/container.py`.
- Added a `ServiceContainer` for service composition.
- Added `app/core/types.py`.
- Added shared type aliases for case-related dictionaries.
- Added `app/workflows/__init__.py` as a future workflow package placeholder.
- Updated `WorkflowEngine` to use centralized status constants.
- Updated `CaseManager` statistics logic to use centralized constants.
- Updated repository typing and service typing foundations.

---

## Architectural Improvements

- Reduced duplicated domain strings.
- Improved consistency across workflow, statistics, and tests.
- Introduced a composition root for application services.
- Prepared the codebase for future workflow modularization.
- Improved code readability with named type aliases.

---

## Challenges Encountered

- Clarified that the `workflows` package should remain a placeholder for now.
- Avoided premature abstraction before a real workflow-splitting need exists.
- Kept Sprint 13 focused on completed backend architecture work only.

---

## Lessons Learned

- Business values should have one authoritative definition.
- Constants reduce typo-related defects.
- A service container centralizes object creation.
- Placeholder packages can communicate future architectural intent.
- Not every planned abstraction should be implemented immediately.

---

## Sprint Outcome

✅ Sprint completed successfully.

---

## Engineering Milestone

Sprint 13 introduced stronger domain consistency and service composition.

At this stage, Andiny Atlas now includes:

- Layered Architecture
- Dependency Injection
- Repository Pattern
- Service Container
- Centralized Domain Constants
- Shared Type Aliases
- Structured Exception Handling
- Typed Pydantic Models
- Automated Testing
- Structured Logging
- Centralized Configuration
- Environment Variable Support
- Engineering Handbook

---

## Commit

```text
refactor(sprint-13): centralize domain constants and service composition
16bf89e
v0.13.0

# Sprint 14

## Objectives

- Introduce a typed domain model for investigation statuses.
- Prevent unsupported investigation status values.
- Replace plain status strings with a controlled enumeration.
- Preserve the existing public API response contract.
- Strengthen validation through automated testing.

---

## Features Implemented

- Added the `InvestigationStatus` enum.
- Defined supported investigation statuses as explicit domain values.
- Updated `InvestigationResult` to require `InvestigationStatus`.
- Updated `WorkflowEngine` to use enum members directly.
- Updated `CaseManager` to convert persisted status strings into the domain enum.
- Removed transitional `STATUS_*` aliases.
- Updated API tests to use the typed status model.
- Added an automated test proving invalid investigation statuses are rejected.

---

## Architectural Improvements

Sprint 14 strengthened the investigation domain model.

Previously, investigation statuses were represented as unrestricted strings.

```python
status: str
```

This allowed any string value to enter the model, including unsupported values.

The application now uses:

```python
status: InvestigationStatus
```

Supported statuses are explicitly defined as:

```text
Resolved
Waiting
Technical Investigation
Escalated
```

This creates a stronger contract between the workflow engine, service layer, persistence layer, and API models.

---

## Domain Validation

Before Sprint 14, the following value could be accepted by the model:

```python
status="Invalid Status"
```

The application had no model-level mechanism for rejecting it.

After Sprint 14, Pydantic validates the value against `InvestigationStatus`.

Unsupported statuses now raise a validation error.

This behavior is protected by an automated test.

---

## Persistence Compatibility

Investigation records are currently stored in JSON.

JSON stores investigation statuses as strings.

For example:

```json
{
    "status": "Resolved"
}
```

When persisted records are processed by `CaseManager`, the stored string is converted back into the domain enum:

```python
status = InvestigationStatus(
    case["result"]["status"],
)
```

This allows the application to maintain a typed domain model while preserving the existing JSON storage format.

---

## API Compatibility

The introduction of `InvestigationStatus` did not change the public API response format.

The API continues to return:

```json
{
    "status": "Resolved"
}
```

Enum values are serialized using their string values.

This allowed the internal domain model to become stricter without introducing a breaking API change.

---

## Challenges Encountered

- Migrated status handling incrementally to avoid breaking existing modules.
- Temporarily retained `STATUS_*` aliases while production code was migrated.
- Verified that enum serialization preserved the existing API contract.
- Updated statistics logic to interpret persisted strings as domain enum values.
- Ensured tests validated both successful API behavior and invalid domain values.

---

## Lessons Learned

- Centralized constants reduce duplication, but typed domain values provide stronger guarantees.
- Domain models should reject invalid states as early as possible.
- Enums make business concepts explicit.
- Internal architectural improvements do not always require public API changes.
- Incremental migration reduces the risk of large refactoring work.
- Automated tests should verify both valid behavior and rejected invalid behavior.

---

## Sprint Outcome

✅ Sprint completed successfully.

Automated test coverage increased from:

```text
3 tests
```

to:

```text
4 tests
```

Final verification:

```text
4 passed
```

---

## Engineering Milestone

Sprint 14 marks the introduction of a stronger domain model into Andiny Atlas.

The application now includes:

- Layered Architecture
- Dependency Injection
- Repository Pattern
- Service Container
- Centralized Configuration
- Environment Variable Support
- Structured Logging
- Structured Exception Handling
- Typed Pydantic Models
- Typed Investigation Status Domain Model
- Enum-Based Business Values
- JSON Persistence Compatibility
- Automated Validation Testing
- Shared Type Aliases
- Engineering Handbook
- Semantic Git History
- Release Tags

Andiny Atlas no longer treats investigation status as arbitrary text.

Investigation status is now an explicit business concept enforced by the application.

---

## Commit

```text
refactor(sprint-14): introduce typed investigation statuses
```

---

## Commit Hash

```text
31524e0
```

---

## Release Tag

```text
v0.14.0
```

# Sprint 15

## Objectives

- Detect corrupted persisted investigation data.
- Prevent low-level JSON errors from leaking through the API.
- Introduce an application-specific persistence exception.
- Return a standardized API error for persistence failures.
- Add isolated automated coverage for corrupted JSON data.

---

## Features Implemented

- Added `PersistenceDataException`.
- Added `persistence_data_handler`.
- Registered the persistence exception handler globally in FastAPI.
- Updated `CaseRepository` to catch `JSONDecodeError`.
- Translated low-level JSON parsing failures into an application-specific exception.
- Added explicit UTF-8 encoding for repository file operations.
- Added isolated corruption testing using pytest's `tmp_path`.
- Added FastAPI dependency overrides for test-specific repository injection.
- Added a controlled-error API test using `raise_server_exceptions=False`.

---

## Architectural Improvements

Sprint 15 strengthened the boundary between persistence infrastructure and application behavior.

Previously, corrupted JSON caused a raw Python exception:

```text
JSONDecodeError
```

That exception leaked through the application and could cause endpoints to fail without a standardized response.

The repository now translates the low-level infrastructure error into:

```text
PersistenceDataException
```

The global FastAPI exception handler then converts it into a controlled API response.

```text
Corrupted JSON
      │
      ▼
JSONDecodeError
      │
      ▼
PersistenceDataException
      │
      ▼
Global Exception Handler
      │
      ▼
HTTP 500 JSON Response
```

---

## Standardized Error Response

When persisted investigation data cannot be read safely, the API now returns:

```json
{
  "error": {
    "code": "PERSISTENCE_DATA_ERROR",
    "message": "Persisted investigation data is invalid and could not be read."
  }
}
```

The response uses:

```text
HTTP 500 Internal Server Error
```

This is appropriate because the failure originates from the server's persisted state rather than from invalid client input.

---

## Repository Exception Translation

The repository now catches:

```python
JSONDecodeError
```

and raises:

```python
PersistenceDataException
```

using exception chaining:

```python
raise PersistenceDataException(
    "Persisted investigation data is invalid and could not be read."
) from exc
```

Exception chaining preserves the original failure for logs and debugging while exposing a clean application-level error to higher layers.

---

## Test Isolation

The corruption test does not modify the real application data file.

Pytest creates a temporary file using:

```python
tmp_path
```

The test then injects a temporary `CaseRepository` through FastAPI's dependency override mechanism.

This ensures:

- The real `data/investigations.json` remains untouched.
- The corruption scenario is reproducible.
- Test cleanup happens automatically.
- The test suite remains safe and isolated.

---

## Challenges Encountered

- The first corruption test caused `TestClient` to re-raise the server exception.
- A dedicated client was required with:

```python
raise_server_exceptions=False
```

- The persistence handler initially existed but was not registered in `main.py`.
- FastAPI returned plain `Internal Server Error` text until the handler was registered.
- The issue was resolved by tracing the complete exception path rather than changing the repository unnecessarily.

---

## Lessons Learned

- Infrastructure errors should be translated at architectural boundaries.
- Custom exceptions create cleaner contracts between layers.
- Exception handlers must be explicitly registered.
- A test client may re-raise server exceptions unless configured otherwise.
- Automated tests should never corrupt real application data.
- Temporary files and dependency overrides are essential for safe integration testing.
- Logs should preserve low-level failure details while clients receive standardized responses.

---

## Sprint Outcome

✅ Sprint completed successfully.

Automated test coverage increased from:

```text
4 tests
```

to:

```text
5 tests
```

Final verification:

```text
5 passed
```

---

## Engineering Milestone

Sprint 15 introduced persistence resilience into Andiny Atlas.

The application now includes:

- Layered Architecture
- Dependency Injection
- Repository Pattern
- Service Container
- Centralized Configuration
- Environment Variable Support
- Structured Logging
- Structured Exception Handling
- Typed Pydantic Models
- Typed Investigation Status Domain Model
- Persistence Exception Translation
- Standardized Persistence Error Responses
- Isolated Repository Failure Testing
- Automated Validation Testing
- Shared Type Aliases
- Engineering Handbook
- Semantic Git History
- Release Tags

Andiny Atlas can now detect corrupted JSON persistence data and respond predictably instead of leaking raw infrastructure errors.

---

## Commit

```text
fix(sprint-15): add resilient persistence error handling
```

---

## Commit Hash

```text
1072a57
```

---

## Release Tag

```text
v0.15.0
```
# Sprint 16

## Objectives

- Isolate automated tests from production data.
- Introduce reusable pytest fixtures.
- Separate test infrastructure from test implementation.
- Add repository-level unit tests.
- Improve the maintainability and scalability of the test suite.

---

## Features Implemented

- Introduced a shared `tests/conftest.py`.
- Added reusable `isolated_repository` fixture.
- Added reusable `client` fixture using FastAPI dependency overrides.
- Migrated API tests to isolated persistence.
- Added repository unit tests.
- Separated test infrastructure from test behavior.
- Eliminated writes to the production `investigations.json` during automated testing.

---

## Architectural Improvements

Sprint 16 established a dedicated testing architecture.

Previously, every API test interacted with the application's default repository.

```text
API Test
    │
    ▼
CaseRepository
    │
    ▼
data/investigations.json
```

This caused automated tests to modify production development data.

The new testing architecture introduces isolated persistence.

```text
API Test
    │
    ▼
Shared Fixture
    │
    ▼
Temporary Repository
    │
    ▼
pytest tmp_path
```

Every test now receives its own temporary JSON database.

The production data file remains untouched.

---

## Test Infrastructure

Shared fixtures now reside inside:

```text
tests/conftest.py
```

Pytest automatically discovers these fixtures without requiring imports inside each test module.

The shared fixtures provide:

- Temporary repository creation.
- Temporary JSON storage.
- Dependency override management.
- Automatic cleanup.
- Shared FastAPI test client.

This significantly reduces duplicated setup code.

---

## Repository Unit Tests

Sprint 16 introduced repository-focused testing.

Current repository tests verify:

- Loading an empty investigation collection.
- Saving investigation records.
- Reloading persisted investigation records.
- Detecting corrupted JSON.
- Raising `PersistenceDataException`.

These tests validate persistence behavior independently of FastAPI.

---

## Test Suite Structure

The testing structure now follows professional pytest conventions.

```text
tests/
├── conftest.py
├── test_case_repository.py
└── test_support.py
```

Responsibilities are now clearly separated.

| Module | Responsibility |
|---------|----------------|
| `conftest.py` | Shared fixtures |
| `test_case_repository.py` | Repository behavior |
| `test_support.py` | API behavior |

---

## Challenges Encountered

Initially, automated tests modified the real application database.

Although temporary repositories had already been introduced for one scenario, the remaining API tests still used the production repository.

The solution was to move shared setup into reusable pytest fixtures and inject temporary repositories into every API test.

---

## Lessons Learned

- Automated tests should never modify production data.
- Test infrastructure deserves the same architectural attention as production code.
- Shared fixtures reduce duplication.
- Dependency overrides make integration tests deterministic.
- Repository unit tests complement API integration tests.
- Clear separation between fixtures and test cases improves maintainability.

---

## Sprint Outcome

✅ Sprint completed successfully.

The automated test suite now contains:

- Repository unit tests.
- API integration tests.
- Domain validation tests.
- Persistence failure tests.

Final verification:

```text
8 passed
```

No production data files were modified during execution.

---

## Engineering Milestone

Sprint 16 marks the transition from a basic automated test suite to a structured testing architecture.

The project now includes:

- Layered Architecture
- Dependency Injection
- Repository Pattern
- Service Container
- Centralized Configuration
- Structured Logging
- Typed Domain Models
- Structured Exception Handling
- Repository Exception Translation
- Shared Pytest Fixtures
- Repository Unit Tests
- API Integration Tests
- Temporary Test Persistence
- Automated Validation Tests
- Engineering Handbook
- Semantic Git History
- Release Tags

The testing infrastructure is now capable of supporting future database migration, authentication testing, and larger integration test suites without affecting production development data.

---

## Commit

```text
test(sprint-16): isolate persistence and add repository coverage
```

---

## Release Tag

```text
v0.16.0
```

# Sprint 17

## Objectives

- Introduce a relational database foundation.
- Add SQLAlchemy to the backend.
- Establish a centralized database engine.
- Create a reusable database session factory.
- Define the initial investigation ORM model.
- Create the SQLite schema without changing the existing API.
- Prepare the project for JSON-to-SQLite migration.

---

## Features Implemented

- Installed SQLAlchemy `2.0.51`.
- Added `greenlet` as a SQLAlchemy dependency.
- Created the `app/database` package.
- Added a SQLAlchemy declarative base.
- Added the SQLite database engine.
- Added the `SessionLocal` session factory.
- Created the `Investigation` ORM model.
- Added automatic database schema initialization.
- Created the `investigations` relational table.
- Added SQLite database patterns to `.gitignore`.

---

## Database Package Structure

Sprint 17 introduced the following structure:

```text
app/
└── database/
    ├── __init__.py
    ├── database.py
    ├── models.py
    └── session.py
```

Each module has a focused responsibility.

| Module | Responsibility |
|--------|----------------|
| `database.py` | SQLAlchemy declarative base |
| `session.py` | Engine and session factory |
| `models.py` | ORM persistence models |
| `__init__.py` | Database schema initialization |

---

## Database Architecture

Before Sprint 17, the active persistence architecture was:

```text
FastAPI
    │
    ▼
Case Manager
    │
    ▼
Repository
    │
    ▼
investigations.json
```

Sprint 17 added a relational database foundation alongside the existing JSON repository:

```text
FastAPI
    │
    ▼
Case Manager
    │
    ▼
Repository
    │
    ├── JSON Persistence
    │
    └── SQLite Foundation
```

The JSON repository remains active until Sprint 18.

This allowed the database infrastructure to be introduced without changing application behavior.

---

## SQLAlchemy Declarative Base

All ORM models inherit from a shared SQLAlchemy base:

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass
```

The shared base collects database table metadata and supports schema creation.

---

## SQLite Engine

The database engine connects to:

```text
data/andiny_atlas.db
```

using the following database URL:

```text
sqlite:///./data/andiny_atlas.db
```

The engine is configured with:

```python
connect_args={
    "check_same_thread": False,
}
```

This supports SQLite usage within FastAPI's request execution environment.

---

## Session Factory

Sprint 17 introduced a reusable session factory:

```python
SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
)
```

Future repositories will create short-lived database sessions through this factory.

This separates database connection management from business logic.

---

## Investigation ORM Model

The relational investigation model contains:

- Case ID
- Timestamp
- Customer name
- Phone number
- Status
- Reason
- Next action

The investigation result fields are stored as separate relational columns:

```text
status
reason
next_action
```

rather than as a nested JSON object.

This improves queryability, indexing, filtering, and future reporting capabilities.

---

## Database Indexes

Indexes were added to fields that are already used for searching and statistics:

- `customer_name`
- `phone_number`
- `status`

These indexes prepare the database for efficient filtering and aggregation as the number of investigations grows.

---

## Schema Initialization

The database schema is initialized using:

```python
Base.metadata.create_all(bind=engine)
```

The `Investigation` model is imported before schema creation so that SQLAlchemy registers its table metadata.

The operation is idempotent:

- Missing tables are created.
- Existing tables are preserved.
- Application startup does not recreate stored data.

---

## Generated Database Handling

The SQLite database file is generated per environment and should not be committed to source control.

The root `.gitignore` now includes:

```text
*.db
*.sqlite
*.sqlite3
```

This ensures local and future test databases remain outside Git history.

---

## Challenges Encountered

- The SQLite file did not initially appear after the first Uvicorn startup check.
- Database initialization was verified directly through Python.
- The investigation table was confirmed through SQLite.
- A PowerShell quoting issue affected a schema inspection command.
- SQLite ignore patterns were initially entered as terminal commands instead of being added to `.gitignore`.
- Sprint 16 documentation changes were separated from the Sprint 17 code commit.

---

## Lessons Learned

- Database infrastructure should be introduced before persistence migration.
- ORM models and Pydantic API models serve different responsibilities.
- Generated database files should not be tracked in Git.
- Schema initialization depends on ORM model registration.
- Database engines and session factories should be centralized.
- Incremental infrastructure changes reduce migration risk.
- A relational schema can be introduced without changing the public API.

---

## Sprint Outcome

✅ Sprint completed successfully.

The SQLite database was created successfully with an empty `investigations` table.

Final database row count:

```text
(0,)
```

Final automated verification:

```text
8 passed
```

The existing JSON-backed API remained fully operational.

---

## Engineering Milestone

Sprint 17 marks the introduction of relational database infrastructure into Andiny Atlas.

The project now includes:

- Layered Architecture
- Dependency Injection
- Repository Pattern
- Service Container
- Typed Domain Models
- Centralized Configuration
- Environment Variable Support
- Structured Logging
- Structured Exception Handling
- JSON Persistence
- SQLAlchemy ORM Foundation
- SQLite Database Engine
- Database Session Factory
- Investigation Relational Model
- Automatic Schema Initialization
- Isolated Test Persistence
- Repository Unit Tests
- API Integration Tests
- Engineering Handbook
- Semantic Git History
- Release Tags

Andiny Atlas is now prepared for the migration from JSON persistence to relational SQL storage.

---

## Commit

```text
feat(sprint-17): establish SQLAlchemy database foundation
```

---

## Commit Hash

```text
916d7d9
```

---

## Release Tag

```text
v0.17.0
```

---

# Revision History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | July 2026 | Initial release covering Sprints 10–13. |
| 1.1 | July 2026 | Added Sprint 14 – Typed Investigation Status Domain Model. |
| 1.2 | July 2026 | Added Sprint 15 – Persistence Integrity and Repository Resilience. |
| 1.3 | July 2026 | Added Sprint 16 – Test Isolation and Repository Test Infrastructure. |
| 1.4 | July 2026 | Added Sprint 17 – Database Foundation and SQL Persistence Infrastructure. |

---

© 2026 Dallas Uzo

This document is part of the **Andiny Atlas Engineering Handbook** and serves as the permanent historical record of the project's engineering evolution.