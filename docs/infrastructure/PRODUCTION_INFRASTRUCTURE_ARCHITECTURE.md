# Andiny Atlas Production Infrastructure Architecture

## Purpose

This document defines the target production infrastructure architecture for
Andiny Atlas.

The purpose of this architecture is to provide a secure, reliable, scalable,
and operationally manageable foundation for deploying Andiny Atlas as an
enterprise application.

The infrastructure architecture must support the established Andiny Atlas
application architecture without changing or weakening:

- Organization as the tenant boundary;
- authentication controls;
- authorization rules;
- role-based capabilities;
- tenant isolation;
- platform governance;
- organization lifecycle controls; and
- immutable audit and case history controls.

This document defines infrastructure responsibilities and deployment boundaries.
It does not replace application-level security or authorization controls.

---

# 1. Architecture Principles

The Andiny Atlas production infrastructure must follow these principles.

## 1.1 Preserve the Existing Application Architecture

Production infrastructure must support the existing Andiny Atlas architecture.

Infrastructure deployment must not:

- bypass application authorization;
- weaken tenant isolation;
- expose cross-organization data;
- introduce unrestricted administrative access;
- replace Organization-based tenant boundaries; or
- alter established platform governance rules.

The application remains responsible for enforcing:

- authentication;
- authorization;
- role restrictions;
- organization scope;
- branch scope;
- department scope; and
- tenant isolation.

---

## 1.2 Organization Remains the Tenant Boundary

Andiny Atlas uses the **Organization** as the enterprise tenant boundary.

Production infrastructure must preserve this model.

Customer organizations must remain logically isolated according to the existing
application authorization and data-access rules.

Infrastructure-level separation does not replace application-level tenant
isolation.

The established model remains:

```text
Organization
    │
    ├── Branches
    │      │
    │      └── Departments
    │
    ├── Authorized Users
    │
    ├── Investigations / Cases
    │
    ├── Case History / Audit
    │
    ├── Reports
    │
    └── Analytics
```

Platform governance remains outside customer tenant scope.

---

# 2. Target Production Architecture

The target production architecture consists of separate logical layers.

```text
                           INTERNET
                               │
                               ▼
                        DOMAIN / DNS
                               │
                               ▼
                         HTTPS / TLS
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
       FRONTEND HOSTING                 BACKEND HOSTING
       React Application              Container Platform
                │                             │
                │                             ▼
                │                    Andiny Atlas API
                │                       FastAPI
                │                             │
                │                             ▼
                │                  Production Database
                │                             │
                │                             ▼
                │                    Backup / Recovery
                │
                ▼
              USERS
```

The architecture separates the following responsibilities:

1. frontend delivery;
2. backend application execution;
3. production data persistence;
4. secrets management;
5. networking and HTTPS;
6. logging and monitoring; and
7. backup and recovery.

---

# 3. Frontend Infrastructure Boundary

The Andiny Atlas frontend is responsible for providing the enterprise user
interface.

The frontend production environment will host the compiled React application.

The frontend hosting layer must provide:

- secure HTTPS delivery;
- production application build hosting;
- environment-specific configuration;
- reliable static asset delivery;
- controlled API endpoint configuration; and
- separation between development and production environments.

The frontend must communicate only with approved production backend API
endpoints.

Production frontend configuration must not expose:

- backend secrets;
- JWT signing secrets;
- database credentials;
- cloud provider credentials; or
- internal infrastructure credentials.

---

# 4. Backend Container Boundary

The Andiny Atlas backend will be prepared for container-based deployment.

The backend container will contain:

```text
Andiny Atlas Backend Container
│
├── Python Runtime
├── Application Dependencies
├── Backend Application
├── FastAPI
├── Application Server
└── Runtime Configuration
```

The container must be capable of running the Andiny Atlas backend consistently
across approved environments.

The container must not contain permanent production secrets.

Production configuration must be injected through approved environment and
secrets management mechanisms.

---

# 5. Application Runtime

The Andiny Atlas backend application uses FastAPI.

The production runtime must:

- start the application successfully;
- load approved production configuration;
- enforce production safety restrictions;
- expose approved health endpoints;
- connect to the approved production database; and
- terminate gracefully when required.

The application health model includes:

```text
/health
/health/live
/health/ready
```

These endpoints provide operational visibility into:

- application status;
- application liveness; and
- database readiness.

---

# 6. Production Database Boundary

The production database must remain independent from the application container.

The production database must not be treated as disposable container data.

The database must have its own:

- persistence strategy;
- access controls;
- backup process;
- recovery process;
- availability monitoring; and
- operational ownership.

The application container must be replaceable without destroying production
data.

The production database strategy must ensure that:

```text
Container replacement
        ≠
Data loss
```

---

# 7. Database Access

Database access must follow the principle of least privilege.

The backend application should receive only the database permissions required
for normal application operation.

Production database credentials must:

- remain outside source control;
- remain outside committed Docker images;
- be stored securely;
- be restricted to authorized infrastructure processes; and
- be rotated according to operational security requirements.

Development database configuration must not be reused as production
configuration.

---

# 8. Environment Separation

Andiny Atlas environments must remain deliberately separated.

The supported environments include:

```text
development
testing
staging
production
```

Production must not inherit unsafe development behavior.

Production configuration must enforce:

- production environment settings;
- approved production database configuration;
- demo restrictions;
- development seed restrictions;
- strong JWT secret requirements; and
- production-safe credentials.

The environment model is governed by:

- `docs/deployment/DEPLOYMENT_ENVIRONMENT_MATRIX.md`
- `docs/deployment/PRODUCTION_CONFIGURATION_CONTRACT.md`

---

# 9. Secrets Management

Production secrets must never be committed to source control.

The following are considered sensitive:

- JWT secrets;
- database credentials;
- production API credentials;
- cloud provider credentials;
- infrastructure access credentials; and
- third-party service secrets.

Production secrets must be injected into the application through an approved
secrets management mechanism.

The following must never be committed:

```text
backend/.env
production credentials
production secrets
private keys
cloud access keys
```

Example configuration files may be committed only when they contain no real
production credentials.

---

# 10. Networking Architecture

Production networking must separate public and internal responsibilities.

The public-facing layers include:

```text
Domain
HTTPS
Frontend
Approved API access
```

Internal infrastructure may include:

```text
Backend application
Database
Secrets
Monitoring services
```

The production database should not be unnecessarily exposed directly to the
public internet.

Only approved backend services should require access to production database
services.

---

# 11. Domain and DNS

The production deployment will require an approved domain strategy.

The domain architecture should support separate endpoints where appropriate.

Example:

```text
https://app.<production-domain>
```

for the frontend application, and:

```text
https://api.<production-domain>
```

for the backend API.

The final domain names will be determined during production hosting
configuration.

DNS configuration must be controlled and documented.

---

# 12. HTTPS and TLS

Production traffic must use HTTPS.

HTTPS must protect:

- user authentication;
- API communication;
- investigation data;
- organization information; and
- enterprise operations.

HTTP-only production access should not be used for normal user application
traffic.

TLS certificates must be managed through the approved hosting or infrastructure
platform.

Certificate renewal must be monitored or automatically managed.

---

# 13. Container Security Principles

The backend container must follow secure deployment principles.

These include:

- minimal required runtime dependencies;
- no production secrets embedded in the image;
- controlled environment configuration;
- reproducible builds;
- explicit dependency installation;
- approved application startup commands; and
- regular dependency maintenance.

The container image must represent an application artifact.

The image must not become a storage location for:

- production data;
- production credentials; or
- environment-specific secrets.

---

# 14. Logging

Production infrastructure must provide access to application logs.

Logging must support investigation of:

- startup failures;
- application errors;
- authentication failures;
- database connection failures; and
- unexpected operational conditions.

Logs must not expose:

- passwords;
- JWT secrets;
- database credentials;
- private tokens; or
- sensitive production secrets.

Operational logging must complement the existing application audit and case
history controls.

---

# 15. Monitoring and Health Checks

Production infrastructure must monitor application availability.

The existing Andiny Atlas health endpoints provide the initial operational
monitoring foundation.

The required endpoints are:

```text
/health
/health/live
/health/ready
```

The monitoring system should detect:

- application failure;
- application unavailability;
- liveness failure;
- database readiness failure; and
- repeated operational errors.

Health monitoring must be included in production operational procedures.

---

# 16. Backup and Recovery

Production deployment requires a defined backup and recovery strategy.

The production database must have:

- scheduled backups;
- backup retention rules;
- verified backup storage;
- documented recovery procedures; and
- identified recovery ownership.

A successful backup is not sufficient unless recovery procedures are also
available.

Production deployment must preserve the ability to recover from:

- infrastructure failure;
- application deployment failure;
- database failure; and
- accidental data loss.

---

# 17. Rollback Architecture

Every production release must have a rollback path.

The rollback strategy must identify:

- the previous stable application version;
- the previous deployment artifact;
- rollback ownership;
- database recovery requirements; and
- rollback decision criteria.

Application rollback must be coordinated with database changes.

Production releases must not introduce irreversible changes without an approved
recovery strategy.

The formal rollback process is governed by:

```text
docs/deployment/PRODUCTION_DEPLOYMENT_CHECKLIST.md
```

and:

```text
docs/deployment/DEPLOYMENT_RUNBOOK.md
```

---

# 18. Infrastructure and Application Responsibilities

The production architecture separates responsibilities between infrastructure
and the application.

| Responsibility | Infrastructure | Application |
|---|---|---|
| HTTPS | Yes | No |
| Container execution | Yes | No |
| Secrets injection | Yes | No |
| Database hosting | Yes | No |
| Backup infrastructure | Yes | No |
| Authentication rules | No | Yes |
| Authorization rules | No | Yes |
| Tenant isolation | No | Yes |
| Organization scope | No | Yes |
| Role enforcement | No | Yes |
| Case audit history | No | Yes |

Infrastructure must not be relied upon as a replacement for application
security controls.

---

# 19. Production Deployment Governance

Production infrastructure deployment must follow the established deployment
governance documentation.

The governing documents are:

- `docs/deployment/DEPLOYMENT_ENVIRONMENT_MATRIX.md`
- `docs/deployment/PRODUCTION_CONFIGURATION_CONTRACT.md`
- `docs/deployment/DEPLOYMENT_RUNBOOK.md`
- `docs/deployment/PRODUCTION_DEPLOYMENT_CHECKLIST.md`

The deployment validation script is:

```text
scripts/validate_deployment.ps1
```

Production deployment must pass the defined release gates before formal
production approval.

---

# 20. Implementation Roadmap

The container-based production preparation will proceed in the following order.

## Step 6.1 — Production Infrastructure Architecture

Define and document the infrastructure architecture.

## Step 6.2 — Backend Containerization

Create and validate:

```text
Dockerfile
.dockerignore
```

## Step 6.3 — Container Environment Validation

Prepare controlled container execution and local validation.

## Step 6.4 — Production Environment Strategy

Define:

- production environment variables;
- secrets injection;
- configuration management; and
- production safety controls.

## Step 6.5 — Production Database Strategy

Review the current persistence architecture and define the approved production
database approach.

## Step 6.6 — Frontend Production Deployment

Prepare the frontend for:

- production builds;
- production API configuration; and
- frontend hosting.

## Step 6.7 — Cloud Hosting Selection

Select approved services for:

- backend container hosting;
- production database;
- frontend hosting;
- secrets management; and
- operational monitoring.

## Step 6.8 — Domain and HTTPS

Configure:

- production domains;
- DNS;
- HTTPS; and
- secure frontend-to-backend communication.

## Step 6.9 — Monitoring and Operational Readiness

Prepare:

- application monitoring;
- health monitoring;
- logging; and
- operational response procedures.

## Step 6.10 — Production Deployment Execution

Deploy using the approved production infrastructure and follow the established
deployment governance and release sign-off procedures.

---

# 21. Architecture Protection Statement

The production infrastructure architecture must preserve the established
Andiny Atlas system architecture.

In particular:

- **Organization remains the tenant boundary.**
- Roles continue to determine capabilities.
- Organization and scope continue to determine accessible data.
- Customer users remain tenant-bound.
- Customer administrators cannot create platform Super Admins.
- Platform governance remains outside customer tenant scope.
- Organization lifecycle controls remain enforced.
- Authorization and tenant isolation remain application responsibilities.

Containerization and cloud infrastructure provide deployment and operational
capabilities.

They do not replace the established Andiny Atlas security and governance
architecture.

---

# 22. Approval Requirement

Changes to production infrastructure must be reviewed before they are treated
as approved production architecture.

Production infrastructure implementation must not proceed in a way that:

- bypasses deployment validation;
- exposes production secrets;
- weakens authentication;
- weakens authorization;
- compromises tenant isolation;
- removes rollback capability; or
- introduces uncontrolled production configuration.

This document serves as the architectural baseline for the container-based
production deployment of Andiny Atlas.