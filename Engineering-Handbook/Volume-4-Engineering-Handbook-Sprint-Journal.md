# Engineering Handbook

# Volume III – Sprint Journal

**Version:** 1.1 (Living Document)

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

---

# Revision History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | July 2026 | Initial release covering Sprints 10–13. |
| 1.1 | July 2026 | Added Sprint 14 – Typed Investigation Status Domain Model. |

---

© 2026 Dallas Uzo

This document is part of the **Andiny Atlas Engineering Handbook** and serves as the permanent historical record of the project's engineering evolution.