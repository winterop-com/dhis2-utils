# Lessons learned

Accumulating knowledge about DHIS2's API quirks as we build against it. Keep this file short — one section per discovery with just enough context to not repeat the learning.

## DHIS2 Personal Access Token API

- **Endpoint:** `POST /api/apiToken` (as of v2.42).
- **Required payload:** `{"attributes": [], "type": "PERSONAL_ACCESS_TOKEN_V2"}`.
- The **old `PERSONAL_ACCESS_TOKEN`** type string returns a 500 with a Jackson deserialisation error. Valid enum values are `PERSONAL_ACCESS_TOKEN_V1` and `PERSONAL_ACCESS_TOKEN_V2`; use **V2**.
- **Response:** `{"response": {"key": "d2p_..."}}` — the token value is in `response.key`.
- **Token prefix:** `d2p_` (not `d2pat_` as you might guess from some DHIS2 docs).
- **Auth header:** `Authorization: ApiToken d2p_...`.

## DHIS2 login flow (web UI)

- **Login page:** `{base_url}/dhis-web-login/`.
- **Form fields:** `input[name="username"]`, `input[name="password"]`.
- **Submit:** `button[type="submit"]`.
- **Post-login redirect:** away from `/dhis-web-login` — DHIS2 sends you to the dashboard app by default. Waiting on the URL to no longer contain `/dhis-web-login` is a reliable signal.

## `/api/schemas` response shape

- `schema.name` is **not unique** across the response. Six schemas (JobConfiguration, Route, ValidationNotificationTemplate, EventHook, DatastoreEntry, FileResource on v2.44) share `name="identifiableObject"`. The `legend` name is also shared (Legend + LegendDefinitions).
- `schema.klass` is the fully-qualified Java class — always unique. The last dot-segment is what we use to derive Python class names in codegen.
- Useful field selector: `fields=name,plural,singular,displayName,apiEndpoint,metadata,klass,properties[name,fieldName,propertyType,klass,collection,simple,constants]`. This gets everything codegen needs in one round trip.

## Version strings

- **Play dev:** reports `"2.44-SNAPSHOT"` — cutting-edge, not always stable.
- **Stable releases:** `"2.42.4"`, `"2.41.3"`, etc.
- Our version key is `v{minor}` — `"v44"` for `"2.44-SNAPSHOT"`, `"v42"` for `"2.42.4"`. Patch and `-SNAPSHOT` are stripped.
- Codegen must tolerate suffixes like `-SNAPSHOT` when parsing `systemInfo.version`.

## DHIS2 analytics

- `lastAnalyticsTableSuccess` in `/api/system/info` tells you when the analytics tables were last rebuilt. A fresh play/test instance reports `"1970-01-01T00:00:00.000"` until you trigger an analytics run.
- Analytics queries against pre-populated tables are fast (single SQL view lookup). Empty tables return empty responses without failing.

## DHIS2 resource paths vs schema names

- Schema name may be singular (e.g. `"dataElement"`).
- Schema `plural` is what the API endpoint uses (`/api/dataElements`).
- Schema `apiEndpoint` gives the relative path in some cases; not always set.
- We default to `/api/{schema.plural}` for CRUD paths in codegen — this has held up across every resource on play/dev and localhost so far.

## Typer single-command apps

- A Typer app with only one registered command runs that command as the default — `python -m dhis2_browser pat --url ...` fails with "unexpected extra argument (pat)". Invoke as `python -m dhis2_browser --url ...`.
- Adding a second command (even a stub like `info`) flips dispatch to subcommand-style. `dhis2-browser` now does this so `pat` is a proper subcommand name.

## DHIS2 `COMPLEX` fields vary wildly

- `schema.properties[].propertyType == "COMPLEX"` in DHIS2 schemas does not mean "nested object with known structure". The server returns some COMPLEX fields as `{}`, others as `[]`, others as `[{...}]`, still others as populated dicts.
- Example: `Constant.attributeValues` is declared COMPLEX but an unset constant returns `attributeValues: []` (a list, not a dict).
- Codegen maps COMPLEX → `Any` (not `dict[str, Any]`). Combined with `model_config = ConfigDict(extra="allow")`, the data is preserved and pydantic doesn't reject mismatched shapes.

## DHIS2 apiToken quirks (v2.42)

While building the seed flow for standard PAT variations:

- **POST endpoint is `/api/apiToken` (singular)**; the **list endpoint is `/api/apiTokens` (plural)**. The plural response contains an array under the key `apiToken` — yes, singular key inside a plural-endpoint response. DHIS2 casing is not perfectly regular.
- `allowedIps` takes **plain IPs only**, not CIDR. `127.0.0.1/32` → error `E1004` "Not a valid ip address". Use `127.0.0.1` and `::1`.
- `allowedReferrers` rejects URLs with **ports and non-HTTPS schemes for localhost**. `http://localhost:3000` → error `E1004` "Not a valid referrer url". `https://example.com` is accepted. Port-bound loopback referrers aren't supported.
- DHIS2 PAT response key `response.key` is the only place the token value is returned. No retrieval afterwards.
- Errors surface as 409 Conflict (not 400 Bad Request) for validation failures on attributes.

## DHIS2 oAuth2Client endpoint (v2.42)

- Schema path: `/api/schemas/oAuth2Client` — capital A. The plural is `oAuth2Clients`.
- Create: `POST /api/oAuth2Clients` with payload `{name, clientId, clientSecret, authorizationGrantTypes, redirectUris, scopes}`.
- `authorizationGrantTypes` is a comma-separated string, not a JSON list. `redirectUris` is comma/newline-separated.
- Upsert pattern: list with `filter=clientId:eq:<id>`, PUT to `/api/oAuth2Clients/{id}` if found, otherwise POST. Keeps re-seeding idempotent.

## FastMCP 3.x `Client` takes a `FastMCP` instance directly

For in-process tests, you don't need stdio framing or subprocess:

```python
from fastmcp import Client
from dhis2_mcp.server import build_server

async def test_x() -> None:
    server = build_server()
    async with Client(server) as client:
        tools = await client.list_tools()
        result = await client.call_tool("whoami", {})
```

`Client` accepts either a transport descriptor (path, URL, config dict) or a `FastMCP` server instance. Passing the instance wires an in-memory transport. No real network, no stdio — just dispatch through FastMCP's tool registry.

The call result shape varies by FastMCP minor version. Defensive extraction:

1. `result.structured_content` — a dict (current preferred shape).
2. `result.data.model_dump()` — if a pydantic model was returned from the tool.
3. `result.content[0].text` parsed as JSON — older MCP content block.

Our test helper `_extract_payload` tries all three. When upgrading FastMCP, check which of these still produces the expected payload.

## Typer single-registered-command apps flatten automatically

We hit this twice: a Typer app with exactly one `@app.command(...)` runs that command as the root, not as a named subcommand. `python -m dhis2_browser pat --foo` fails with "unexpected extra argument (pat)". Two paths:

1. Drop the subcommand name — call `python -m dhis2_browser --foo`.
2. Add a second placeholder command (e.g. `info`) so Typer flips to subcommand-dispatch mode.

We use (2) for `dhis2-browser` now so `dhis2-browser pat ...` stays the documented invocation.

## Watching Playwright work during tests

Tests default to headless Chromium. Set `DHIS2_HEADFUL=1` to flip — the `resolve_headless()` helper in `dhis2_browser.session` reads this env var and propagates to `logged_in_page` and `create_pat`. Explicit `headless=True/False` kwargs override the env. Useful when debugging the login flow or when the user wants to visually confirm what's happening.

## Pydantic datetime serialization on PUT/POST

- Generated models have `created`, `lastUpdated` etc. typed as `datetime`. After `client.get(..., model=X)`, those fields hold real `datetime` objects.
- `model.model_dump(by_alias=True, exclude_none=True)` leaves datetimes as `datetime` objects — `httpx.Request(json=...)` then blows up with `TypeError: Object of type datetime is not JSON serializable`.
- Fix: dump with `mode="json"`. That converts datetime → ISO 8601 string, `UUID → str`, etc.
- Generated CRUD templates now use `model_dump(by_alias=True, exclude_none=True, mode="json")`.
