# Andiny Atlas Containerization Architecture

## Purpose

This document defines the containerization architecture for Andiny Atlas.

The purpose of this architecture is to provide a consistent, portable, secure,
and production-ready method for packaging and running Andiny Atlas using
containers.

Containerization must support the established Andiny Atlas application and
infrastructure architecture without changing or weakening:

- Organization as the tenant boundary;
- authentication controls;
- authorization rules;
- role-based capabilities;
- tenant isolation;
- platform governance;
- organization lifecycle controls; and
- immutable audit and case history controls.

This document defines how Andiny Atlas application components are packaged,
configured, connected, validated, and prepared for cloud deployment.

---

# 1. Containerization Principles

The Andiny Atlas container architecture must follow these principles:

1. Application containers must be reproducible.
2. Development and production environments must remain clearly separated.
3. Production secrets must not be embedded in container images.
4. Application configuration must be supplied through approved environment
   configuration mechanisms.
5. Containers must remain stateless where practical.
6. Persistent data must not depend on temporary container filesystems.
7. Health checks must be available for operational monitoring.
8. Container images must be versioned and traceable to approved source code.
9. Production deployments must support rollback.
10. Containerization must not bypass application-level security controls.

---

# 2. Target Container Architecture

The target Andiny Atlas deployment architecture consists of the following
logical components:

```text
                    Internet / Enterprise Users
                               |
                               v
                    +-----------------------+
                    | Load Balancer / HTTPS |
                    | Reverse Proxy         |
                    +-----------+-----------+
                                |
                +---------------+---------------+
                |                               |
                v                               v
      +-------------------+         +-------------------+
      | Frontend Container|         | Backend Container |
      |                   |         |                   |
      | React Application |         | FastAPI Service   |
      +-------------------+         +---------+---------+
                                              |
                                              v
                                  +----------------------+
                                  | Production Database  |
                                  +----------------------+
```

The exact cloud services used to implement these logical components may vary.

The logical architecture must remain consistent regardless of the selected
cloud provider.

---

# 3. Application Components

Andiny Atlas is expected to run as separate logical application components.

## 3.1 Frontend

The frontend container is responsible for serving the Andiny Atlas user
interface.

Responsibilities include:

- serving the compiled frontend application;
- providing the enterprise user interface;
- communicating with the backend API through approved endpoints;
- supporting secure HTTPS delivery through the infrastructure layer.

The frontend container must not contain:

- production secrets;
- database credentials;
- backend private keys;
- JWT secrets.

---

## 3.2 Backend

The backend container is responsible for running the Andiny Atlas application
API.

The backend provides:

- authentication;
- authorization;
- tenant isolation;
- organization management;
- branch and department access control;
- investigation and case operations;
- analytics;
- reports;
- exports;
- audit and case history;
- health and readiness endpoints.

The backend container must load configuration through approved environment
configuration.

Production secrets must not be hard-coded into the container image.

---

## 3.3 Database

The database is a persistent infrastructure component.

Production database responsibilities include:

- storing application data;
- preserving organization boundaries;
- preserving investigation records;
- preserving audit history;
- supporting approved backup procedures;
- supporting recovery procedures.

The production database must not depend on a temporary container filesystem.

For production cloud deployment, a managed database service is preferred where
appropriate.

---

# 4. Container Boundaries

Each major application responsibility should remain logically separated.

The preferred container boundaries are:

| Component | Responsibility |
|---|---|
| Frontend Container | Serves the Andiny Atlas frontend |
| Backend Container | Runs the Andiny Atlas API |
| Database Service | Provides persistent application storage |
| Reverse Proxy / Load Balancer | Handles external routing and HTTPS |

Container boundaries must not change the established application authorization
or tenant isolation architecture.

---

# 5. Backend Container Architecture

The backend container will package the Andiny Atlas backend application and
its required runtime dependencies.

The backend container must include:

- the supported Python runtime;
- backend application dependencies;
- the Andiny Atlas backend application;
- the approved application startup command.

The backend container must not include:

- development-only credentials;
- production secrets embedded in source files;
- unnecessary development tools where avoidable;
- development seed data in production mode.

---

## 5.1 Backend Startup

The backend container will run the approved ASGI application.

The application entry point remains based on the existing Andiny Atlas backend
architecture.

The container startup process must support:

- controlled environment configuration;
- application startup validation;
- health checks;
- production logging;
- graceful failure reporting.

---

# 6. Frontend Container Architecture

The frontend container will package the Andiny Atlas frontend application.

The recommended approach is:

1. build the frontend application;
2. produce optimized static assets;
3. serve those assets using an approved production web server.

The production frontend image should not require the full development
environment.

The production container should contain only the components required to serve
the approved frontend build.

---

# 7. Environment Configuration

Application configuration must remain external to the container image.

Environment-specific values may include:

- `ENVIRONMENT`;
- `ATLAS_ENV`;
- `ATLAS_ENVIRONMENT`;
- database configuration;
- JWT configuration;
- allowed origins;
- API configuration;
- production service configuration.

The production environment must comply with:

```text
docs/deployment/PRODUCTION_CONFIGURATION_CONTRACT.md
```

The container architecture must not override or weaken the production
configuration contract.

---

# 8. Secrets Management

Production secrets must not be committed to source control.

Production secrets must not be embedded directly into Docker images.

Examples of protected values include:

- JWT secrets;
- database credentials;
- API credentials;
- private keys;
- cloud provider credentials.

Production secrets should be supplied through an approved secrets management
mechanism provided by the selected deployment environment.

Examples may include:

- cloud secrets management;
- managed environment secrets;
- encrypted deployment secrets.

The exact implementation will be determined during cloud provider preparation.

---

# 9. Container Networking

Containers must communicate only through approved network paths.

The logical communication flow is:

```text
User
  |
  v
HTTPS / Load Balancer
  |
  +-------------------+
  |                   |
  v                   v
Frontend           Backend API
                        |
                        v
                    Database
```

The database should not be directly exposed to the public internet unless a
specific approved infrastructure requirement exists.

Internal services should use private networking where supported.

---

# 10. Persistent Storage

Containers should be treated as replaceable runtime units.

Persistent application data must not depend on container-local storage.

Persistent data includes:

- production database records;
- investigation records;
- audit history;
- approved uploaded files;
- generated artifacts requiring long-term retention.

Persistent storage must use an approved external or managed storage mechanism.

---

# 11. Health Checks

Andiny Atlas already provides application health endpoints.

The container deployment must use these endpoints for operational validation.

## Application Health

```text
/health
```

Expected application status:

```text
running
```

## Liveness

```text
/health/live
```

Expected status:

```text
alive
```

## Readiness

```text
/health/ready
```

Expected status:

```text
ready
```

The readiness endpoint must confirm that required dependencies, including the
database where applicable, are available.

These endpoints will be used during:

- container validation;
- deployment validation;
- cloud health monitoring;
- production release verification.

---

# 12. Development and Production Separation

Container configuration must support clear separation between development and
production.

## Development

Development containers may support:

- local development;
- local debugging;
- controlled testing;
- local environment configuration.

Development configuration must not be used as production configuration.

---

## Production

Production containers must support:

- optimized application execution;
- production environment configuration;
- secure secret injection;
- health monitoring;
- controlled logging;
- rollback capability.

Production mode must comply with the existing production safety controls.

---

# 13. Production Safety Requirements

Containerization must preserve the production safety rules already established
for Andiny Atlas.

Production deployment must confirm:

- `ENVIRONMENT` is set to `production`;
- approved production environment settings are used;
- demo mode is disabled;
- development seed data is disabled;
- strong JWT configuration is used;
- production credentials are securely managed;
- development credentials are not used;
- sensitive values are not exposed in container images or logs.

The existing deployment validation procedure remains mandatory.

---

# 14. Tenant Isolation and Security

Containerization does not replace application security.

The Andiny Atlas application remains responsible for enforcing:

- Organization as the tenant boundary;
- user authentication;
- role-based authorization;
- organization-scoped access;
- branch-scoped access where applicable;
- department-scoped access where applicable;
- platform governance restrictions.

The container infrastructure must not introduce a path that bypasses these
controls.

---

# 15. Image Versioning

Container images must be traceable to approved application releases.

Each production image should be associated with:

- application version;
- source commit;
- release identifier;
- build date where appropriate.

The deployment process must make it possible to identify which application
version is currently running.

Recommended image versioning should support both:

```text
release version
```

and:

```text
source commit identifier
```

where practical.

---

# 16. Image Registry

Production container images should be stored in an approved container registry.

The registry must support:

- controlled access;
- image versioning;
- deployment retrieval;
- release traceability.

The exact registry will depend on the selected cloud provider.

Examples of possible registry approaches include:

- GitHub Container Registry;
- cloud provider container registries;
- another approved enterprise registry.

The final registry choice will be made during cloud infrastructure preparation.

---

# 17. Logging and Observability

Containers must produce operational logs that can be accessed through the
approved deployment platform.

Operational logging should support identification of:

- application startup failures;
- unexpected application errors;
- authentication failures;
- database connectivity failures;
- deployment failures.

Logs must not expose:

- JWT secrets;
- passwords;
- database credentials;
- private keys;
- sensitive production configuration.

The cloud deployment platform will provide the final log aggregation and
monitoring mechanism.

---

# 18. Rollback Architecture

Container-based deployment must support rollback to a previously approved
application version.

Rollback capability requires:

- previous approved images remain identifiable;
- previous release versions remain available;
- deployment history is traceable;
- database backup procedures exist;
- rollback ownership is defined.

Rollback requirements remain governed by:

```text
docs/deployment/PRODUCTION_DEPLOYMENT_CHECKLIST.md
```

A production deployment must not proceed without an identified rollback path.

---

# 19. Local Container Validation

Before cloud deployment, the container architecture must be validated locally.

Validation must confirm:

- backend image builds successfully;
- frontend image builds successfully;
- containers start successfully;
- environment configuration loads correctly;
- backend health checks pass;
- database readiness works;
- frontend can communicate with the backend where applicable.

Local container validation does not replace production deployment validation.

---

# 20. Docker Compose

Docker Compose will be used as the initial orchestration mechanism for local
container validation.

The Docker Compose configuration will define the approved local relationship
between:

- frontend;
- backend;
- database or approved database configuration;
- required environment configuration.

Docker Compose will provide a controlled environment for validating the
container architecture before cloud deployment.

The local Compose configuration must not contain production secrets.

---

# 21. Cloud Deployment Boundary

Docker and containerization provide the application packaging layer.

The cloud platform provides infrastructure services such as:

- container hosting;
- networking;
- HTTPS;
- load balancing;
- secrets management;
- managed databases;
- logging;
- monitoring.

The final cloud implementation will be selected and documented separately.

Containerization must remain cloud-portable where practical.

---

# 22. Implementation Sequence

The approved implementation sequence is:

1. Create and approve this containerization architecture.
2. Create the backend Dockerfile.
3. Build and validate the backend container.
4. Create the frontend Dockerfile.
5. Build and validate the frontend container.
6. Create Docker Compose configuration.
7. Validate the complete local container environment.
8. Verify health and readiness endpoints.
9. Document container validation procedures.
10. Commit and push the containerization implementation.
11. Prepare the selected cloud infrastructure.
12. Deploy to a controlled production environment.

---

# 23. Approval Requirement

Container implementation must not proceed in a way that:

- embeds production secrets in images;
- bypasses production configuration validation;
- weakens authentication;
- weakens authorization;
- compromises tenant isolation;
- removes rollback capability;
- exposes the database unnecessarily;
- introduces uncontrolled production configuration.

This document serves as the architectural baseline for containerizing Andiny
Atlas and preparing the application for container-based cloud deployment.

---

# 24. Architecture Continuity Statement

The Andiny Atlas container architecture is an infrastructure implementation
layer.

It does not replace or modify the established Andiny Atlas application
architecture.

The following architectural decisions remain unchanged:

- **Organization is the tenant and customer deployment boundary.**
- Roles determine capability.
- Organization and scope determine accessible data.
- Customer users remain tenant-bound.
- Customer administrators cannot create platform Super Admins.
- Platform governance remains outside customer scope.
- Organization lifecycle controls remain security and business controls.
- Authorization and tenant isolation remain mandatory application controls.
- Immutable audit and case history remain protected.

Containerization exists to make the approved Andiny Atlas application easier to
deploy, operate, scale, monitor, and recover.

It must always preserve the architecture and governance already established
for the platform.