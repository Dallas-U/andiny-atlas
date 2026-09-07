# Andiny Atlas Deployment Environment Matrix

## Purpose

This document defines the supported deployment and runtime
environments for Andiny Atlas and establishes the rules for each
environment.

The objective is to ensure that development, testing, staging,
demonstration, and production environments remain clearly separated
and that development-only functionality cannot accidentally be enabled
in production.

---

# 1. Environment Configuration Model

Andiny Atlas uses two related configuration controls:

- `ENVIRONMENT`
- `ATLAS_ENV`

These controls serve different purposes and must not be confused.

## ENVIRONMENT

`ENVIRONMENT` defines the application deployment lifecycle.

Allowed values are:

```text
development
testing
staging
production
```

## ATLAS_ENV

`ATLAS_ENV` defines the Andiny Atlas runtime and data context.

Allowed values are:

```text
development
demo
test
```

---

# 2. Development Environment

## Configuration

```text
ENVIRONMENT=development
ATLAS_ENV=development
```

## Purpose

The development environment is intended for:

- Local developer implementation
- Feature development
- Debugging
- Local testing
- Development workflows

Development-only seed functionality may be enabled when required:

```text
ALLOW_DEVELOPMENT_SEED=true
```

Development configuration must not be used for live enterprise
operations.

---

# 3. Testing Environment

## Configuration

A typical testing configuration is:

```text
ENVIRONMENT=testing
ATLAS_ENV=test
```

## Purpose

The testing environment is intended for:

- Automated tests
- Integration tests
- Regression tests
- Manual validation
- Test-specific data

Testing must remain isolated from production operations and production
customer data.

---

# 4. Demonstration Environment

## Configuration

A demonstration runtime may use:

```text
ENVIRONMENT=development
ATLAS_ENV=demo
```

The current application architecture does not define `demo` as an
`ENVIRONMENT` value. Instead, demonstration behavior is controlled
through `ATLAS_ENV=demo`.

## Purpose

The demonstration environment is intended for:

- Controlled product demonstrations
- Product presentations
- Demo organizations
- Demonstration users
- Demonstration investigations
- Demonstration data

Demo data must not be used for live production operations.

---

# 5. Staging Environment

## Configuration

A staging deployment uses:

```text
ENVIRONMENT=staging
```

The appropriate `ATLAS_ENV` value must be selected according to the
deployment and data context supported by the application.

## Purpose

The staging environment is intended for:

- Pre-production validation
- Release testing
- Deployment verification
- Infrastructure validation
- Production-like operational testing

Staging should reflect production configuration as closely as practical
without becoming the live production environment.

---

# 6. Production Environment

## Configuration

A production deployment must use:

```text
ENVIRONMENT=production
```

Production is intended for:

- Live enterprise customer operations
- Customer organizations
- Authorized users
- Live investigations
- Enterprise administration
- Production reporting
- Production analytics

Production configuration is subject to additional application safety
validation.

Production deployments must follow:

```text
docs/deployment/PRODUCTION_CONFIGURATION_CONTRACT.md
```

---

# 7. Configuration Relationship

`ENVIRONMENT` and `ATLAS_ENV` work together but serve different
purposes.

`ENVIRONMENT` determines the application deployment lifecycle.

`ATLAS_ENV` determines the Atlas runtime and data context.

Example development configuration:

```text
ENVIRONMENT=development
ATLAS_ENV=development
```

Example testing configuration:

```text
ENVIRONMENT=testing
ATLAS_ENV=test
```

Example demonstration configuration:

```text
ENVIRONMENT=development
ATLAS_ENV=demo
```

Example staging configuration:

```text
ENVIRONMENT=staging
ATLAS_ENV=development
```

Production configuration must comply with the production safety rules
implemented by the application.

---

# 8. Production Safety Rules

When:

```text
ENVIRONMENT=production
```

the application enforces additional safety rules.

## Demo Restriction

Production cannot use:

```text
ATLAS_ENV=demo
```

The application rejects this configuration.

## Development Seed Restriction

Production cannot use:

```text
ALLOW_DEVELOPMENT_SEED=true
```

Development seed functionality must be disabled.

## JWT Secret Requirement

The production JWT secret must:

- Be configured
- Not be empty
- Contain at least 32 characters

Production configuration with an insufficient JWT secret is rejected.

---

# 9. Database Runtime Context

Andiny Atlas currently determines the SQLite database name from
`ATLAS_ENV`.

The current behavior is:

```text
ATLAS_ENV=demo  -> atlas_demo.db
ATLAS_ENV=test  -> atlas_test.db
other values    -> andiny_atlas.db
```

This provides separation between demonstration, testing, and normal
application data contexts.

---

# 10. Deployment Validation

Deployment configuration is implemented and validated in:

```text
backend/app/core/settings.py
```

Current validation includes:

- Valid `ENVIRONMENT` values
- Valid `ATLAS_ENV` values
- Non-empty `JWT_SECRET_KEY`
- Positive `ACCESS_TOKEN_EXPIRE_MINUTES`
- Production demo-environment restrictions
- Production development-seed restrictions
- Minimum production JWT secret length

These validations provide an application-level deployment safety
boundary.

---

# 11. Operational Rule

Deployment configuration must always be deliberately selected.

Development, testing, staging, demonstration, and production
environments must not share configuration carelessly.

Production deployments must not accidentally enable:

- Demonstration behavior
- Development seed behavior
- Weak JWT secrets
- Invalid deployment configuration

---

# 12. Related Documentation

The following documents are related to this deployment model:

- `docs/deployment/PRODUCTION_CONFIGURATION_CONTRACT.md`
- `docs/demo/ANDINY_ATLAS_DEMONSTRATION_ENVIRONMENT.md`
- `backend/app/core/settings.py`

---

# 13. Current Architecture Status

This document reflects the current deployment configuration implemented
in:

```text
backend/app/core/settings.py
```

Any future changes to the deployment architecture must update:

1. The application configuration implementation
2. This Deployment Environment Matrix
3. The Production Configuration Contract

This ensures that the documented deployment architecture remains
consistent with the implemented Andiny Atlas platform.