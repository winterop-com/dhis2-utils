# Typed schemas

`dhis2-client` exports three families of pydantic models that give callers a typed surface over the DHIS2 JSON API. All three are derived from DHIS2's OpenAPI spec (`/api/openapi.json`) with a per-version copy committed under `packages/dhis2-client/src/dhis2_client/generated/v{N}/openapi.json`.

## 1. WebMessageResponse — write-envelope model

Every POST / PUT / PATCH / DELETE through `/api/*` returns one of DHIS2's WebMessage envelopes. `WebMessageResponse` models the common shape, leaving the inner `response` field loose (its subtype varies by endpoint) but giving callers typed methods to narrow it.

```python
from dhis2_client import WebMessageResponse
response = await route_service.add_route(profile, payload)

response.httpStatus           # "Created"
response.httpStatusCode       # 201
response.status               # "OK"

response.created_uid          # "abc123uid12" — pulls response.uid, closes BUGS.md #4f
report = response.object_report()          # typed ObjectReport when the inner is a create/update
counts = response.import_count()           # typed ImportCount for /api/dataValueSets imports
full_report = response.import_report()     # typed ImportReport for /api/metadata bulk imports
```

Available subtypes: `ObjectReport`, `ImportCount`, `ImportReport`, `ErrorReport`, `Stats`, `TypeReport` — all exported from `dhis2_client`.

Every plugin's write service returns `WebMessageResponse`:

| Plugin | Methods |
|---|---|
| route | `add_route`, `update_route`, `patch_route`, `delete_route` |
| aggregate | `push_data_values`, `set_data_value`, `delete_data_value` |
| tracker | `push_tracker` |
| analytics | `refresh_analytics` |

## 2. AuthScheme — discriminated union for Route auth

Route auth blocks (see [Route API guide](../guides/connecting-to-dhis2.md)) are polymorphic — the `type` field discriminates between five variants. The union is typed end-to-end.

```python
from dhis2_client import (
    AuthScheme,
    AuthSchemeAdapter,
    HttpBasicAuthScheme,
    ApiTokenAuthScheme,
    ApiHeadersAuthScheme,
    ApiQueryParamsAuthScheme,
    OAuth2ClientCredentialsAuthScheme,
    auth_scheme_from_route,
)

# Validate a dict into the right subclass:
scheme = AuthSchemeAdapter.validate_python({"type": "http-basic", "username": "u", "password": "p"})
assert isinstance(scheme, HttpBasicAuthScheme)

# Parse an existing Route's auth field:
route = await client.resources.routes.get("abc123uid12")
scheme = auth_scheme_from_route(route)
match scheme:
    case HttpBasicAuthScheme(username=u):      ...
    case ApiTokenAuthScheme(token=t):          ...
    case OAuth2ClientCredentialsAuthScheme():  ...
```

| `type` value | Class | Use for |
|---|---|---|
| `http-basic` | `HttpBasicAuthScheme` | `Authorization: Basic base64(u:p)` |
| `api-token` | `ApiTokenAuthScheme` | DHIS2-flavour static token — `Authorization: ApiToken <v>` (NOT standard `Bearer`, see BUGS.md #4e) |
| `api-headers` | `ApiHeadersAuthScheme` | Arbitrary custom headers map |
| `api-query-params` | `ApiQueryParamsAuthScheme` | Query-string param map |
| `oauth2-client-credentials` | `OAuth2ClientCredentialsAuthScheme` | Upstream OAuth2 client-credentials flow |

The generated `Route.auth` stays typed as `Any | None` because DHIS2's `/api/schemas` endpoint can't express polymorphic unions — the helper `auth_scheme_from_route(route)` narrows it.

## 3. Tracker instance models

`/api/tracker/*` returns runtime instance data (enrollments, events, etc.), not metadata definitions — these shapes are in OpenAPI only. Hand-written pydantic models in `dhis2_client/tracker.py` cover the common paths:

| Class | Endpoint | Key fields |
|---|---|---|
| `TrackerTrackedEntity` | `/api/tracker/trackedEntities` | `trackedEntity`, `trackedEntityType`, `orgUnit`, `attributes`, `enrollments` |
| `TrackerEnrollment` | `/api/tracker/enrollments` | `enrollment`, `trackedEntity`, `program`, `status`, `events`, `attributes` |
| `TrackerEvent` | `/api/tracker/events` | `event`, `enrollment`, `program`, `programStage`, `orgUnit`, `status`, `dataValues` |
| `TrackerRelationship` | `/api/tracker/relationships` | `relationship`, `relationshipType`, `from_`, `to` |

Nested value types — `TrackerAttributeValue`, `TrackerDataValue`, `TrackerNote`, `TrackerRelationshipItem` — live in the same module.

Status enums use `StrEnum` so they round-trip through JSON cleanly:

```python
from dhis2_client import EnrollmentStatus, EventStatus

EnrollmentStatus.ACTIVE      # "ACTIVE"  -> "ACTIVE" in JSON
EventStatus("SCHEDULE")      # parses from DHIS2's wire value
```

### TrackedEntityType — metadata vs instance

A `TrackerTrackedEntity` carries `trackedEntityType: str | None` as a UID reference. The full TrackedEntityType metadata (name, description, per-type attributes like "Person" vs "Patient" vs "Lab Sample") is a metadata resource and lives under the generated `/api/schemas` codegen:

```python
entity = await client.resources.tracked_entity_types.get("tet01234567")
entity.name          # "Person", "Patient", ...
```

Join via `TrackerTrackedEntity.trackedEntityType` (UID) → `client.resources.tracked_entity_types.get(uid)`.

## Why all three shapes?

- **WebMessageResponse** — universal envelope, worth modelling once and reusing everywhere.
- **AuthScheme union** — OpenAPI's discriminator is the only place this polymorphism is described. `/api/schemas` can't express it, so we carry a hand-written union.
- **Tracker instance models** — the `/api/tracker/*` endpoints aren't metadata; they need their own models regardless of source.

Writing these as deliberate pydantic files (rather than a full OpenAPI-driven generator) keeps the surface small, reviewable, and auditable. An automated generator may land later once we have enough targets to justify the infrastructure.
