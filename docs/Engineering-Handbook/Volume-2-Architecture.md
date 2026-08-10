# Engineering Handbook

# Volume II – System Architecture

**Version:** 1.0  
**Project:** Andiny Atlas  
**Author:** Dallas Uzo

---

# Purpose

This volume explains the architecture of **Andiny Atlas**, the responsibility of each application layer, and how requests travel through the system from the API to persistent storage.

Its purpose is to establish a common architectural language that guides future development and ensures consistency as the application evolves.

---

# Table of Contents

1. Chapter 1 – High-Level Architecture
2. Chapter 2 – Project Structure
3. Chapter 3 – Layer Responsibilities
4. Chapter 4 – Dependency Injection
5. Chapter 5 – Request Lifecycle
6. Chapter 6 – Error Lifecycle
7. Chapter 7 – Testing Strategy
8. Chapter 8 – Architecture Summary
9. Chapter 9 – Revision History

---

# Chapter 1 – High-Level Architecture

Every request follows a consistent path through the application.

```text
          Client / Swagger UI
                  │
                  ▼
            FastAPI Router
                  │
                  ▼
       Dependency Injection
                  │
                  ▼
          Workflow Engine
                  │
                  ▼
            Case Manager
                  │
                  ▼
          Repository Layer
                  │
                  ▼
       investigations.json
                  │
                  ▼
            JSON Response
```

Each layer has a single responsibility and communicates only with the layer immediately above or below it.

This separation keeps the application maintainable, testable, and easy to extend.

---

# Chapter 2 – Project Structure

```text
backend/

├── app/
│   ├── api/
│   ├── core/
│   ├── exceptions/
│   ├── logging/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── dependencies.py
│   └── main.py
│
├── data/
│
├── tests/
│
└── requirements.txt
```

The project is organized using a layered architecture that clearly separates:

- HTTP communication
- Business logic
- Data persistence
- Application infrastructure

Each directory has a single responsibility, making the project easier to navigate and maintain.

---

# Chapter 3 – Layer Responsibilities

## API Layer (`app/api`)

### Responsibility

Receive HTTP requests and return HTTP responses.

### What belongs here

- Route definitions
- Request models
- Response models
- Dependency Injection
- HTTP status codes
- Swagger documentation

### What should **not** belong here

- Business rules
- File operations
- Database access
- Complex calculations

The API layer should remain as thin as possible.

---

## Service Layer (`app/services`)

### Responsibility

Implement business logic.

Examples include:

- Investigating support cases
- Calculating statistics
- Searching investigations
- Building investigation records

This is where the application's behavior lives.

---

## Repository Layer (`app/repositories`)

### Responsibility

Manage data persistence.

Current implementation:

- Load investigations from `investigations.json`
- Save investigations to `investigations.json`

The remainder of the application should never know where data is stored.

Today the repository uses JSON.

Tomorrow it could use:

- SQLite
- PostgreSQL
- MongoDB
- DynamoDB

Only the repository should change.

---

## Models Layer (`app/models`)

### Responsibility

Validate and serialize application data.

Current models include:

- SupportCase
- InvestigationResult
- CaseResponse
- Statistics
- ErrorResponse

Pydantic ensures incoming data is valid before business logic executes.

---

## Exceptions Layer (`app/exceptions`)

### Responsibility

Provide centralized error handling.

Current exception:

- `CaseNotFoundException`

Current handler:

- `case_not_found_handler`

Centralized exception handling ensures consistent API responses.

---

## Core Layer (`app/core`)

### Responsibility

Provide application-wide infrastructure.

Examples include:

- Configuration
- Settings
- Environment management
- Logging configuration

Business logic should never be mixed with infrastructure code.

---

# Chapter 4 – Dependency Injection

Dependencies are created inside:

```text
app/dependencies.py
```

Instead of constructing services inside routes:

### Avoid

```python
engine = WorkflowEngine()
```

### Preferred

```python
engine: WorkflowEngine = Depends(get_workflow_engine)
```

## Benefits

- Cleaner routes
- Easier testing
- Better separation of concerns
- Centralized object creation
- Easier future refactoring

Dependency Injection keeps application components loosely coupled and easier to maintain.

---

# Chapter 5 – Request Lifecycle

Example endpoint:

```text
POST /support/investigate
```

The request travels through the application as follows:

1. Client sends a JSON payload.
2. FastAPI validates it using `SupportCase`.
3. The router receives the validated request.
4. Dependencies provide `WorkflowEngine` and `CaseManager`.
5. `WorkflowEngine` performs the investigation.
6. `CaseManager` saves the investigation.
7. Repository writes to `investigations.json`.
8. FastAPI serializes the response using `CaseResponse`.
9. JSON is returned to the client.

---

# Chapter 6 – Error Lifecycle

Example endpoint:

```text
GET /support/cases/unknown-id
```

When a requested investigation cannot be found:

1. Router calls `get_case_by_id()`.
2. `CaseManager` searches the repository.
3. No matching case exists.
4. `CaseNotFoundException` is raised.
5. Global exception handler catches the exception.
6. A standardized `ErrorResponse` is generated.
7. Client receives an **HTTP 404 Not Found** response.

This ensures every error follows the same response format across the application.

---

# Chapter 7 – Testing Strategy

Current automated tests verify:

- Successful investigation
- Unknown case handling (404)
- Statistics endpoint

Tests are executed using:

```bash
python -m pytest
```

Automated testing ensures architectural changes do not introduce regressions and provides confidence that existing functionality continues to work as expected.

---

# Chapter 8 – Architecture Summary

The architecture follows a clear separation of responsibilities.

| Layer | Responsibility |
|--------|----------------|
| API | HTTP communication |
| Models | Validation and serialization |
| Services | Business logic |
| Repository | Data persistence |
| Exceptions | Error handling |
| Tests | Behavioral verification |

Each layer focuses on a single responsibility, making the application easier to understand, maintain, extend, and test.

This architecture establishes a solid foundation for future enhancements, including database migration, authentication, deployment, monitoring, and cloud-native scalability.

---

# Chapter 9 – Revision History

| Version | Date | Description |
|---------|------|-------------|
| **1.0** | July 2026 | Initial release of **Volume II – System Architecture** |

---

## Closing Note

A well-designed architecture allows engineers to evolve a system without constantly rewriting it.

By separating concerns into clearly defined layers, Andiny Atlas remains maintainable, testable, and adaptable as new features are introduced.

The architecture documented in this volume represents the foundation upon which all future engineering work will be built.

---

© 2026 Dallas Uzo — *Part of the Andiny Atlas Engineering Handbook.*