# Doctor plugin

One command that probes a DHIS2 instance for every gotcha tracked in
`BUGS.md` (at the repo root) plus the workspace's hard requirements. Runs
as `dhis2 doctor`, `doctor_run` MCP tool, or the library-level
`service.run_doctor` — same probe set, three surfaces.

## Why it exists

Three reasons to have `doctor`:

1. **Fast triage.** When an example fails against a fresh instance, a
   one-line `dhis2 doctor` answer triangulates whether the problem is
   auth, DHIS2 version, a missing OAuth2 config, or one of the logged
   upstream quirks — without grepping `BUGS.md` by hand.
2. **Drift detection.** When DHIS2 releases fix an upstream bug, a
   `pass` probe flips to `warn` ("bug may have been fixed — re-check").
   Gives us a nudge to clean up workarounds without manually watching
   every DHIS2 release note.
3. **CI / monitoring hook.** The CLI exits non-zero if any probe is
   `fail`; the MCP / Python surfaces return a typed `DoctorReport`.
   Drop into a cron, a status page, or a `make preflight` target
   without extra plumbing.

## Probe inventory

Each probe is a pure read. Running `dhis2 doctor` against a healthy v42
seeded fixture takes ~200ms (probes dispatch concurrently).

| Probe | What it checks | Status meaning |
| --- | --- | --- |
| `dhis2-version` | `/api/system/info.version >= 2.42` (workspace hard requirement) | `pass`: requirement met. `fail`: version too old; things break. |
| `auth` | `/api/me` returns a username | `pass`: authenticated. `fail`: credentials rejected or endpoint unreachable. |
| `login-config` | Informational — prints title, OIDC providers, logo flag from `/api/loginConfig` | Always `pass` unless the endpoint itself fails. |
| `oauth2-discovery` | `/.well-known/openid-configuration` present + has `authorization_endpoint` / `token_endpoint` / `jwks_uri` | `pass`: OAuth2 server is configured. `skip`: OAuth2 not enabled (404). `fail`: enabled but malformed. (BUGS.md #4) |
| `analytics-rawdata-json-suffix` | `GET /api/analytics/rawData` (no `.json`) still 404s | `pass`: workaround still needed. `warn`: upstream may have fixed content negotiation. (BUGS.md #1) |
| `userrole-authorities-naming` | `/api/schemas/userRole` still reports `name=authority fieldName=authorities` | `pass`: workaround still needed. `warn`: schema shape changed — re-check the OAS-derived code path. (BUGS.md #8) |
| `outlier-algorithm-enum` | `GET /api/analytics/outlierDetection?algorithm=MOD_Z_SCORE` still returns 400 | `pass`: server still rejects the OAS-emitted name. `warn`: server now accepts it — OAS vs runtime may be in sync again. (BUGS.md #13) |
| `custom-logo-flag` | `useCustomLogoFront` in `/api/loginConfig` mirrors `keyUseCustomLogoFront` system setting | `pass`: consistent. `warn`: mismatch — an upload won't be visible until both agree. (BUGS.md #11) |

## Statuses

- `pass` — requirement met OR bug workaround still functional.
- `warn` — something non-fatal changed; re-check the linked BUGS entry.
- `fail` — a hard requirement (auth, version) failed. CLI exits 1.
- `skip` — feature disabled on this instance (e.g. OAuth2 not configured).

The CLI prints a table; `--json` emits the `DoctorReport` pydantic model
for scripting. The MCP `doctor_run` tool returns the same structure.

## Example output

```
              dhis2 doctor — http://localhost:8080 (DHIS2 2.42.4)
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ probe                     ┃ status ┃ message                   ┃ bugs        ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ dhis2-version             │  PASS  │ 2.42.4 (requires 2.42+)   │             │
│ auth                      │  PASS  │ authenticated as admin    │             │
│ login-config              │  PASS  │ title='dhis2-utils local' │             │
│                           │        │ oidc-providers=['dhis2']  │             │
│ oauth2-discovery          │  PASS  │ issuer=http://localhost.. │             │
│ analytics-rawdata-json-.. │  PASS  │ 404 without .json OK      │ BUGS.md #1  │
│ userrole-authorities-..   │  PASS  │ schema reports 'authority'│ BUGS.md #8  │
│ outlier-algorithm-enum    │  PASS  │ server still rejects      │ BUGS.md #13 │
│                           │        │ MOD_Z_SCORE               │             │
│ custom-logo-flag          │  PASS  │ consistent: both true     │ BUGS.md #11 │
└───────────────────────────┴────────┴───────────────────────────┴─────────────┘
8 pass / 0 warn / 0 fail / 0 skip (8 probes)
```

## Adding a new probe

1. Add an `async def _probe_<name>(client: Dhis2Client) -> ProbeResult` to
   `service.py`. Keep it a pure read (no POST / PUT / DELETE).
2. Append it to the `_PROBES` tuple so `run_doctor` picks it up.
3. Add a row in the inventory table above.
4. Add a respx test in `test_doctor_plugin.py` covering at least one
   success + one drift / failure case.

Probes are independent — they run concurrently via `asyncio.gather`, so
adding one doesn't measurably slow the command.

## Not covered here

- **Behavioural quirks that require a write** (soft-delete on
  `/api/dataValueSets`, `organisationUnits` capture-scope DESCENDANT
  rule, bulk-import 409 reporting) — probing them would mutate state.
  Documented in BUGS.md; not automated.
- **UI bugs** (login-app `html { transparent }` at non-100% zoom) —
  needs a browser; not reachable from an HTTP probe.
- **dhis.conf audit / changelog settings** — DHIS2 doesn't expose these
  via the API.
