# Andiny Atlas — Enterprise Architecture Rules

**Status:** LOCKED  
**Purpose:** Authoritative architectural reference for enterprise/customer deployment  
**Repository:** Andiny Atlas

---

## 1. Baseline

The current backend baseline is:

- 85 tests passing
- Existing functionality must remain protected
- New capabilities must have tests
- Existing roadmap must not be changed without an explicit architectural decision

The 85-test baseline is the known-good foundation.

---

# 2. Tenant / Customer Boundary

An `Organization` is the Andiny Atlas tenant/customer boundary.

The enterprise hierarchy is:

Organization
→ Branch
→ Department
→ Cases / Investigations

Customer-scoped capabilities include:

- Users
- Investigations
- Case history
- Reports
- Analytics
- Exports
- Configuration

Platform governance remains outside the customer tenant.

---

# 3. Authorization Model

Authorization consists of:

1. Authentication
2. User identity
3. Role
4. Organization scope
5. Resource ownership
6. Authorization decision

Conceptually:

JWT
→ Current User
→ Role
→ Organization Scope
→ Resource Ownership
→ Authorization Decision
→ Repository Query

---

# 4. Role Hierarchy

The application roles are:

- Agent
- Supervisor
- Admin
- Super Admin

Hierarchy:

Agent
→ Supervisor
→ Admin
→ Super Admin

Roles determine capability.

Organization scope determines accessible data.

---

# 5. Tenant-Scoped Roles

The following roles are tenant-bound:

- Agent
- Supervisor
- Admin

They may only operate within their own organization.

A customer Admin cannot:

- Access another organization
- Create users in another organization
- Create Super Admins
- Perform platform governance
- Change another tenant's configuration

---

# 6. Super Admin

Super Admin is the platform-level role.

Super Admin may:

- Provision organizations
- Provision initial customer administrators
- Perform platform governance
- Access cross-tenant administrative information where explicitly required

Super Admin is not treated as belonging to an arbitrary customer organization.

---

# 7. User Organization

Every enterprise customer user must belong to an organization.

Conceptually:

User
- id
- organization_id
- role
- ...

Super Admin is the platform-scope exception.

---

# 8. Organization Isolation

Organization is the mandatory server-side security boundary.

A customer request must never establish its authorization scope from a client-supplied `organization_id`.

The authenticated user's organization must determine tenant scope.

Client-supplied organization identifiers must not override authenticated scope.

---

# 9. Cross-Tenant Access

A user belonging to Organization A must not access:

- Organization B users
- Organization B branches
- Organization B departments
- Organization B investigations
- Organization B case history
- Organization B reports
- Organization B analytics
- Organization B exports

Cross-tenant access must be rejected server-side.

Where appropriate, inaccessible resources should not reveal whether another tenant's resource exists.

---

# 10. Branch and Department Integrity

A branch must belong to its organization.

A department must belong to:

- The specified organization
- The specified branch

The following relationship must always hold:

department.organization_id
==
branch.organization_id

Hierarchy integrity must be enforced server-side.

---

# 11. Reports and Analytics

Reports, analytics and exports must inherit organization scope.

Customer users must not obtain global results by manipulating:

- organization_id
- branch_id
- department_id
- date ranges
- filters

Tenant scope comes from authenticated identity.

---

# 12. User Administration

Customer Admins may administer users within their own organization.

Customer Admins may not:

- Create Super Admins
- Create users in another organization
- Move users between tenants

Tenant reassignment is a platform governance operation.

---

# 13. User Deactivation

A deactivated user must immediately lose operational access.

Existing authentication behaviour checks user activity status and must remain protected.

---

# 14. Customer Onboarding

Customer onboarding follows:

Super Admin
→ Organization
→ Initial Customer Admin
→ Branches
→ Departments
→ Customer Users
→ Operations

The initial customer administrator is provisioned by the platform.

Customer Admin subsequently manages permitted users and organizational configuration.

---

# 15. Organization Lifecycle

An organization may be:

- Active
- Inactive / Deactivated

Deactivation is a business/security state.

Deactivation must not automatically destroy customer data.

Investigations and audit history must be retained according to the platform's retention policy.

Inactive organizations must not permit customer operational access.

---

# 16. Deployment Model

Andiny Atlas must support:

### Dedicated deployment

A customer may have an isolated Atlas deployment.

### Shared platform

Multiple customer organizations may operate within one Atlas deployment.

Tenant isolation must remain enforced in either model.

Infrastructure architecture must not weaken the organization security boundary.

---

# 17. Deployment Configuration

Deployment configuration includes:

### Application

- Environment
- Application name
- Application version

### Database

- Database connection
- Database credentials

### Authentication

- Secret configuration
- JWT configuration
- Token expiration

### Email

- Email provider
- Sender configuration
- Notification configuration

### Storage

- Export storage
- Document/attachment storage
- Retention configuration

### Observability

- Application logging
- Error monitoring
- Audit logging

### Integrations

Customer-specific integrations must use defined configuration/integration boundaries.

---

# 18. Secrets

Secrets must never be committed to Git.

Examples:

- Database passwords
- JWT secrets
- API keys
- SMTP passwords
- Encryption keys

The repository may contain:

`.env.example`

but must not contain actual production secrets.

Secrets must be supplied through deployment configuration or a secrets-management mechanism.

---

# 19. Customer-Specific Behaviour

Customer-specific behaviour must not be hard-coded.

Avoid patterns such as:

```python
if organization == "Customer X":
    ...