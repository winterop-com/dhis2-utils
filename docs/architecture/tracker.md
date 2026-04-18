# Tracker plugin

`dhis2-core/plugins/tracker/` wraps the DHIS2 tracker API at `/api/tracker/*`. This covers the full case-management surface — tracked entities, enrollments, events (both event programs and tracker programs), relationships, and bulk import.

## What it exposes

| Operation | CLI | MCP tool |
| --- | --- | --- |
| List tracked entities | `dhis2 tracker list-tracked-entities` | `list_tracked_entities` |
| Get one tracked entity | `dhis2 tracker get-tracked-entity <uid>` | `get_tracked_entity` |
| List enrollments | `dhis2 tracker list-enrollments` | `list_enrollments` |
| List events | `dhis2 tracker list-events` | `list_events` |
| List relationships | `dhis2 tracker list-relationships` | `list_relationships` |
| Bulk import | `dhis2 tracker push <file>` | `push_tracker` |

## Program types matter

DHIS2 has two program kinds:

- **`WITH_REGISTRATION`** (tracker programs) — support tracked entities, enrollments, events, relationships.
- **`WITHOUT_REGISTRATION`** (event programs) — only events; no tracked entities or enrollments.

Every tracker API call requires a program (or at least a tracked-entity-type), and that program must match the call's kind:

- `list_tracked_entities` / `list_enrollments` require a tracker program (or skip them for event-only instances).
- `list_events` works for both kinds.
- `push_tracker` accepts any mix — each object in the bundle routes to the right service internally.

The plugin doesn't validate this client-side — DHIS2 returns a 400 "Program specified is not a tracker program" if you pass the wrong kind. The service surfaces that error directly; agents and CLI users see the DHIS2 message.

## CLI examples

```bash
# Find a tracker program first
dhis2 metadata list programs --fields id,name,programType --json \
  | jq '.[] | select(.programType=="WITH_REGISTRATION") | .id'

# List tracked entities under a program
dhis2 tracker list-tracked-entities \
  --program IpHINAT79UW \
  --org-unit ImspTQPwCqd \
  --ou-mode DESCENDANTS \
  --page-size 10

# List events (works with either program kind)
dhis2 tracker list-events \
  --program IpHINAT79UW \
  --org-unit ImspTQPwCqd \
  --status COMPLETED \
  --after 2024-01-01

# Bulk import from a JSON bundle
dhis2 tracker push bundle.json --strategy CREATE_AND_UPDATE --dry-run
```

## MCP examples

```python
# List tracked entities
await mcp.call_tool("list_tracked_entities", {
    "program": "IpHINAT79UW",
    "org_unit": "ImspTQPwCqd",
    "ou_mode": "DESCENDANTS",
    "page_size": 10,
})

# List events with status filter
await mcp.call_tool("list_events", {
    "program": "IpHINAT79UW",
    "org_unit": "ImspTQPwCqd",
    "status": "COMPLETED",
    "occurred_after": "2024-01-01",
})

# Push a bundle (mix of entities, enrollments, events)
await mcp.call_tool("push_tracker", {
    "bundle": {
        "trackedEntities": [{"trackedEntity": "abc", "trackedEntityType": "X", "orgUnit": "Y"}],
        "enrollments": [{"enrollment": "def", "program": "Z", "orgUnit": "Y", "trackedEntity": "abc", ...}],
        "events": [{"event": "ghi", "program": "Z", "programStage": "S", "orgUnit": "Y", ...}],
    },
    "import_strategy": "CREATE_AND_UPDATE",
    "dry_run": True,
})
```

## Filter parameter reference

**`ou_mode`** values:
- `SELECTED` — only this org unit
- `CHILDREN` — immediate children
- `DESCENDANTS` — all descendants (default for most queries)
- `ACCESSIBLE` — user's accessible unit
- `CAPTURE` — user's capture unit
- `ALL` — superuser only

**`status`** values vary by object:
- Enrollments: `ACTIVE`, `COMPLETED`, `CANCELLED`
- Events: `ACTIVE`, `COMPLETED`, `VISITED`, `SCHEDULE`, `OVERDUE`, `SKIPPED`

**`import_strategy`** values: `CREATE`, `UPDATE`, `CREATE_AND_UPDATE` (default), `DELETE`.

**`atomic_mode`** values:
- `ALL` — fail the whole bundle on any object error (default, safer)
- `OBJECT` — import whatever validates, skip invalid ones

## Bundle shape for `push`

```json
{
  "trackedEntities": [ { "trackedEntity": "...", "trackedEntityType": "...", "orgUnit": "...", "attributes": [...], "enrollments": [...] } ],
  "enrollments":    [ { "enrollment": "...", "program": "...", "orgUnit": "...", "trackedEntity": "...", "events": [...] } ],
  "events":         [ { "event": "...", "program": "...", "programStage": "...", "orgUnit": "...", "dataValues": [...] } ],
  "relationships":  [ { "relationship": "...", "relationshipType": "...", "from": {...}, "to": {...} } ]
}
```

Any key can be omitted. Nested enrollments/events inside a tracked entity are allowed — the tracker import pipeline unwraps them.

## Async import

For bundles larger than ~10k objects, use `async_mode=True`. The server returns a job reference immediately; poll `/api/system/tasks/TRACKER_IMPORT_JOB/{taskId}` for progress. A future helper will wrap the poll loop.

## Not yet exposed

- Single-event GET (`/api/tracker/events/{uid}`) — covered by `list_events` + filter for now.
- Single-enrollment GET.
- Ownership transfer endpoints.

Add them to `service.py` when needed.
