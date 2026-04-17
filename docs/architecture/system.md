# System module

The `system` module on `Dhis2Client` wraps the non-metadata system endpoints — `/api/system/info` and `/api/me`. These don't come from `/api/schemas`, so they're **hand-written** in `dhis2_client/system.py` rather than generated.

## Usage

```python
async with Dhis2Client(...) as client:
    info = await client.system.info()
    # -> SystemInfo(version="2.44-SNAPSHOT", revision="abc1234", ...)

    me = await client.system.me()
    # -> Me(id="xY123", username="system", authorities=["ALL"], ...)
```

`client.system` is initialised in `Dhis2Client.__init__` — it's available before `connect()` completes. That matters because `connect()` itself calls `system.info()` internally to discover the version.

## Models

Both `SystemInfo` and `Me` carry `model_config = ConfigDict(extra="allow")` so unknown fields from the DHIS2 response are preserved on the model (accessible via `model.__pydantic_extra__` or dict-style). That's deliberate — system endpoints accumulate fields across DHIS2 versions and we don't want to silently drop them.

The common fields are explicitly typed:

- **`SystemInfo`** — `version`, `revision`, `buildTime`, `serverDate`, `contextPath`, `calendar`, `dateFormat`, `systemId`, `systemName`
- **`Me`** — `id`, `username`, `displayName`, `email`, `firstName`, `surname`, `authorities`, `organisationUnits`

## Why hand-written, not generated

`/api/schemas` lists metadata types. `SystemInfo` and `Me` are not metadata types — they're computed endpoints. They'd be missing from any codegen run. Hand-writing them is the correct call.

Same logic will apply to the next batch of modules: tracker, data values, analytics. Those are computed/derived endpoints with their own API shapes.

## Open question

Should `client.system.info()` cache its result for the lifetime of the client? `Dhis2Client.connect()` already fetches it once (for version discovery); a second call via `client.system.info()` re-fetches. For now the two paths don't share state — simplest. If latency matters, a lazy cache on the client is a small change.
