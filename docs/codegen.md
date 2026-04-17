# Codegen

`dhis2-codegen` is a workspace member that hits a live DHIS2 instance and emits typed pydantic models + resource classes into `packages/dhis2-client/src/dhis2_client/generated/v{NN}/`.

Generated code is **committed**, reviewable in diffs, and forms the typed surface of the client.

## Why a separate member

- **The client wheel on PyPI must stay lean** — no jinja2, no generator tooling.
- **The generator can import `dhis2-client`** to reuse `AuthProvider` / `Dhis2Client` for talking to the live instance.
- **Future plugins** (e.g. custom-schema generators for specific deployments) can depend on `dhis2-codegen` without pulling the rest of the tooling.

## Invocation

Two ways to run it:

```bash
# Standalone module
uv run python -m dhis2_codegen generate --url https://play.im.dhis2.org/stable-2-42-0 \
                                        --username admin --password district

# As a dhis2 CLI subcommand (after Phase 2, when dhis2-cli mounts it via entry points)
dhis2 codegen generate --profile play
```

The CLI subcommand is registered via `[project.entry-points."dhis2.plugins"]` in `dhis2-codegen`'s `pyproject.toml`. `dhis2-cli`'s plugin discovery picks it up at startup.

## Pipeline

1. **Authenticate.** Use one of the shipped `AuthProvider` implementations. For the standalone run, `--username/--password` or `--pat` give Basic/PAT auth. For the CLI flavor, `--profile NAME` reads the stored profile.
2. **Discover version.** `GET /api/system/info` → extract `version` (e.g. `"2.42.0"` → `"v42"`).
3. **Fetch schemas.** `GET /api/schemas?fields=name,plural,apiEndpoint,displayName,klass,metadata,properties[*]` — one request gets every metadata type with their full property definitions.
4. **Write the manifest.** `generated/v42/schemas_manifest.json` — raw snapshot of the schemas response. Audit trail, and the input to emission. Re-running the emitter without re-fetching is possible.
5. **Emit models.** One pydantic `BaseModel` file per schema, in `generated/v42/models/<resource>.py`. Field names mirror DHIS2 wire format (camelCase) so there's no alias translation at parse/serialise time. Nested references use a common `Reference` model with at minimum an `id` field.
6. **Emit resources.** `generated/v42/resources.py` — one `_<Name>Resource` class per metadata type with `get`, `list`, `create`, `update`, `delete`. A `Resources` container class bundles them all and is instantiated by `Dhis2Client.connect()`.
7. **Stamp and format.** `generated/v42/__init__.py` sets `GENERATED = True` and re-exports `Resources`. The whole output directory is run through `ruff format`.

## Schema → pydantic-type mapping

| DHIS2 property type | Python type |
| --- | --- |
| `TEXT`, `IDENTIFIER`, `CONSTANT`, `EMAIL`, `URL`, `PHONENUMBER`, `COLOR` | `str` |
| `BOOLEAN` | `bool` |
| `INTEGER` | `int` |
| `NUMBER` | `float` |
| `DATE`, `DATETIME` | `datetime` |
| `REFERENCE` | Named nested model (min: `{"id": str}`) |
| `COLLECTION` of X | `list[X]` |
| `COMPLEX` | dedicated nested model if `properties` are present, else `dict[str, Any]` |
| `CONSTANT` with `constants=[...]` | `Literal[...]` |

All properties are `Optional` (default `None`) — DHIS2 doesn't reliably mark which are required in the schema response, and "nothing known" beats "wrong schema".

## What lives in `dhis2-codegen`

```
packages/dhis2-codegen/src/dhis2_codegen/
├── __init__.py
├── __main__.py           # python -m dhis2_codegen entry
├── plugin.py             # Plugin + entry-point registration for dhis2 CLI
├── cli.py                # Typer sub-app
├── discover.py           # /api/system/info + /api/schemas fetch, returns SchemasManifest
├── emit.py               # SchemasManifest → files on disk
├── mapping.py            # DHIS2 schema property → Python type string
├── names.py              # camelCase resource → snake_case module + safe Python identifier
└── templates/            # jinja2 templates for model/resource/init files
```

## Trade-offs

- **Committed generated code**, not gitignored. Diffs are reviewable; downstream PyPI users of `dhis2-client` don't need to run codegen to install the library.
- **Minor-version granularity** (`v42`, not `2.42.1`). Patch-level differences aren't worth separate modules.
- **Emission uses jinja2 templates**, not ad-hoc string building. Templates are easier to tweak and diff than escaped f-strings.
- **Tests are on the mapping + naming logic**, not the end-to-end emit. Full emission requires a live instance or a canned manifest fixture; we'll commit a minimal one in `tests/fixtures/` so end-to-end tests don't need network.
- **The generator reuses `dhis2-client`'s auth/client**, so any auth flow that works at runtime also works for codegen. Including OAuth2 PKCE — the generator is just another client consumer.

## Deferred

- **Live first generation** — happens once a DHIS2 v42 instance is reachable with working credentials. After Phase 2 profiles land, `make schemas PROFILE=play` is the one-liner.
- **Type-aware field/filter/order DSL.** For now, `resources.X.list(fields="id,displayName,...")` takes a string. Once codegen lands, we'll build a typed DSL (`Q.fields(R.DataElement.id, R.DataElement.displayName)`) that gives IDE autocomplete over resource properties.
- **Paging helpers.** Initial `list()` defaults to `paging=false` (single request, all items). A `list_paged()` async iterator will come once we hit an instance large enough to care.
