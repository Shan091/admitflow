# ADR-003: Multi-Tenancy Strategy

## Status
Accepted


## Context
AdmitFlow is a SaaS platform serving multiple educational institutions. We must ensure that one institution cannot access another's leads, courses, or chats.

## Decision
Use **Row-Level Isolation** with a shared PostgreSQL database. Every tenant-scoped table will have a `tenant_id` column, and all ORM queries must filter by this column.

## Alternatives Considered

### Schema-per-Tenant
- Pros: Stronger data isolation at the database level. Easier to backup/restore a single tenant.
- Cons: Running database migrations across hundreds of schemas is operationally complex and slow. 
- Rejected: Unnecessary overhead for an MVP.

### Database-per-Tenant
- Pros: Maximum isolation.
- Cons: Extremely expensive and difficult to provision/manage dynamically.
- Rejected: Not suitable for our scale and cost profile.

## Consequences
- Developers must be extremely disciplined to include `tenant_id` in every single database query and API endpoint constraint.
- The webhook ingress must reliably map Meta's `phone_number_id` to our internal `tenant_id` before enqueuing tasks.
