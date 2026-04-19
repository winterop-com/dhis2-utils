# `dhis2-client` shape

The client library is deliberately small. The big ideas — auth, version dispatch, typed dispatch — are in separate modules; the client itself is a thin async httpx wrapper that glues them together.

## Surface

```python
from dhis2_client import Dhis2Client, BasicAuth

async with Dhis2Client(
    base_url="https://play.im.dhis2.org/stable-2-42-0",
    auth=BasicAuth("admin", "district"),
) as client:
    # Version is discovered from /api/system/info during __aenter__.
    assert client.version_key == "v42"
    assert client.raw_version.startswith("2.42.")

    # Typed access (requires codegen for this version)
    # me = await client.resources.me.get()          # <- once v42 codegen has run

    # Escape hatches — work without codegen, return dicts
    raw = await client.get_raw("/api/me")

    # Typed escape hatch — bring your own BaseModel
    me = await client.get("/api/me", model=MyMeModel)
```

## Construction options

```python
Dhis2Client(
    base_url="https://...",
    auth=AuthProvider,                       # Basic, PAT, OAuth2, or any Protocol impl
    timeout=30.0,                            # read/write/pool timeout
    connect_timeout=60.0,                    # connect timeout (cold-start friendly)
    allow_version_fallback=False,            # nearest-lower generated module if exact missing
)
```

## Lifecycle

Two usage patterns:

```python
# Async context manager — recommended
async with Dhis2Client(...) as client:
    ...

# Explicit connect/close
client = Dhis2Client(...)
await client.connect()
try:
    ...
finally:
    await client.close()
```

`connect()` does two things:

1. Builds the underlying `httpx.AsyncClient` (connection pool).
2. Calls `get_raw("/api/system/info")`, parses the version, loads the matching `dhis2_client.generated.v{NN}` module.

Both happen only once per client. Calling `connect()` repeatedly is safe (second call is a no-op for the HTTP pool, but refreshes the version info).

## Methods

```python
await client.get_raw(path, params=None) -> dict[str, Any]
await client.get(path, model=SomeModel, params=None) -> SomeModel
await client.post_raw(path, body=None) -> dict[str, Any]
await client.put_raw(path, body=None) -> dict[str, Any]
await client.delete_raw(path) -> dict[str, Any]
```

Typed `post` / `put` / `delete` variants will land when `query.py` grows a pydantic-aware request body helper. For now, raw methods are the baseline and typed `get[T]` covers the common case.

## Client-side UID generation

```python
from dhis2_client import generate_uid, generate_uids, is_valid_uid, UID_RE

generate_uid()            # "aB3dEf5gH7i" — 11 chars, first is letter
generate_uids(100)        # list[str] of 100 unique UIDs
is_valid_uid("DEancVis1") # False (too short)
UID_RE.pattern            # '^[A-Za-z][A-Za-z0-9]{10}$'
```

Mirrors `dhis-2/dhis-api/src/main/java/org/hisp/dhis/common/CodeGenerator.java` — same 62-char alphabet (digits + upper + lower), same 11-char length, same letter-first constraint. Uses `secrets.choice` so UIDs are CSPRNG-strong (the `SecureRandom` path upstream). Avoids a `/api/system/id` round-trip when minting IDs for `/api/metadata` bulk payloads.

## Errors

```
Dhis2ClientError                     # base
├── Dhis2ApiError                    # non-success HTTP response (≥400 except 401)
├── AuthenticationError              # 401 specifically
├── OAuth2FlowError                  # state mismatch, missing code, refresh failure
└── UnsupportedVersionError          # no generated module for reported DHIS2 version
```

`Dhis2ApiError` carries `status_code`, `message`, and `body` (parsed JSON if available, else text).

## Design choices

- **`httpx.AsyncClient` is held as an attribute, not constructed per call.** Connection pooling matters for MCP tools that an agent hits dozens of times per session.
- **Auth is resolved per request, not cached on the client.** Each request goes through `auth.headers()` which gives OAuth2 a chance to refresh before sending.
- **`get[T: BaseModel]` uses PEP 695 generic syntax.** Requires Python 3.13, which we require anyway. Gives strict pyright full type visibility — `await client.get("/api/me", model=Me)` returns `Me`, not `Any`.
- **No sync wrapper.** Notebook users call `asyncio.run(...)`. Adding a sync façade via `unasync` was considered; rejected because the duplicate surface would need duplicate testing and the real cost of `asyncio.run` is negligible.
- **JSON responses that return non-dict root (lists, primitives) are wrapped as `{"data": ...}`.** Keeps the return type stable; callers can branch if they need raw access via `get_raw`, but the typed path is dict-shaped.
- **No retries, no backoff, no circuit breakers — yet.** Those belong in a transport layer we'd wire via `httpx.AsyncHTTPTransport` when we know what the failure modes actually are in practice. Premature policy would encode the wrong defaults.

## Open questions

- Should `post`/`put` accept a pydantic model and auto-serialise? Probably yes, but the field alias story for DHIS2 camelCase matters. Waiting for codegen to pin the conventions first.
- Do we need a streaming variant (`stream(path) -> AsyncIterator[bytes]`) for large analytics downloads? Not yet — we'll add it when a plugin needs it.
- Should `UnsupportedVersionError` attempt to download the schemas and emit models on the fly as a last-resort "runtime codegen"? Tempting but rejected — runtime models don't satisfy strict pyright, defeating the point.
