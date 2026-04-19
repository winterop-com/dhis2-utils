# `dhis2-client`: step-by-step guide

End-to-end tutorial for the `dhis2-client` Python library. Every block is runnable; paste it into a file, set your env, and run.

If you already use the `dhis2` CLI or the MCP server, this library is what those layers sit on. Use it directly when you're writing Python scripts or your own tooling.

- Prerequisites
- Install
- Your first call
- Auth
- Typed resource CRUD
- Bulk operations
- Error handling
- Analytics queries
- Tracker reads
- Task polling
- UID generation
- Versions + fallback
- Concurrency
- Raw escape hatches

## Prerequisites

- Python 3.13+
- A reachable DHIS2 v42+ instance. Local: `make dhis2-run`; remote: your own install or `https://play.im.dhis2.org/stable-2-42`.
- Credentials; PAT, username+password, or OAuth2 client config.

## Install

The client is a workspace member. If you're inside this repo:

```bash
uv sync --all-packages        # installs every member
```

Standalone (outside the repo, once published):

```bash
uv add dhis2-client            # or: pip install dhis2-client
```

## Your first call

Simplest working script. `Dhis2Client` is an async context manager that handles the connection pool and the DHIS2-version handshake.

```python
# examples/client/01_whoami.py (roughly)
import asyncio
import os
from dhis2_client import BasicAuth, Dhis2Client

async def main() -> None:
    async with Dhis2Client(
        base_url=os.environ.get("DHIS2_URL", "http://localhost:8080"),
        auth=BasicAuth(username="admin", password="district"),
    ) as client:
        print(f"Connected to DHIS2 {client.raw_version}")
        me = await client.system.me()
        print(f"  logged in as: {me.username} ({me.displayName})")

asyncio.run(main())
```

What happens on `__aenter__`:
1. Opens an `httpx.AsyncClient` connection pool.
2. Calls `/api/system/info` to discover the DHIS2 version.
3. Binds the matching generated resource accessors (`client.resources.*`).

`client.version_key` is `"v42"` afterwards; `client.raw_version` is `"2.42.4"`.

## Auth

Every auth method implements the same `AuthProvider` Protocol. The rest of the client is identical regardless of what you pick.

### Basic auth

```python
from dhis2_client import BasicAuth, Dhis2Client

async with Dhis2Client(
    base_url="http://localhost:8080",
    auth=BasicAuth(username="admin", password="district"),
) as client:
    ...
```

`BasicAuth` sends `Authorization: Basic base64(user:pw)` on every request. Use against dev/play instances only; production should prefer PAT or OAuth2.

### PAT

```python
from dhis2_client import Dhis2Client, PatAuth

async with Dhis2Client(
    base_url="http://localhost:8080",
    auth=PatAuth(token=os.environ["DHIS2_PAT"]),
) as client:
    ...
```

PATs are user-scoped, long-lived, revocable. They travel as `Authorization: ApiToken <token>` (DHIS2-flavoured, not `Bearer`).

Mint a PAT:

- CLI: `dhis2 dev pat create --url <url> --admin-user admin --description "example"` (needs `DHIS2_ADMIN_PAT` or `DHIS2_ADMIN_PASSWORD` in env)
- Web UI: every user's profile page at `/dhis-web-user-profile`
- Per the seeded e2e fixture: `make dhis2-run` writes one to `infra/home/credentials/.env.auth`

### OAuth2 / OIDC

The most setup but the cleanest token hygiene; short-lived access tokens, auto-refresh, per-device authorisation.

```python
from dhis2_client import Dhis2Client
from dhis2_client.auth.oauth2 import OAuth2Auth, OAuth2Token

# Typical flow: the user runs `dhis2 profile login <name>` once, which walks the
# browser flow and persists an access+refresh token in `.dhis2/tokens.sqlite`.
# From Python you load that persisted token:
from dhis2_core.token_store import token_store_for_scope

store = token_store_for_scope("global")
token = await store.get("my-oauth-profile")

auth = OAuth2Auth(
    token=token,
    token_store=store,
    token_key="my-oauth-profile",
    token_url="http://localhost:8080/oauth2/token",
    client_id=os.environ["DHIS2_OAUTH_CLIENT_ID"],
    client_secret=os.environ["DHIS2_OAUTH_CLIENT_SECRET"],
)

async with Dhis2Client(base_url="http://localhost:8080", auth=auth) as client:
    ...
```

The access token auto-refreshes in `headers()` when it's within 30 s of expiry; the refreshed token is written back to the store. See [Pluggable auth](../architecture/auth.md) for the internals and [Connecting to DHIS2](connecting-to-dhis2.md) for the end-to-end OAuth2 setup (registering a client, first-time login).

For a complete standalone OAuth2 demo including PKCE, FastAPI redirect receiver, and SQLite token store, see `examples/client/04_oidc_login.py`.

### Route API auth

The DHIS2 Route API proxies requests to upstream services. Its own auth is one of five discriminated variants (`http-basic`, `api-token`, `api-headers`, `api-query-params`, `oauth2-client-credentials`). The typed union lives in `dhis2_client.AuthScheme`:

```python
from dhis2_client import AuthSchemeAdapter, HttpBasicAuthScheme, OAuth2ClientCredentialsAuthScheme

scheme = HttpBasicAuthScheme(type="http-basic", username="svc", password="secret")
# Or parse from a raw Route response:
parsed = AuthSchemeAdapter.validate_python({"type": "api-token", "token": "..."})
```

## Typed resource CRUD

After `__aenter__`, `client.resources` exposes a typed accessor for every metadata resource DHIS2 publishes at `/api/<plural>`. Attribute names are snake-cased plurals: `data_elements`, `organisation_units`, `category_combos`, etc.

```python
from dhis2_client import Dhis2Client, BasicAuth, generate_uid
from dhis2_client.generated.v42.common import Reference
from dhis2_client.generated.v42.enums import AggregationType, DataElementDomain, ValueType
from dhis2_client.generated.v42.schemas.data_element import DataElement

async with Dhis2Client("http://localhost:8080", auth=BasicAuth("admin", "district")) as client:
    uid = generate_uid()  # 11-char, client-side, matches dhis2-core/CodeGenerator.java

    # CREATE
    new_de = DataElement(
        id=uid,
        code=f"EX_DE_{uid}",
        name=f"Example DE {uid}",
        shortName=f"Ex {uid[:4]}",
        domainType=DataElementDomain.AGGREGATE,
        valueType=ValueType.NUMBER,
        aggregationType=AggregationType.SUM,
        categoryCombo=Reference(id="bjDvmb4bfuf"),  # default CC from the seed
    )
    await client.resources.data_elements.create(new_de)

    # READ
    fetched = await client.resources.data_elements.get(uid, fields="id,name,valueType")
    print(f"fetched: {fetched.name} ({fetched.valueType})")

    # UPDATE; PUT the whole model back
    fetched.name = "Renamed"
    await client.resources.data_elements.update(fetched)

    # DELETE
    await client.resources.data_elements.delete(uid)
```

Enum fields are `StrEnum`s; `DataElementDomain.AGGREGATE == "AGGREGATE"` is true, so you can pass bare strings too. `Reference` has both `id` and `code` fields; pick whichever your calling import strategy uses.

### Filters, order, paging

```python
# Single filter
recent = await client.resources.data_elements.list(
    filters=["name:like:ANC"],
    fields="id,name",
)

# Multi-filter OR
matches = await client.resources.data_elements.list(
    filters=["name:like:ANC", "code:eq:DEancVisit1"],
    root_junction="OR",
)

# Server-side paging + ordering
page = await client.resources.organisation_units.list(
    order=["level:asc", "name:asc"],
    page_size=20,
    page=2,
)

# Dump everything in one request (paging=False)
everything = await client.resources.indicators.list(paging=False, fields=":identifiable")

# Or walk pages to get the `pager` block
envelope = await client.resources.data_elements.list_raw(page_size=50, page=1)
pager = envelope.get("pager", {})  # {"page", "pageSize", "total", "pageCount"}
```

Filter syntax is DHIS2's native `property:operator:value` form. Operators: `eq`, `ieq`, `ne`, `like`, `!like`, `ilike`, `in`, `!in`, `null`, `!null`, `gt`, `ge`, `lt`, `le`, `token`. Use Python f-strings for interpolation; `f"valueType:eq:{ValueType.NUMBER}"`.

## Bulk operations

Every write endpoint returns a `WebMessageResponse` envelope. It's the same shape across DHIS2 so we model it once and reuse.

```python
from dhis2_client import Dhis2Client, BasicAuth, DataValue, DataValueSet, WebMessageResponse

async with Dhis2Client("http://localhost:8080", auth=BasicAuth("admin", "district")) as client:
    payload = DataValueSet(
        dataValues=[
            DataValue(
                dataElement="DEancVisit1",
                period="202603",
                orgUnit="NOROsloProv",
                value="42",
            ),
        ],
    )
    raw = await client.post_raw("/api/dataValueSets", payload.model_dump(exclude_none=True))
    response = WebMessageResponse.model_validate(raw)

    print(f"status={response.status}")
    counts = response.import_count()
    if counts is not None:
        print(
            f"  imported={counts.imported} updated={counts.updated} "
            f"ignored={counts.ignored} deleted={counts.deleted}"
        )
    for conflict in response.conflicts():
        print(f"  conflict: {conflict.property} = {conflict.value} [{conflict.errorCode}]")
```

Helpers on `WebMessageResponse`:

- `.status`, `.httpStatus`, `.httpStatusCode`, `.message`; the envelope scalar fields
- `.created_uid`; the UID from an object-report envelope (handles DHIS2's `response.uid` vs `id` inconsistency, see BUGS.md #4f)
- `.import_count()` → typed `ImportCount` (flat OR nested `response.importCount` forms)
- `.conflicts()` → `list[Conflict]`; per-row rejections with `property`, `value`, `errorCode`
- `.rejected_indexes()` → `list[int]`; payload-array indexes DHIS2 refused
- `.import_report()` → typed `ImportReport` for `/api/metadata` bulk responses
- `.task_ref()` → `(job_type, task_uid)` tuple when DHIS2 returned a job-kickoff envelope

## Error handling

DHIS2 returns 4xx with a JSON body describing what went wrong. The client always raises for ≥400; and always captures the body, even when it's a WebMessageResponse.

```python
from dhis2_client import AuthenticationError, Dhis2ApiError, Dhis2Client, PatAuth

async with Dhis2Client("http://localhost:8080", auth=PatAuth(token="not-a-real-pat")) as client:
    try:
        await client.system.me()
    except AuthenticationError as exc:
        print(f"401: {exc}")
    except Dhis2ApiError as exc:
        # Any non-401 4xx/5xx
        print(f"{exc.status_code}: {exc.message}")
        envelope = exc.web_message  # typed WebMessageResponse, or None
        if envelope is not None:
            for conflict in envelope.conflicts():
                print(f"  {conflict.property}: {conflict.value}")
```

Exception hierarchy:

- `Dhis2ClientError`; base
- `Dhis2ApiError`; any non-success response, `.body` carries the parsed JSON / text, `.web_message` lazily parses it as `WebMessageResponse`
- `AuthenticationError`; 401 specifically
- `OAuth2FlowError`; state mismatch, missing code, refresh failure
- `UnsupportedVersionError`; no generated client for the DHIS2 version the server reports

## Analytics queries

The `/api/analytics` endpoint has three response shapes. Pass `table` (default), `raw`, or `dvs` (DataValueSet).

```python
from dhis2_client import AnalyticsResponse, DataValueSet

# Aggregated query: AnalyticsResponse with headers + rows + metaData
raw = await client.get_raw(
    "/api/analytics",
    params={
        "dimension": ["dx:DEancVisit1", "pe:LAST_12_MONTHS", "ou:NORNorway01"],
        "skipMeta": "true",
    },
)
response = AnalyticsResponse.model_validate(raw)
for row in response.rows:
    print(row)

# dataValueSet shape: round-trippable into /api/dataValueSets
raw = await client.get_raw(
    "/api/analytics/dataValueSet.json",  # .json required, see BUGS.md #1
    params={"dimension": ["dx:DEancVisit1", "pe:LAST_3_MONTHS", "ou:NORNorway01"]},
)
dvs = DataValueSet.model_validate(raw)
for dv in dvs.dataValues:
    print(f"{dv.dataElement} {dv.period} {dv.orgUnit} = {dv.value}")
```

## Tracker reads

Reads return typed instance models from `dhis2_client.generated.v42.tracker` (version-scoped — tracker shapes drift across DHIS2 majors). Writes go through the typed `TrackerBundle` from the same module.

```python
from dhis2_client.generated.v42.tracker import TrackerEnrollment, TrackerEvent, TrackerTrackedEntity

raw = await client.get_raw(
    "/api/tracker/trackedEntities",
    params={"program": "<PROG_UID>", "pageSize": 10},
)
for entity in raw.get("instances", []):
    te = TrackerTrackedEntity.model_validate(entity)
    print(f"{te.trackedEntity}  type={te.trackedEntityType}  orgUnit={te.orgUnit}")
```

`EventStatus` and `EnrollmentStatus` are `StrEnum`s; `EventStatus.COMPLETED == "COMPLETED"`.

## Task polling

Every async DHIS2 op (analytics refresh, metadata import, data-integrity run, tracker async push) returns a `JobConfigurationWebMessageResponse`. Use `.task_ref()` to pull the polling tuple, then hit `/api/system/tasks/{type}/{uid}` until `completed=true`.

```python
import asyncio
from dhis2_client import WebMessageResponse

raw = await client.post_raw("/api/resourceTables/analytics", params={"lastYears": 1})
envelope = WebMessageResponse.model_validate(raw)
ref = envelope.task_ref()
if ref is None:
    raise RuntimeError("response had no jobType/id; nothing to watch")
job_type, task_uid = ref

while True:
    feed = await client.get_raw(f"/api/system/tasks/{job_type}/{task_uid}")
    notifications = feed.get("data", [])
    for notification in reversed(notifications):  # DHIS2 returns newest-first
        print(f"  {notification.get('level')} {notification.get('message')}")
        if notification.get("completed"):
            return
    await asyncio.sleep(1)
```

A fuller version with de-duplication and Rich progress lives in `dhis2_core.cli_task_watch.stream_task_to_stdout`; usable from your own code too. See `examples/client/16_task_polling.py`.

## UID generation

DHIS2 UIDs are 11-char strings matching `^[A-Za-z][A-Za-z0-9]{10}$`. Instead of `/api/system/id` round-trips, generate them client-side; same algorithm as `dhis2-core/CodeGenerator.java`:

```python
from dhis2_client import generate_uid, generate_uids, is_valid_uid, UID_RE

generate_uid()              # "aB3dEf5gH7i"
generate_uids(100)          # list of 100 unique UIDs
is_valid_uid("DEancVisit1") # True
UID_RE.pattern              # '^[A-Za-z][A-Za-z0-9]{10}$'
```

Uses `secrets.choice` (CSPRNG), matches the `SecureRandom` path upstream.

## Versions + fallback

On connect, the client pulls `/api/system/info`, extracts the minor version, and binds the matching generated module. Versions shipped: v40, v41, v42, v44. If the reported version has no generated module, construction fails with `UnsupportedVersionError` unless you opt into fallback:

```python
async with Dhis2Client(
    base_url="https://example/dhis2",
    auth=BasicAuth("admin", "district"),
    allow_version_fallback=True,  # pick the highest generated version <= reported
) as client:
    ...
```

You can also pin a version explicitly if you want to target a specific module regardless of what the server reports:

```python
from dhis2_client import Dhis2

async with Dhis2Client(
    base_url="https://example/dhis2",
    auth=BasicAuth("admin", "district"),
    version=Dhis2.V42,
) as client:
    ...
```

Regenerate codegen for a new version with `dhis2 dev codegen rebuild` or point at a live instance with `dhis2 dev codegen generate --url <url>`.

## Concurrency

The client's `httpx.AsyncClient` is shared across concurrent calls on the same `Dhis2Client` instance; safe to use with `asyncio.gather`.

```python
import asyncio

async with Dhis2Client(...) as client:
    # Parallel GETs
    uids = ["DEancVisit1", "DEancVisit4", "DEdelFacilt"]
    elements = await asyncio.gather(
        *(client.resources.data_elements.get(uid) for uid in uids),
    )

    # Parallel writes; DHIS2 is generally fine with moderate concurrency
    # on independent records. Tune to your instance's capacity.
    await asyncio.gather(*(client.resources.data_elements.update(de) for de in updated))
```

Connection pool defaults are httpx's defaults (100 max connections, 20 keepalive). Override by passing a pre-built `httpx.AsyncClient` via future config if you hit limits.

## Raw escape hatches

Every endpoint ever built at DHIS2 is reachable through four raw methods. Prefer the typed accessors when they exist; but these never lose.

```python
raw = await client.get_raw("/api/some/unusual/path", params={"key": "val"})
raw = await client.post_raw("/api/metadata", {"dataElements": [...]})
raw = await client.put_raw("/api/dataElements/abc", {"name": "..."})
raw = await client.delete_raw("/api/dataElements/abc")
raw = await client.patch_raw("/api/dataElements/abc", [{"op": "replace", "path": "/name", "value": "..."}])

# Typed GET against your own model:
from pydantic import BaseModel

class MyModel(BaseModel):
    id: str
    name: str

item = await client.get("/api/something", model=MyModel)
```

`get_raw` always returns `dict[str, Any]`. When DHIS2 returns a bare JSON array (e.g. `/api/system/id`), it's wrapped under `{"data": [...]}` so the return type stays consistent.

---

## Where next?

- [Connecting to DHIS2](connecting-to-dhis2.md); end-to-end setup for PAT / OAuth2 including registering an OAuth2 client
- [Architecture: Pluggable auth](../architecture/auth.md); how `AuthProvider` works under the hood
- [Architecture: Typed schemas](../architecture/typed-schemas.md); full model + enum inventory
- [Architecture: Metadata CRUD](../architecture/metadata-crud.md); deeper dive on the generated resource accessors
- `examples/client/`; 17 runnable examples covering every pattern in this guide
