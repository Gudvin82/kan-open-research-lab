# Foundation Data Model

Foundation adds no publication or experiment tables. Django built-in
auth/admin/session tables are the only migrations.

## Operational value objects

| Object | Fields | Rules |
|---|---|---|
| DependencyStatus | `status`, `code?`, `checked_at` | stable public code, no exception text |
| ComputeNodeStatus | `status`, `code`, `checked_at` | always unavailable in Foundation |

No heartbeat or job is persisted. A later feature must define authorization,
retention and ownership before adding them.

## Database roles contract

| Environment | Role boundary |
|---|---|
| local | local database only |
| Preview | preview branch/database only |
| Production web | web CRUD, no role/admin |
| Research worker | future job/result subset only |
| Migration job | gated DDL only |

These are contracts only; Foundation provisions no production credentials.
