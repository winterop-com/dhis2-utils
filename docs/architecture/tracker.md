# Tracker plugin

`dhis2-core/plugins/tracker/` wraps the DHIS2 tracker API at `/api/tracker/*`. This covers the full case-management surface — tracked entities, enrollments, events (both event programs and tracker programs), relationships, and bulk import.

## Typed returns

Read services return typed pydantic models from `dhis2_client.generated.v42.tracker` (tracker shapes drift between DHIS2 majors, so models are version-scoped):

| Service | Returns |
|---|---|
| `list_tracked_entities` | `list[TrackerTrackedEntity]` |
| `get_tracked_entity` | `TrackerTrackedEntity` |
| `list_enrollments` | `list[TrackerEnrollment]` |
| `list_events` | `list[TrackerEvent]` |
| `list_relationships` | `list[TrackerRelationship]` |
| `push_tracker` | `WebMessageResponse` |

Status fields come back as `StrEnum` values (`EnrollmentStatus`, `EventStatus`) so agents/scripts can match them without stringly-typed drift. See [Typed schemas](typed-schemas.md) for the full model list and the TrackedEntityType metadata ↔ instance relationship.

## What it exposes

| Operation | CLI | MCP tool |
| --- | --- | --- |
| List TrackedEntityTypes | `dhis2 data tracker type` | `data_tracker_type_list` |
| List tracked entities | `dhis2 data tracker list <TET_NAME_OR_UID>` | `data_tracker_list` |
| Get one tracked entity | `dhis2 data tracker get <uid>` | `data_tracker_get` |
| List enrollments | `dhis2 data tracker enrollment list` | `data_tracker_enrollment_list` |
| List events | `dhis2 data tracker event list` | `data_tracker_event_list` |
| List relationships | `dhis2 data tracker relationship list` | `data_tracker_relationship_list` |
| Bulk import | `dhis2 data tracker push <file>` | `data_tracker_push` |

## Program types matter

DHIS2 has two program kinds:

- **`WITH_REGISTRATION`** (tracker programs) — support tracked entities, enrollments, events, relationships.
- **`WITHOUT_REGISTRATION`** (event programs) — only events; no tracked entities or enrollments.

Every tracker API call requires a program (or at least a tracked-entity-type), and that program must match the call's kind:

- `data_tracker_list` / `data_tracker_enrollment_list` require a tracker program (or skip them for event-only instances).
- `data_tracker_event_list` works for both kinds.
- `data_tracker_push` accepts any mix — each object in the bundle routes to the right service internally.

The plugin doesn't validate this client-side — DHIS2 returns a 400 "Program specified is not a tracker program" if you pass the wrong kind. The service surfaces that error directly; agents and CLI users see the DHIS2 message.

## `<type>` arg — TrackedEntityType by name or UID

`dhis2 data tracker list` takes the TrackedEntityType as a positional argument.
Pass a human name (case-insensitive; resolved server-side) or a UID directly:

```bash
dhis2 data tracker type                      # discover configured types first
dhis2 data tracker list Person               # by name
dhis2 data tracker list patient              # case-insensitive
dhis2 data tracker list tet01234567          # by UID
```

## CLI examples

```bash
# Find a tracker program first
dhis2 metadata list programs --fields id,name,programType --json \
  | jq '.[] | select(.programType=="WITH_REGISTRATION") | .id'

# List tracked entities of type "Person" under a program
dhis2 data tracker list Person \
  --program IpHINAT79UW \
  --org-unit ImspTQPwCqd \
  --ou-mode DESCENDANTS \
  --page-size 10

# Fetch one tracked entity by UID (type inferred from the entity)
dhis2 data tracker get te01234567

# List events (works with either program kind)
dhis2 data tracker event list \
  --program IpHINAT79UW \
  --org-unit ImspTQPwCqd \
  --status COMPLETED \
  --after 2024-01-01

# Bulk import from a JSON bundle
dhis2 data tracker push bundle.json --strategy CREATE_AND_UPDATE --dry-run
```

## MCP examples

```python
# Discover configured TrackedEntityTypes
await mcp.call_tool("data_tracker_type_list", {})

# List tracked entities of type "Person"
await mcp.call_tool("data_tracker_list", {
    "type": "Person",
    "program": "IpHINAT79UW",
    "org_unit": "ImspTQPwCqd",
    "ou_mode": "DESCENDANTS",
    "page_size": 10,
})

# List events with status filter
await mcp.call_tool("data_tracker_event_list", {
    "program": "IpHINAT79UW",
    "org_unit": "ImspTQPwCqd",
    "status": "COMPLETED",
    "occurred_after": "2024-01-01",
})

# Push a bundle (mix of entities, enrollments, events)
await mcp.call_tool("data_tracker_push", {
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

- Single-event GET (`/api/tracker/events/{uid}`) — covered by `data_tracker_event_list` + filter for now.
- Single-enrollment GET.
- Ownership transfer endpoints.

Add them to `service.py` when needed.
