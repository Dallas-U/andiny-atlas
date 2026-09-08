# Andiny Atlas Production Deployment Checklist and Release Sign-Off Procedure

## Purpose

This document provides the mandatory checklist and formal sign-off procedure for deploying Andiny Atlas to a production environment.

The checklist ensures that:

- approved source code is deployed;
- dependencies are verified;
- production configuration is validated;
- automated tests pass;
- production safety controls are enforced;
- application startup succeeds;
- health and readiness checks pass;
- tenant isolation remains protected;
- database readiness is confirmed;
- functional verification is completed;
- rollback readiness exists; and
- formal release approval is recorded.

This document should be used together with:

- `docs/deployment/DEPLOYMENT_RUNBOOK.md`
- `docs/deployment/DEPLOYMENT_ENVIRONMENT_MATRIX.md`
- `docs/deployment/PRODUCTION_CONFIGURATION_CONTRACT.md`
- `backend/.env.example`
- `scripts/validate_deployment.ps1`

---

# 1. Release Information

Record the release information before beginning deployment.

| Item | Details |
|---|---|
| Application | Andiny Atlas |
| Release Version | ________________________________ |
| Release Date | ________________________________ |
| Environment | Production |
| Deployment Engineer | ________________________________ |
| Technical Reviewer | ________________________________ |
| Release Approver | ________________________________ |
| Release Commit | ________________________________ |

---

# 2. Source Code Verification

Confirm that the correct branch and approved release code are being used.

Run:

```powershell
git status
```

Expected result:

```text
On branch master
Your branch is up to date with 'origin/master'.

nothing to commit, working tree clean
```

Update the repository:

```powershell
git pull origin master
```

Record the release commit:

```powershell
git log -1 --oneline
```

### Sign-Off

- [ ] Source code verified

Verified by: ________________________________

Date: ________________________________

---

# 3. Python and Dependency Verification

Confirm that the supported Python environment and application dependencies are available.

Check Python:

```powershell
python --version
```

Install or verify backend dependencies:

```powershell
pip install -r backend\requirements.txt
```

Expected result:

```text
Requirement already satisfied
```

Or a successful dependency installation without errors.

### Sign-Off

- [ ] Python environment verified
- [ ] Backend dependencies installed successfully

Verified by: ________________________________

Date: ________________________________

---

# 4. Environment Configuration Verification

Confirm that the required environment configuration exists before deployment.

Check for the backend environment file:

```powershell
Test-Path backend\.env
```

Expected result:

```text
True
```

Verify the active application configuration:

```powershell
python -c "from backend.app.core.settings import settings; print('Application:', settings.app_name); print('Version:', settings.app_version); print('ENVIRONMENT:', settings.environment); print('ATLAS_ENV:', settings.atlas_environment); print('Database:', settings.database_path)"
```

For production deployment, verify that the configuration matches the approved production configuration contract.

## Mandatory Production Checks

- [ ] `ENVIRONMENT` is set to `production`.
- [ ] `ATLAS_ENV` / `ATLAS_ENVIRONMENT` is approved for production use.
- [ ] Demo mode is not enabled.
- [ ] Development seed data is disabled.
- [ ] A strong JWT secret is configured.
- [ ] Production database configuration is correct.
- [ ] Production credentials are not development credentials.
- [ ] Sensitive values are not exposed in source code or logs.

### Sign-Off

- [ ] Production configuration verified

Verified by: ________________________________

Date: ________________________________

---

# 5. Automated Test Verification

All automated backend tests must pass before production deployment.

Run:

```powershell
pytest backend/tests -v
```

Record the result:

```text
Total Tests: __________________

Passed: __________________

Failed: __________________

Test Duration: __________________
```

## Release Requirement

Production deployment must not proceed if:

- [ ] any automated test fails;
- [ ] tenant isolation tests fail;
- [ ] authentication tests fail;
- [ ] authorization tests fail;
- [ ] production configuration tests fail; or
- [ ] health endpoint tests fail.

## Current Validated Baseline

The latest validated deployment readiness run recorded:

```text
178 passed
```

### Sign-Off

- [ ] All automated tests passed

Verified by: ________________________________

Date: ________________________________

---

# 6. Deployment Validation Script

Run the Andiny Atlas deployment validation script:

```powershell
.\scripts\validate_deployment.ps1
```

The validation must successfully confirm:

- [ ] Configuration loading
- [ ] Production safety rules
- [ ] Application startup
- [ ] Health endpoint
- [ ] Liveness endpoint
- [ ] Database readiness

Expected final result:

```text
==================================================
DEPLOYMENT VALIDATION SUCCESSFUL
==================================================

All deployment readiness checks passed.
```

## Important Note

The production safety validation intentionally tests invalid production configurations, including:

- demo environment restrictions;
- development seed restrictions; and
- weak JWT secret restrictions.

Validation errors generated during those intentional negative tests are expected when the script subsequently reports that the corresponding safety restriction has passed.

### Sign-Off

- [ ] Deployment validation completed successfully

Verified by: ________________________________

Date: ________________________________

---

# 7. Production Safety Verification

Before releasing the application to production, confirm the following controls.

## Environment Safety

- [ ] Production environment is explicitly configured.
- [ ] Development environment settings are not being used.
- [ ] Demo mode is disabled.
- [ ] Development seed data is disabled.

## Authentication and Security

- [ ] JWT secret meets production strength requirements.
- [ ] Production credentials are securely stored.
- [ ] No default development passwords are being used.
- [ ] Authentication is functioning correctly.
- [ ] Unauthorized access is rejected.

## Tenant Isolation

Andiny Atlas uses the **Organization** as the tenant boundary.

Confirm:

- [ ] Customer users cannot access another organization's data.
- [ ] Customer administrators remain restricted to their organization.
- [ ] Customer administrators cannot create platform Super Admins.
- [ ] Cross-tenant access is restricted according to platform governance rules.
- [ ] Organization lifecycle controls remain functional.

### Sign-Off

- [ ] Production safety controls verified
- [ ] Tenant isolation controls verified

Verified by: ________________________________

Date: ________________________________

---

# 8. Production Application Startup

Start the application using the approved production deployment method.

For local validation, the application can be started with:

```powershell
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

For the actual production environment, use the approved production process, service manager, container platform, or hosting configuration.

Confirm that startup completes successfully.

Expected startup indicators include:

```text
Application startup complete.
```

And the application running in:

```text
production mode
```

### Sign-Off

- [ ] Application started successfully
- [ ] Production environment confirmed

Verified by: ________________________________

Date: ________________________________

---

# 9. Health Endpoint Verification

After the production application starts, verify the health endpoints.

## Application Health

```powershell
Invoke-RestMethod http://<PRODUCTION_HOST>/health
```

Expected status:

```text
running
```

## Liveness

```powershell
Invoke-RestMethod http://<PRODUCTION_HOST>/health/live
```

Expected status:

```text
alive
```

## Readiness

```powershell
Invoke-RestMethod http://<PRODUCTION_HOST>/health/ready
```

Expected status:

```text
ready
```

The readiness response must confirm that the database is available.

Example:

```text
status      : ready
database    : available
service     : Andiny Atlas
environment : production
version     : <release-version>
```

### Sign-Off

- [ ] `/health` passed
- [ ] `/health/live` passed
- [ ] `/health/ready` passed
- [ ] Database availability confirmed

Verified by: ________________________________

Date: ________________________________

---

# 10. Production Database Verification

Confirm that the production database is available and accessible.

Verify:

- [ ] Database connection succeeds.
- [ ] Required data structures are available.
- [ ] Database readiness endpoint passes.
- [ ] Production data is not replaced by development seed data.
- [ ] Backup status has been confirmed.
- [ ] Recovery procedure is available.

Record database backup information:

| Item | Details |
|---|---|
| Backup Completed | Yes / No |
| Backup Date | ________________________________ |
| Backup Location | ________________________________ |
| Backup Verified | Yes / No |
| Recovery Owner | ________________________________ |

### Sign-Off

- [ ] Database verified
- [ ] Backup confirmed

Verified by: ________________________________

Date: ________________________________

---

# 11. Post-Deployment Functional Verification

After deployment, perform a controlled functional verification.

## Authentication

- [ ] Login succeeds with an authorized production account.
- [ ] Invalid credentials are rejected.
- [ ] Protected endpoints require authentication.

## Authorization

- [ ] Authorized users can access permitted resources.
- [ ] Unauthorized users are denied restricted operations.

## Organization and Tenant Boundaries

- [ ] Organization access behaves correctly.
- [ ] Branch access remains organization-scoped.
- [ ] Department access remains properly scoped.
- [ ] Customer users cannot access another organization's resources.

## Investigation Operations

- [ ] Cases can be retrieved.
- [ ] Authorized users can access investigation details.
- [ ] Case updates follow authorization rules.
- [ ] Immutable audit history remains available.

## Enterprise Operations

Where applicable, verify:

- [ ] Organization-level analytics
- [ ] Branch drill-down
- [ ] Department drill-down
- [ ] Department-to-case navigation
- [ ] Investigation detail access

### Sign-Off

- [ ] Post-deployment functional verification completed

Verified by: ________________________________

Date: ________________________________

---

# 12. Monitoring and Operational Verification

Immediately after deployment, verify operational visibility.

Confirm:

- [ ] Application logs are accessible.
- [ ] Startup errors are not present.
- [ ] Unexpected authentication failures are not occurring.
- [ ] Database errors are not occurring.
- [ ] Health checks remain successful.
- [ ] The application remains stable after startup.

Observation period:

```text
Start Time: __________________

End Time: __________________
```

### Sign-Off

- [ ] Operational monitoring completed successfully

Verified by: ________________________________

Date: ________________________________

---

# 13. Rollback Readiness

A production release must have a rollback path before deployment approval.

Confirm:

- [ ] Previous stable release has been identified.
- [ ] Previous release source or deployment artifact is available.
- [ ] Database backup has been confirmed.
- [ ] Rollback owner has been identified.
- [ ] Rollback procedure has been reviewed.

## Rollback Trigger Conditions

Rollback should be considered if:

- critical application startup failure occurs;
- health checks fail;
- database readiness fails;
- authentication is unavailable;
- tenant isolation is compromised;
- critical business operations fail; or
- production instability cannot be quickly resolved.

## Rollback Record

| Item | Details |
|---|---|
| Previous Stable Version | ________________________________ |
| Rollback Owner | ________________________________ |
| Rollback Procedure Location | ________________________________ |
| Database Recovery Required | Yes / No |

### Sign-Off

- [ ] Rollback readiness confirmed

Verified by: ________________________________

Date: ________________________________

---

# 14. Release Acceptance Decision

The release may be accepted only when all mandatory sections have passed.

## Mandatory Release Gates

| Release Gate | Status |
|---|---|
| Source Code Verification | PASS / FAIL |
| Dependency Verification | PASS / FAIL |
| Production Configuration | PASS / FAIL |
| Automated Tests | PASS / FAIL |
| Deployment Validation | PASS / FAIL |
| Production Safety | PASS / FAIL |
| Application Startup | PASS / FAIL |
| Health Checks | PASS / FAIL |
| Database Readiness | PASS / FAIL |
| Functional Verification | PASS / FAIL |
| Monitoring Verification | PASS / FAIL |
| Rollback Readiness | PASS / FAIL |

---

# 15. Final Production Release Sign-Off

## Deployment Engineer

I confirm that the deployment procedure was completed and that the recorded results are accurate.

**Name:**

```text
________________________________
```

**Signature:**

```text
________________________________
```

**Date:**

```text
________________________________
```

---

## Technical Reviewer

I confirm that the technical validation requirements have been reviewed and successfully completed.

**Name:**

```text
________________________________
```

**Signature:**

```text
________________________________
```

**Date:**

```text
________________________________
```

---

## Release Approver

I approve the release of Andiny Atlas to the production environment.

**Name:**

```text
________________________________
```

**Signature:**

```text
________________________________
```

**Date:**

```text
________________________________
```

---

# 16. Final Release Status

Select one:

- [ ] APPROVED FOR PRODUCTION
- [ ] APPROVED WITH CONDITIONS
- [ ] REJECTED — DO NOT DEPLOY
- [ ] ROLLED BACK

## Release Version

```text
________________________________
```

## Production Deployment Date

```text
________________________________
```

## Final Notes

```text
________________________________

________________________________

________________________________
```

---

# 17. Release Record Summary

After release completion, record the final deployment result.

| Item | Result |
|---|---|
| Application | Andiny Atlas |
| Version | ________________________________ |
| Environment | Production |
| Deployment Status | ________________________________ |
| Test Result | ________________________________ |
| Deployment Validation | ________________________________ |
| Health Status | ________________________________ |
| Database Status | ________________________________ |
| Rollback Required | Yes / No |
| Final Approval | ________________________________ |

---

# Deployment Completion Statement

A production deployment of Andiny Atlas is considered complete only when:

1. the approved source code has been deployed;
2. automated tests have passed;
3. production configuration has passed validation;
4. production safety restrictions have been verified;
5. the application has started successfully;
6. health, liveness, and readiness checks have passed;
7. database availability has been confirmed;
8. critical functional checks have passed;
9. rollback readiness has been confirmed; and
10. formal release sign-off has been completed.

The deployment must preserve the established Andiny Atlas architecture, including **Organization as the tenant boundary** and the platform's existing authorization, tenant isolation, and governance controls.