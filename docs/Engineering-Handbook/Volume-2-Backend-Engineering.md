Engineering Handbook
Volume II – Backend Engineering

Version: 1.0 (Living Document)

Project: Andiny Atlas

Author: Dallas Uzo

Table of Contents

Chapter 9 – Backend Engineering Principles

Chapter 10 – API Design Standards

Chapter 11 – Service Layer Principles

Chapter 12 – Repository Pattern

Chapter 13 – Exception Handling Strategy

Chapter 14 – Data Models

Chapter 15 – Engineering Decisions

Notice something important.

We're not writing all of those today.

We're creating the framework.

Today we'll complete Chapter 9 only.

As future sprints introduce more concepts, Chapters 10–15 will naturally fill themselves.

That's exactly how real engineering documentation evolves.

Chapter 9 – Backend Engineering Principles

I would write this exactly as follows.

Chapter 9 – Backend Engineering Principles

Throughout the development of Andiny Atlas, the backend has gradually evolved from a single application file into a layered architecture with clearly separated responsibilities.

Rather than introducing complex design patterns from the beginning, each architectural improvement was adopted only when the project naturally required it.

This approach keeps the codebase understandable while allowing it to scale over time.

9.1 Single Responsibility Principle

Every component should have one primary responsibility.

Examples within Andiny Atlas include:

API routes receive HTTP requests and return HTTP responses.
Services implement business logic.
Repositories manage persistence.
Models describe data structures.
Dependencies construct shared services.
Exception handlers translate exceptions into HTTP responses.

Keeping responsibilities isolated reduces coupling and makes changes easier to implement.

9.2 Business Logic Lives in Services

API routes should remain thin.

Routes should coordinate requests rather than contain business logic.

Instead of implementing investigation rules inside the API layer, the request is delegated to the Workflow Engine.

Client

↓

API Route

↓

Workflow Engine

↓

Case Manager

↓

Repository

↓

JSON Storage

This separation allows the investigation logic to evolve independently of the API.

9.3 Dependency Injection

Objects should not construct their own dependencies.

Instead, dependencies are provided externally.

For example:

WorkflowEngine
CaseManager
CaseRepository

are all injected using FastAPI's dependency system.

Benefits include:

easier testing
reduced coupling
easier replacement of implementations
improved maintainability
9.4 Repository Pattern

Persistence is isolated inside the repository layer.

The application should not know whether investigations are stored in:

JSON
SQLite
PostgreSQL
MongoDB

Only the repository knows.

This allows storage technologies to change without affecting the rest of the application.

9.5 Models Represent Data

Pydantic models define the structure of incoming and outgoing data.

Examples include:

SupportCase
InvestigationResult
CaseResponse
Statistics
ErrorResponse

Using explicit models provides:

validation
documentation
serialization
consistency
9.6 Exceptions Represent Business Failures

Unexpected situations should not be handled using arbitrary dictionaries or manual HTTP responses.

Instead, meaningful exceptions are raised.

Examples:

CaseNotFoundException

The global exception handler converts these exceptions into consistent API responses.

9.7 Testing is Part of Development

Features are not considered complete until they are verified through automated tests.

Current tests cover:

successful investigation
unknown case retrieval
statistics endpoint

Testing protects the project from regressions as new features are added.

9.8 Engineering Evolution

The backend architecture has grown progressively through the project.

Sprint 1

Simple FastAPI endpoint.

↓

Sprint 2

Business logic introduced.

↓

Sprint 3

Models added.

↓

Sprint 4

Persistence layer created.

↓

Sprint 5

Configuration improvements.

↓

Sprint 6

Repository Pattern.

↓

Sprint 7

Dependency Injection.

↓

Sprint 8

Exception Handling.

↓

Sprint 9

Automated Testing and Typed Responses.

Future sprints will continue refining the architecture while preserving these engineering principles.

End of Volume II (Current)

This document is intentionally incomplete.

Additional chapters will be added as the project evolves.

Each architectural improvement should first be implemented in code before it is documented here.