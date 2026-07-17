# Engineering Handbook

# Volume III – Sprint Journal

**Version:** 1.6 (Living Document)

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
9. Sprint 18
10. Sprint 19


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

# Sprint 18

## Objectives

- Complete the migration from JSON persistence to SQLAlchemy persistence.
- Replace file-based repositories with SQLite-backed repositories.
- Introduce database mappers to isolate ORM models from domain records.
- Preserve the existing business logic while changing the persistence layer.
- Expand repository testing for SQL persistence.

---

## Features Implemented

- Replaced JSON persistence with SQLite persistence.
- Refactored `CaseRepository` to use SQLAlchemy sessions.
- Added ORM-to-domain mapping layer.
- Added domain-to-ORM mapping layer.
- Introduced SQLAlchemy transactions for persistence.
- Added SQLAlchemy exception handling.
- Expanded repository test coverage.
- Preserved all existing API behavior during the migration.

---

## Architectural Evolution

Sprint 18 completed the application's persistence migration.

Previous architecture:

```text
CaseManager
      │
      ▼
CaseRepository
      │
      ▼
investigations.json
```

New architecture:

```text
CaseManager
      │
      ▼
CaseRepository
      │
      ▼
Mapper Layer
      │
      ▼
SQLAlchemy ORM
      │
      ▼
SQLite
```

Business logic remained unchanged.

Only the persistence implementation evolved.

---

## Repository Refactoring

The repository now performs persistence through SQLAlchemy sessions.

Responsibilities include:

- Opening sessions
- Executing queries
- Managing transactions
- Translating ORM models
- Returning domain records

The repository continues to expose the same public API:

```python
load_cases()
save_cases()
```

This preserved compatibility with the service layer.

---

## Mapper Layer

Sprint 18 introduced:

```text
app/database/mappers.py
```

The mapper layer separates persistence models from application models.

It provides:

```python
record_to_investigation()

investigation_to_record()
```

Responsibilities include:

- Converting ORM models into dictionary records
- Converting dictionary records into ORM models
- Keeping SQLAlchemy isolated from the business layer

This ensures that neither the API nor the service layer depends directly on SQLAlchemy objects.

---

## SQLAlchemy Transactions

Persistence now occurs inside explicit database transactions.

```text
Session
     │
     ▼
Transaction
     │
     ▼
Insert / Replace
     │
     ▼
Commit
```

Failures automatically trigger rollback behavior through SQLAlchemy.

---

## SQL Persistence Error Handling

Repository operations now catch SQLAlchemy exceptions.

Database failures are translated into:

```text
PersistenceDataException
```

This maintains consistent error handling throughout the application.

The service layer remains unaware of database implementation details.

---

## Test Infrastructure

Existing isolated SQLite fixtures introduced during Sprint 17 were reused.

Repository tests now execute against temporary SQLite databases instead of JSON files.

Production data remains untouched during testing.

---

## Repository Test Coverage

Sprint 18 expanded repository verification to include:

- Loading empty databases
- Saving investigations
- Reading investigations
- Multiple investigation persistence
- SQL persistence replacement
- SQL persistence integrity

The repository migration was completed without changing external behavior.

---

## Backward Compatibility

Despite replacing the persistence layer completely:

- Support endpoints required no changes.
- CaseManager required only minimal repository adaptation.
- Existing API contracts remained unchanged.
- Existing clients continued to function.

This demonstrates the value of layered architecture.

---

## Challenges Encountered

- Mapping between ORM objects and domain records.
- Maintaining backward compatibility.
- Preserving service-layer interfaces.
- Managing SQLAlchemy session lifecycle.
- Replacing JSON persistence without changing API behavior.

---

## Lessons Learned

- Repository interfaces should remain stable even when implementations change.
- Mapper layers simplify large architectural migrations.
- SQLAlchemy should remain isolated inside the persistence layer.
- Business logic should never depend directly on ORM models.
- Automated tests provide confidence during infrastructure changes.

---

## Sprint Outcome

✅ Sprint completed successfully.

Repository persistence now uses SQLite exclusively.

JSON storage has been fully replaced.

All automated tests passed after the migration.

---

## Engineering Milestone

Sprint 18 completed one of the largest architectural refactorings performed on Andiny Atlas.

The application successfully transitioned from:

```text
File Persistence
```

to

```text
Relational Persistence
```

without breaking existing functionality.

This establishes a production-ready persistence foundation for future authentication, authorization, and auditing features.

---

## Commit

```text
refactor(sprint-18): migrate repository persistence to SQLAlchemy
```

---

## Release Tag

```text
v0.18.0
```

---

# Sprint 19

## Objectives

- Introduce user identity into Andiny Atlas.
- Add secure password hashing and verification.
- Add user persistence through SQLAlchemy.
- Implement user registration and login.
- Generate and validate JWT access tokens.
- Introduce authentication-specific exceptions and handlers.
- Add isolated authentication integration tests.

---

## Features Implemented

- Added the `User` SQLAlchemy ORM model.
- Added Pydantic models for:
  - User registration
  - User login
  - User response
  - JWT token response
  - JWT token payload
- Added secure password hashing with Passlib and bcrypt.
- Added password verification.
- Added JWT access-token creation.
- Added JWT decoding and validation.
- Added `UserRepository`.
- Added `AuthService`.
- Added `/auth/register`.
- Added `/auth/login`.
- Added authentication dependency providers.
- Added authentication-specific exceptions.
- Added authentication-specific global exception handlers.
- Added isolated authentication test infrastructure.
- Added authentication API tests.
- Added JWT tests.
- Added password-security tests.

---

## Authentication Architecture

Sprint 19 introduced a second complete business domain alongside the support domain.

```text
                    FastAPI
                       │
        ┌──────────────┴──────────────┐
        │                             │
   Support Domain               Authentication Domain
        │                             │
   CaseManager                  AuthService
        │                             │
 CaseRepository               UserRepository
        │                             │
        └──────────────┬──────────────┘
                       │
                  SQLAlchemy ORM
                       │
                    SQLite
```

The support and authentication domains remain independent while sharing common infrastructure.

---

## User Persistence Model

The new `users` table stores:

- User ID
- Full name
- Email
- Hashed password
- Active status
- Creation timestamp

Plaintext passwords are never stored.

The database stores only:

```text
hashed_password
```

The user email is unique and indexed to support efficient authentication lookups.

---

## API Models

Sprint 19 introduced dedicated Pydantic models for different authentication responsibilities.

| Model | Responsibility |
|---|---|
| `UserCreate` | User registration request |
| `UserLogin` | Login request |
| `UserResponse` | Safe user response |
| `Token` | JWT access-token response |
| `TokenPayload` | Decoded token claims |

The safe response model excludes:

```text
hashed_password
```

This prevents password hashes from being exposed through the API.

---

## Password Security

Passwords are processed through:

```text
app/core/security.py
```

The module provides:

```python
hash_password()
verify_password()
```

The authentication flow never compares or stores plaintext passwords directly.

```text
Plaintext Password
        │
        ▼
Password Hashing
        │
        ▼
Stored Hash
```

During login:

```text
Submitted Password
        │
        ▼
Verify Against Stored Hash
        │
        ▼
Authenticated or Rejected
```

---

## Dependency Compatibility

The initial security configuration used:

```text
passlib==1.7.4
bcrypt==5.0.0
```

This combination caused Passlib's bcrypt backend initialization to fail.

The failure was caused by a compatibility change in bcrypt 5.x.

The project was stabilized by pinning bcrypt to a compatible 4.x release.

This demonstrated the importance of:

- Dependency compatibility testing
- Exact dependency pinning
- Reading full stack traces
- Verifying library behavior through automated tests

---

## User Repository

The `UserRepository` provides:

```python
create_user()
get_user_by_email()
get_user_by_id()
```

It handles all SQLAlchemy operations related to users.

The repository normalizes email addresses before lookup and translates database failures into `PersistenceDataException`.

---

## Authentication Service

`AuthService` owns authentication business rules.

Responsibilities include:

- Checking for duplicate users
- Normalizing email addresses
- Trimming user names
- Hashing passwords
- Registering users
- Verifying credentials
- Checking active status
- Creating access tokens

Registration flow:

```text
Registration Request
        │
        ▼
Normalize Email
        │
        ▼
Check Existing User
        │
        ▼
Hash Password
        │
        ▼
Persist User
        │
        ▼
Return Safe User Response
```

Login flow:

```text
Login Request
        │
        ▼
Find User
        │
        ▼
Verify Password
        │
        ▼
Check Active Status
        │
        ▼
Create JWT
        │
        ▼
Return Access Token
```

---

## JWT Configuration

JWT settings are centralized through validated application configuration.

Current settings include:

```text
JWT_SECRET_KEY
JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
JWT_ISSUER
```

The `.env` file remains excluded from Git so secrets are not committed.

---

## JWT Claims

The access token includes:

```text
sub  → User ID
iat  → Issued-at time
exp  → Expiration time
iss  → Andiny Atlas issuer
```

Tokens are signed using the configured secret and algorithm.

JWT decoding validates:

- Signature
- Expiration
- Issuer
- Token structure

Invalid or expired tokens are rejected.

---

## Authentication Endpoints

### Register User

```http
POST /auth/register
```

Successful response:

```text
HTTP 201 Created
```

The response contains safe user information only.

### Login

```http
POST /auth/login
```

Successful response:

```json
{
  "access_token": "<signed-jwt>",
  "token_type": "bearer"
}
```

---

## Authentication Error Handling

Sprint 19 introduced a clear authentication error vocabulary.

| Exception | Code | HTTP Status |
|---|---|---:|
| `InvalidCredentialsException` | `INVALID_CREDENTIALS` | 401 |
| `InactiveUserException` | `INACTIVE_USER` | 403 |
| `UserNotFoundException` | `USER_NOT_FOUND` | 404 |
| `UserAlreadyExistsException` | `USER_ALREADY_EXISTS` | 409 |

Invalid credentials return:

```text
WWW-Authenticate: Bearer
```

This aligns the API response with bearer-token authentication conventions.

---

## Test Infrastructure

The shared test setup now supports both domains.

```text
Temporary SQLite Database
        │
        ├── CaseRepository
        │       └── Support API Client
        │
        └── UserRepository
                └── Authentication API Client
```

Authentication tests use isolated SQLite persistence and FastAPI dependency overrides.

The real application database remains untouched.

---

## Authentication Test Coverage

Sprint 19 added tests for:

- Password hashing
- Correct-password verification
- Wrong-password rejection
- JWT creation
- JWT decoding
- Invalid-token rejection
- Successful user registration
- Duplicate-email rejection
- Successful login
- Wrong-password login rejection
- Unknown-email login rejection

---

## Challenges Encountered

- `EmailStr` required the separate `email-validator` dependency.
- Passlib 1.7.4 was incompatible with bcrypt 5.0.0.
- The compatible bcrypt release had to be pinned.
- JWT secrets had to remain outside Git.
- Existing test infrastructure had to be extended for authentication without coupling it to the support domain.
- Authentication exceptions required distinct HTTP status codes and response behavior.

---

## Lessons Learned

- Authentication should be implemented as an independent business domain.
- Passwords must never be stored or logged in plaintext.
- API models and database models serve different responsibilities.
- JWT secrets belong in environment configuration.
- Dependency versions can affect security behavior.
- Authentication failures should use explicit domain exceptions.
- Integration tests should exercise the entire authentication stack.
- Secure design depends on both architecture and dependency discipline.

---

## Sprint Outcome

✅ Sprint completed successfully.

The test suite increased from:

```text
11 tests
```

to:

```text
21 tests
```

Final verification:

```text
21 passed
```

Andiny Atlas now supports:

- User registration
- Secure password storage
- User authentication
- JWT access-token issuance
- JWT validation
- Standardized authentication errors

---

## Engineering Milestone

Sprint 19 marks the introduction of identity and authentication into Andiny Atlas.

The backend now includes:

- Layered Architecture
- Dependency Injection
- Repository Pattern
- Service Layer
- Mapper Layer
- SQLAlchemy ORM
- SQLite Persistence
- Typed Domain Models
- User Persistence
- Password Hashing
- JWT Authentication
- Registration Endpoint
- Login Endpoint
- Authentication Exceptions
- Structured Error Responses
- Isolated Authentication Testing
- Repository Unit Tests
- API Integration Tests
- Engineering Handbook
- Semantic Git History
- Release Tags

Andiny Atlas is no longer an anonymous API.

It now understands registered users and can issue signed credentials.

---

## Commit

```text
feat(sprint-19): implement JWT authentication and user management
```

---

## Commit Hash

```text
4279b7d
```

---

## Release Tag

```text
v0.19.0
```

# Sprint 22 – Enterprise Query Engine

---

## Executive Summary

Sprint 22 introduced the Enterprise Query Engine for Andiny Atlas.

The sprint transformed investigation retrieval from a basic list-and-search capability into a structured, validated, ownership-aware and paginated query system suitable for enterprise applications and future frontend integration.

Before Sprint 22, the platform could:

- Create investigation cases.
- Retrieve all investigation cases.
- Retrieve one investigation case by its identifier.
- Search cases using customer name or phone number.
- Calculate investigation statistics.

These capabilities were appropriate for the platform’s earlier development phase. However, returning an unrestricted list of records would not scale effectively when the number of investigations grows into thousands or millions.

Sprint 22 therefore introduced:

- Validated query models.
- Generic pagination models.
- SQL-level filtering.
- SQL-level sorting.
- SQL-level pagination.
- Matching-record counting.
- Ownership-aware investigation retrieval.
- Pagination metadata.
- The authenticated /support/my-cases endpoint.
- An updated public response contract exposing investigation ownership.
- Expanded repository and API test coverage.

The completed implementation preserves Andiny Atlas’s layered architecture:

```text
API Layer
    │
    ▼
Validated Query Models
    │
    ▼
Service Layer
    │
    ▼
Repository Layer
    │
    ▼
SQLAlchemy
    │
    ▼
SQLite
```
---

## Sprint Objective

Transform investigation retrieval into an enterprise-grade query capability by introducing reusable filtering, sorting, pagination and ownership-aware retrieval while preserving the existing layered architecture and automated test stability.

---

## Engineering Motivation

Up to Sprint 21, investigation retrieval was intentionally simple.

The application could return all cases or apply basic searches using customer name and phone number.

This design was sufficient while the dataset remained small. However, it introduced several limitations:

- Collection responses were unbounded.
- Large datasets could be loaded unnecessarily.
- Pagination was unavailable.
- Sorting choices were unavailable.
- Ownership-aware retrieval required separate application logic.
- Future filters would continuously expand repository method signatures.
- Frontend applications would not receive pagination metadata.
- Administrative dashboards would have limited querying capability.

- An enterprise platform must return only the records required by the client.

Filtering, sorting and pagination should occur inside the database rather than after loading complete collections into application memory.

Sprint 22 addressed this requirement by introducing a reusable query architecture.

---

## Architectural Decision

The central architectural decision was to represent investigation retrieval requirements using a validated query object.

The previous repository search interface accepted individual optional values:

```text
search_cases(
    customer_name=None,
    phone_number=None,
)
```

Continuing this design would eventually create increasingly large method signatures:

```text
search_cases(
    customer_name=None,
    phone_number=None,
    created_by=None,
    status=None,
    start_date=None,
    end_date=None,
    region=None,
    priority=None,
)
```

Sprint 22 introduced:

```text
query_cases(query: CaseQuery)
```

This design allows future filtering options to be added by extending CaseQuery without repeatedly redesigning repository and service method signatures.

The approach provides:

- Stable repository interfaces.
- Centralized validation.
- Improved OpenAPI documentation.
- Easier frontend integration.
- Reduced duplication.
- Greater extensibility.
---

## Architecture Before Sprint 22

Before Sprint 22, collection retrieval followed this path:

```text
HTTP Request
    │
    ▼
FastAPI Endpoint
    │
    ▼
CaseManager
    │
    ▼
CaseRepository
    │
    ▼
SQLite
```

The repository supported:

- get_all_cases()
- get_case_by_id()
- search_cases()
- get_statistics()

- The architecture was layered correctly, but collection retrieval remained basic.

---

## Architecture After Sprint 22

Sprint 22 expanded the request lifecycle:

```text
HTTP Request
    │
    ▼
FastAPI Endpoint
    │
    ▼
CaseQuery Validation
    │
    ▼
CaseManager
    │
    ├── Repository orchestration
    ├── Pagination calculation
    └── Response construction
    │
    ▼
CaseRepository
    │
    ├── SQL filters
    ├── SQL sorting
    ├── SQL count query
    ├── OFFSET
    └── LIMIT
    │
    ▼
SQLAlchemy / SQLite
    │
    ▼
PaginatedResponse
```

Each layer retains a specific responsibility.

| Layer | Responsibility |
|---|---|
| API | Receives requests, validates query input and returns responses |
| Models | Define accepted query values and pagination contracts |
| Service | Coordinates repository execution and calculates pagination metadata |
| Repository | Builds and executes SQL queries |
| Database | Performs filtering, sorting, counting and pagination |
| Tests | Verify repository, service integration, API behaviour and security boundaries |
---

## Files Added

`backend/app/models/query.py`
`backend/app/models/pagination.py`
---

## Files Modified

`backend/app/api/support.py`
`backend/app/models/case_response.py`
`backend/app/repositories/case_repository.py`
`backend/app/services/case_manager.py`
`backend/tests/test_case_repository.py`
`backend/tests/test_support.py`
---

## Query Models

Sprint 22 introduced:

`app/models/query.py`

This module contains:

### SortOrder

### CaseSortField

### CaseQuery

### SortOrder

SortOrder defines the accepted sorting directions:

```text
asc
desc
```

Example:

```text
GET /support/cases?sort_order=desc
```

Unsupported values are rejected before repository execution.

### CaseSortField

CaseSortField defines the investigation fields clients may use for sorting:

```text
timestamp
customer_name
phone_number
status
created_by
```

This prevents clients from passing arbitrary database field names.

It also ensures that Swagger/OpenAPI exposes the accepted values explicitly.

### CaseQuery

CaseQuery is the validated contract for investigation collection requests.

Supported fields:

```text
page
page_size
customer_name
phone_number
created_by
status
sort_by
sort_order
```

Default values:

```text
page = 1
page_size = 20
sort_by = timestamp
sort_order = desc
```

Validation rules:

```text
page must be at least 1
page_size must be between 1 and 100
sort_by must be a supported CaseSortField
sort_order must be asc or desc
status must be a supported InvestigationStatus
```

- The default sorting behaviour returns newer investigation records before older records.

---

## Pagination Models

Sprint 22 introduced:

`app/models/pagination.py`

This module contains:

### PaginationMetadata

### PaginatedResponse[T]

### PaginationMetadata

PaginationMetadata contains:

```text
page
page_size
total_records
total_pages
returned_records
```
| Field | Meaning |
|---|---|
| page | Current page requested |
| page_size | Maximum records requested per page |
| total_records | Number of records matching the filters |
| total_pages | Pages required to return all matching records |
| returned_records | Records included in the current response |

Example:

```text
total_records = 45
page_size = 20
total_pages = 3
```

The final page would contain:

```text
returned_records = 5
```

When no records match:

```text
total_records = 0
total_pages = 0
returned_records = 0
```
### PaginatedResponse[T]

PaginatedResponse[T] is generic.

For investigation cases, the API uses:

```text
PaginatedResponse[CaseResponse]
```

Example response:

```text
{
  "metadata": {
    "page": 1,
    "page_size": 20,
    "total_records": 1,
    "total_pages": 1,
    "returned_records": 1
  },
  "items": [
    {
      "case_id": "case-001",
      "timestamp": "2026-07-11T10:00:00+00:00",
      "customer_name": "John Doe",
      "phone_number": "08021234567",
      "created_by": "user-001",
      "result": {
        "status": "Resolved",
        "reason": "Device should unlock successfully.",
        "next_action": "No further action required."
      }
    }
  ]
}
```

The generic design allows reuse for future resources such as:

- Users
- Audit logs
- Reports
- Notifications
- Administrative records
- AI recommendations
---

## Repository Evolution

The Enterprise Query Engine was added to:

`app/repositories/case_repository.py`

The new method is:

```text
query_cases(query: CaseQuery)
```

It returns:

```text
tuple[CaseCollection, int]
```

The tuple contains:

Investigation records for the requested page.
Total number of records matching the filters.

The repository intentionally does not create API pagination metadata.

That responsibility belongs to the service layer.

---

## SQL-Level Filtering

The repository supports filtering by:

```text
customer_name
phone_number
created_by
status
```

- Customer-name comparison is case-insensitive.

The repository normalizes the supplied customer name using:

```text
strip
lower
```

Phone number, ownership and status filters use exact matching.

When multiple filters are provided, they are combined.

Example:

```text
GET /support/cases?customer_name=Jane%20Doe&phone_number=08029876543&created_by=user-002&status=Escalated
```

Only cases matching every supplied condition are returned.

---

## SQL-Level Sorting

Validated sorting fields are mapped to SQLAlchemy model columns.

The requested sort order is applied as either:

```text
ASC
DESC
```

A secondary ascending sort using case_id is also applied.

This creates deterministic ordering when several records share the same primary sort value.

For example, two cases may have identical timestamps. The secondary case_id ordering prevents records from changing positions between repeated requests.

---

## SQL Pagination

The repository calculates offset using:

```text
offset = (page - 1) × page_size
```

Example:

page = 3
page_size = 20

offset = (3 - 1) × 20
offset = 40

SQLAlchemy then applies:

```text
OFFSET 40
LIMIT 20
```

The database returns only the requested page.

This is more efficient than retrieving every matching investigation and slicing the collection inside Python.

---

## Matching-Record Count

Pagination requires two related queries:

```text
Data Query
Count Query
```

The data query returns records for the requested page.

The count query returns the total number of records matching the same filters.

Pagination is not applied to the count query.

This ensures:

total_records

represents the complete filtered result set rather than only the records returned on the current page.

---

## Service-Layer Integration

The service implementation is located in:

`app/services/case_manager.py`

Sprint 22 introduced:

```text
query_cases(query: CaseQuery)
```

The service performs the following workflow:

```text
Receive CaseQuery
    │
    ▼
Call repository.query_cases()
    │
    ▼
Receive page records and total count
    │
    ▼
Calculate total_pages
    │
    ▼
Build PaginationMetadata
    │
    ▼
Return PaginatedResponse
```

Total pages are calculated using:

ceil(total_records / page_size)

When there are no matching records:

total_pages = 0

The service layer owns this calculation because pagination metadata is application-response orchestration rather than database-access logic.

---

## API Evolution

Sprint 22 updated:

`app/api/support.py`

The support router remains protected by JWT bearer authentication.

The following collection endpoints are now available:

```text
GET /support/cases
GET /support/my-cases
```
### Endpoint: Query Investigation Cases

### Method and Route

```text
GET /support/cases
```
### Authentication

Required.

The request must include:

```text
Authorization: Bearer <access-token>
```
### Purpose

Returns filtered, sorted and paginated investigation cases.

### Supported Query Parameters

| Parameter | Type | Default | Constraint |
|---|---|---:|---|
| page | Integer | 1 | Minimum 1 |
| page_size | Integer | 20 | Between 1 and 100 |
| customer_name | String | None | Optional |
| phone_number | String | None | Optional |
| created_by | String | None | Optional |
| status | Enum | None | Supported investigation status |
| sort_by | Enum | timestamp | Supported case sort field |
| sort_order | Enum | desc | asc or desc |
### Example Request

```text
GET /support/cases?page=2&page_size=20&status=Resolved&sort_by=timestamp&sort_order=desc
Authorization: Bearer <access-token>
```
### Implementation Path

`app/api/support.py`
```text
    │
    ▼
app/models/query.py
    │
    ▼
app/services/case_manager.py
    │
    ▼
app/repositories/case_repository.py
    │
    ▼
app/database/models.py
```
### Endpoint: Query My Investigation Cases

### Method and Route

```text
GET /support/my-cases
```
### Authentication

Required.

### Purpose

Returns only investigation cases created by the authenticated user.

### Ownership Enforcement

The API accepts a standard CaseQuery, but replaces any supplied created_by value with:

```text
current_user.id
```

Flow:

```text
Client Request
    │
    ▼
JWT Validation
    │
    ▼
Current User Resolution
    │
    ▼
Override created_by
    │
    ▼
Execute Query
    │
    ▼
Return Authenticated User's Cases
```

A client cannot retrieve another user’s cases by supplying:

?created_by=another-user-id

The supplied value is replaced server-side.

### Security Outcome

Ownership filtering is enforced by the backend.

It is not dependent on frontend behaviour or trusted client input.

---

## Public Response Contract Update

Sprint 22 updated:

`app/models/case_response.py`

CaseResponse now includes:

```text
created_by: str
```

The field was already present in:

- The database model.
- ORM mappings.
- Repository records.
- Service-layer records.
- Investigation creation logic.

- However, it was not included in the public response model.

- API tests exposed the mismatch.

The response contract was corrected so that investigation ownership is visible to frontend, reporting and administrative interfaces.

---

## Validation Behaviour

Invalid query input is rejected before repository execution.

Examples:

### Invalid Page

```text
GET /support/cases?page=0
```

Response:

```text
HTTP 422
```
### Invalid Page Size

```text
GET /support/cases?page_size=101
```

Response:

```text
HTTP 422
```
### Invalid Sort Field

```text
GET /support/cases?sort_by=unsupported_field
```

Response:

```text
HTTP 422
```

This validation protects repository code from unsupported input and produces standardized API feedback.

---

## Testing Strategy

Sprint 22 used a bottom-up testing sequence:

```text
Repository Tests
    │
    ▼
Service Integration
    │
    ▼
API Tests
    │
    ▼
Full Regression Suite
```

Repository behaviour was proven before API exposure.

This made failures easier to isolate and reduced debugging complexity.

---

## Repository Test Coverage

Repository tests now verify:

- Empty collection behaviour.
- Case creation.
- Retrieval by case ID.
- Missing-case behaviour.
- Legacy search behaviour.
- Pagination.
- Matching-record totals.
- Customer-name sorting.
- Timestamp sorting.
- Status filtering.
- Ownership filtering.
- Combined filtering.
- Pages beyond the available result set.
- Investigation statistics.

Repository tests increased from:

6

to:

14
---

## API Test Coverage

API tests verify:

- Investigation creation.
- Paginated response structure.
- Pagination metadata.
- Status filtering.
- Customer-name sorting.
- Current-user case retrieval.
- Ownership isolation.
- Protection against manipulated created_by filters.
- Invalid page rejection.
- Invalid page-size rejection.
- Invalid sort-field rejection.
- Unknown-case responses.
- Statistics responses.
- Authentication enforcement.
- Invalid investigation-status rejection.
- Controlled persistence failures.
---

## Test Results

The complete automated suite increased from:

25 tests

to:

42 tests

Final result:

```text
42 passed
```

Regression failures:

0

The suite covers:

- Authentication.
- JWT handling.
- Password security.
- Repository persistence.
- Enterprise querying.
- Filtering.
- Sorting.
- Pagination.
- Ownership isolation.
- API validation.
- Support workflows.
- Exception handling.
---

## Database Verification

Sprint 22 did not require a schema change.

No new Alembic migration was generated.

Schema consistency was verified using:

alembic check

Result:

```text
No new upgrade operations detected.
```

This confirms that the SQLAlchemy metadata and migration-controlled database schema remained aligned.

---

## Architectural Improvements

Sprint 22 introduced the following improvements:

- Collection responses are bounded by default.
- Query options are centrally validated.
- Filtering occurs inside the database.
- Sorting occurs inside the database.
- Pagination occurs inside the database.
- Count queries use the same filters as data queries.
- Repository interfaces remain extensible.
- Pagination responses use a reusable generic model.
- The service layer owns metadata construction.
- Current-user ownership is enforced server-side.
- API responses expose ownership.
- Invalid input is rejected before persistence execution.
- The API contract is ready for frontend pagination controls and enterprise dashboards.
---

## Challenges Encountered

The sprint presented several implementation challenges:

- Correctly positioning the new repository method within the class.
- Preserving the legacy search method during migration.
- Ensuring deterministic sorting.
- Separating total matching records from current-page records.
- Enforcing ownership without trusting query-string identifiers.
- Updating the public response contract.
- Maintaining existing endpoint behaviour.
- Resolving an initial Git staging mistake before tagging the release.

A notable test failure occurred because created_by was stored internally but omitted from CaseResponse.

This demonstrated that internal ownership capability does not automatically become part of the public API contract.

The response model was updated, and all tests passed.

---

## Lessons Learned

Database-level pagination is more scalable than in-memory slicing.
Count queries must use the same filters as data queries.
Query objects scale better than large optional method signatures.
Generic pagination reduces duplication.
Deterministic secondary sorting stabilizes paginated results.
Ownership must be enforced server-side.
Response models must reflect intended public capabilities.
Bottom-up testing improves failure isolation.
Invalid values should be rejected before repository execution.
Git tags must be created only after the intended commit exists.
A strong regression suite makes API contract changes safer.
---

## Why Sprint 22 Matters

Sprint 22 changed the platform from basic investigation retrieval to enterprise-oriented data access.

Andiny Atlas can now answer requests such as:

Return page two of escalated investigations,
created by a specific user,
sorted from newest to oldest,
with twenty records per page,
and include the total matching count.

This capability is required for:

- Agent work queues.
- Supervisor dashboards.
- Administrative interfaces.
- Historical investigation review.
- Operational reporting.
- Frontend pagination controls.
- Large enterprise datasets.

- Sprint 22 also established reusable query conventions for future platform modules.

---

## Architect's Notes

The most important Sprint 22 achievement is not the presence of page and page_size.

It is the creation of an extensible retrieval architecture.

The final responsibility chain is:

```text
FastAPI validates.
CaseManager orchestrates.
CaseRepository queries.
SQLAlchemy translates.
SQLite executes.
Pydantic shapes the response.
Pytest proves the behaviour.
```

This pattern can later support:

- User administration.
- Audit-event retrieval.
- Reporting.
- Notification history.
- AI recommendation history.
- Multi-tenant operational dashboards.

Sprint 22 therefore delivered both immediate functionality and a reusable architectural pattern.

---

## Sprint Outcome

✅ Sprint completed successfully.

Final test result:

```text
42 passed
```

Database verification:

```text
No new upgrade operations detected.
```
---

## Engineering Milestone

At the completion of Sprint 22, Andiny Atlas includes:

- FastAPI application architecture.
- Dependency Injection.
- Service Layer.
- Repository Pattern.
- SQLAlchemy ORM.
- SQLite persistence.
- Alembic schema migrations.
- User registration.
- JWT authentication.
- Protected APIs.
- Current-user resolution.
- Investigation ownership.
- Enterprise investigation querying.
- SQL-level filtering.
- SQL-level sorting.
- SQL pagination.
- Generic paginated responses.
- Ownership-aware /support/my-cases.
- Structured exception handling.
- Structured logging.
- Forty-two passing automated tests.
- Semantic Git history.
- Versioned releases.
- Engineering Handbook and Sprint Journal.
---

## Commit

```text
feat(sprint-22): add enterprise case querying and pagination
```
---

## Commit Hash

```text
a46a391
```
---

## Release Tag

```text
v0.22.0
```

---

# Sprint 23 – Controlled Investigation Updates

**Duration:** Sprint 23

**Version:** v0.23.0

**Status:** ✅ Completed

---

# Sprint Overview

Sprint 23 introduced controlled investigation updates into the Andiny Atlas backend.

Prior to this sprint, investigations could only be created and retrieved. Once a case was created, there was no supported mechanism for modifying its details.

This sprint closes that gap by introducing a secure update workflow that allows investigators to modify permitted fields while preserving ownership rules and protecting immutable data.

The implementation follows the same layered architecture adopted throughout the project:

- API Layer
- Service Layer
- Repository Layer
- Database

This ensures consistency, maintainability, and separation of concerns.

---

# Sprint Objectives

The primary objectives of Sprint 23 were:

- Introduce controlled updates for investigation cases.
- Restrict updates to authorised owners.
- Protect immutable investigation fields.
- Maintain architectural consistency.
- Increase automated test coverage.
- Preserve database integrity.

---

# Features Implemented

## 1. Investigation Update Model

A dedicated request model was introduced specifically for investigation updates.

**New File**

```text
app/models/update_case.py
```

This model validates only the fields that are allowed to change after an investigation has been created.

Separating update validation from creation validation improves maintainability and reduces the risk of accidental modification of protected fields.

---

## 2. Repository Update Support

The repository layer was extended to support updates to existing investigations.

Responsibilities include:

- locating an investigation
- applying permitted changes
- committing changes to the database
- refreshing the entity
- returning the updated investigation

The repository remains responsible solely for data persistence.

---

## 3. Service Layer Enhancements

The service layer now orchestrates investigation updates.

Responsibilities include:

- validating ownership
- enforcing business rules
- coordinating repository operations
- returning the updated investigation

Business logic continues to remain outside the API layer.

---

## 4. PATCH Investigation Endpoint

A new REST endpoint was introduced.

```http
PATCH /support/cases/{case_id}
```

The endpoint enables authenticated users to update investigations that they own.

Supported update fields include operational investigation data while immutable properties remain protected.

---

## 5. Ownership Enforcement

Sprint 20 introduced investigation ownership.

Sprint 23 extends that functionality by ensuring that:

- only investigation owners may perform updates
- update attempts by other users are rejected
- proper HTTP error responses are returned

Ownership validation continues to reside inside the service layer.

---

## 6. Immutable Field Protection

To preserve investigation integrity, certain fields remain immutable after creation.

Examples include:

- Investigation ID
- Owner information
- Creation metadata

Only approved operational fields may be updated.

This protects data consistency throughout the investigation lifecycle.

---

# Files Added

```text
app/models/update_case.py
```

---

# Files Modified

```text
app/api/support.py

app/repositories/case_repository.py

app/services/case_manager.py

tests/test_case_repository.py

tests/test_support.py
```

---

# Testing

Sprint 23 significantly expanded automated testing.

New test coverage includes:

- Successful investigation updates
- Repository update operations
- PATCH endpoint validation
- Ownership enforcement
- Missing investigation handling
- Immutable field protection
- Persistence verification

---

# Quality Assurance

## Automated Tests

```text
52 passed
```

All automated tests completed successfully without regression.

---

## Alembic Verification

```text
No new upgrade operations detected.
```

Database models remain fully synchronised with Alembic migrations.

---

## Version Control

### Commit

```text
feat(sprint-23): add controlled investigation updates
```

### Version Tag

```text
v0.23.0
```

Both commit and version tag were successfully pushed to GitHub.

---

# Architecture Impact

Sprint 23 completes the first phase of the investigation lifecycle.

Current investigation capabilities now include:

- Create Investigation
- Retrieve Investigation
- Query Investigations
- Filter Investigations
- Pagination
- User Ownership
- Controlled Updates

This establishes a strong foundation for introducing investigation history, audit trails, comments, assignments, and workflow management in subsequent sprints.

---

# Lessons Learned

Several engineering lessons were reinforced during Sprint 23.

### Separate Request Models

Using dedicated request models for updates prevents accidental exposure of protected fields and keeps validation rules concise.

### Business Rules Belong in the Service Layer

Ownership validation remains centralised inside the service layer, preventing duplication across API endpoints.

### Repository Responsibility

Repositories continue to focus exclusively on persistence, resulting in cleaner architecture and easier testing.

### Test-Driven Confidence

Expanding automated tests alongside feature implementation continues to minimise regressions and improves long-term maintainability.

---

# Sprint Outcome

Sprint 23 successfully introduced secure investigation updates while preserving ownership controls, protecting immutable fields, and maintaining full architectural consistency.

The backend now supports the complete lifecycle of creating, retrieving, querying, and updating investigations.

All quality gates were successfully completed:

- ✅ Code Implementation
- ✅ Automated Tests (52 Passed)
- ✅ Alembic Verification
- ✅ Git Commit
- ✅ GitHub Push
- ✅ Version Tag (v0.23.0)

Sprint 23 is officially complete and serves as the foundation for future audit history and investigation workflow enhancements.

---

# Backend Progress

| Sprint | Capability | Status |
|---------|------------|--------|
| Sprint 19 | Authentication & User Management | ✅ |
| Sprint 20 | Ownership & Protected APIs | ✅ |
| Sprint 21 | Database Persistence & Alembic | ✅ |
| Sprint 22 | Enterprise Query Engine | ✅ |
| Sprint 23 | Controlled Investigation Updates | ✅ |

**Current Backend Progress:** **5 Major Sprints Completed**
---

# Revision History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | July 2026 | Initial release covering Sprints 10–13. |
| 1.1 | July 2026 | Added Sprint 14 – Typed Investigation Status Domain Model. |
| 1.2 | July 2026 | Added Sprint 15 – Persistence Integrity and Repository Resilience. |
| 1.3 | July 2026 | Added Sprint 16 – Test Isolation and Repository Test Infrastructure. |
| 1.4 | July 2026 | Added Sprint 17 – Database Foundation and SQL Persistence Infrastructure. |
| 1.5 | July 2026 | Added Sprint 18 – SQLAlchemy Repository Migration. |
| 1.6 | July 2026 | Added Sprint 19 – JWT Authentication and User Management Foundation. |

---

© 2026 Dallas Uzo

This document is part of the **Andiny Atlas Engineering Handbook** and serves as the permanent historical record of the project's engineering evolution.