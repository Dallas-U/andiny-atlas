# Andiny Atlas Production Configuration Contract

## Purpose

This document defines the minimum configuration requirements for
running Andiny Atlas in a production environment.

Production configuration must satisfy the application's deployment
safety rules before Andiny Atlas is used for live enterprise
operations.

This contract reflects the current deployment safety rules implemented
in:

```text
backend/app/core/settings.py
```

---

# 1. Production Environment

A production deployment must use:

```text
ENVIRONMENT=production
```

Production represents the live operational environment for:

- Enterprise customer organizations
- Authorized customer users
- Live investigations
- Enterprise administration
- Operational reporting
- Production analytics

Production must remain separated from development, testing, and
demonstration workflows.

---

# 2. ENVIRONMENT Requirements

The application currently supports the following deployment lifecycle
values:

```text
development
testing
staging
production
```

For live enterprise operations:

```text
ENVIRONMENT=production
```

must be configured.

Any unsupported `ENVIRONMENT` value is rejected by application
configuration validation.

---

# 3. ATLAS_ENV Requirements

The application currently supports:

```text
development
demo
test
```

`ATLAS_ENV` determines the Andiny Atlas runtime and data context.

## Production Restriction

When:

```text
ENVIRONMENT=production
```

the following configuration is prohibited:

```text
ATLAS_ENV=demo
```

The application rejects a production configuration using the demo
runtime context.

This prevents demonstration behavior and demonstration data from being
used accidentally in live enterprise operations.

---

# 4. Development Seed Restrictions

Production deployments must not permit development seed behavior.

The following configuration is prohibited:

```text
ALLOW_DEVELOPMENT_SEED=true
```

Production deployments must use:

```text
ALLOW_DEVELOPMENT_SEED=false
```

This prevents development-only seed behavior from being enabled during
live enterprise operations.

---

# 5. JWT Secret Requirements

`JWT_SECRET_KEY` is required for authentication and token security.

The JWT secret must:

- Be configured
- Not be empty
- Contain at least 32 characters in production

A production configuration with an insufficient JWT secret is rejected
by the application.

Example:

```text
JWT_SECRET_KEY=<secure-secret-with-at-least-32-characters>
```

The production JWT secret must not be:

- Empty
- A development placeholder
- Easily predictable
- Committed to the source code repository

Production secrets must be managed securely.

---

# 6. JWT Configuration

The current application configuration includes:

```text
JWT_ALGORITHM=HS256
JWT_ISSUER=AndinyAtlas
```

These values should remain consistent with the application's
authentication configuration unless the authentication architecture is
intentionally changed.

---

# 7. Access Token Configuration

The access token expiration must be greater than zero.

Example:

```text
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The actual expiration value may be adjusted according to enterprise
security requirements.

However, the application rejects values less than or equal to zero.

---

# 8. Logging Configuration

The application supports a logging configuration value:

```text
LOG_LEVEL=INFO
```

Production logging should use an appropriate operational log level.

Sensitive information, including passwords and secrets, must not be
written to application logs.

---

# 9. Recommended Production Configuration

A production deployment should use configuration equivalent to:

```text
APP_NAME=Andiny Atlas
APP_VERSION=0.19.0

ENVIRONMENT=production

ATLAS_ENV=development

LOG_LEVEL=INFO

JWT_SECRET_KEY=<secure-secret-with-at-least-32-characters>
JWT_ALGORITHM=HS256
JWT_ISSUER=AndinyAtlas

ACCESS_TOKEN_EXPIRE_MINUTES=30

ALLOW_DEVELOPMENT_SEED=false
```

The exact infrastructure-specific configuration may vary by deployment
environment.

Sensitive values must not be committed to Git.

---

# 10. Production Health Checks

The current application exposes the following health endpoints:

```text
/health
/health/live
/health/ready
```

## General Health Check

```text
GET /health
```

This endpoint provides the general application health status.

## Liveness Check

```text
GET /health/live
```

This endpoint confirms that the application process is alive.

## Readiness Check

```text
GET /health/ready
```

This endpoint confirms that the application is ready to operate and
that its configured database is available.

Production infrastructure and monitoring systems should use these
endpoints for operational health monitoring.

---

# 11. Production Deployment Validation

Production configuration is validated by the application settings
implementation:

```text
backend/app/core/settings.py
```

Current validation includes:

- Valid `ENVIRONMENT`
- Valid `ATLAS_ENV`
- Non-empty `JWT_SECRET_KEY`
- Positive `ACCESS_TOKEN_EXPIRE_MINUTES`
- Production demo-environment restrictions
- Production development-seed restrictions
- Minimum production JWT secret length

Invalid production configuration must be corrected before the
application is used for live operations.

---

# 12. Production Deployment Checklist

Before releasing Andiny Atlas to production, confirm:

1. `ENVIRONMENT=production`.
2. `ATLAS_ENV` is not set to `demo`.
3. `ALLOW_DEVELOPMENT_SEED=false`.
4. `JWT_SECRET_KEY` is configured securely.
5. The JWT secret contains at least 32 characters.
6. `ACCESS_TOKEN_EXPIRE_MINUTES` is greater than zero.
7. Sensitive configuration is not committed to Git.
8. Automated tests pass.
9. `/health` responds successfully.
10. `/health/live` responds successfully.
11. `/health/ready` responds successfully.
12. The approved application release is being deployed.

---

# 13. Current Production Safety Boundary

The current production safety boundary is implemented primarily in:

```text
backend/app/core/settings.py
```

and validated through the Andiny Atlas backend test suite.

The health endpoints supporting operational monitoring are implemented
in:

```text
backend/app/main.py
```

---

# 14. Infrastructure Responsibilities

The current application-level configuration validation provides a
deployment safety boundary.

Future production infrastructure requirements may include:

- Managed database infrastructure
- Secure secret management
- HTTPS termination
- Backup and recovery procedures
- Monitoring and alerting
- Centralized logging
- Deployment orchestration
- Disaster recovery planning

These infrastructure capabilities should be documented separately when
they are introduced into the approved Andiny Atlas architecture.

---

# 15. Related Documentation

Related documentation includes:

- `docs/deployment/DEPLOYMENT_ENVIRONMENT_MATRIX.md`
- `docs/demo/ANDINY_ATLAS_DEMONSTRATION_ENVIRONMENT.md`
- `backend/app/core/settings.py`
- `backend/app/main.py`