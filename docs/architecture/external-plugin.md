# Shipping an external plugin

`dhis2w-core`'s plugin loader (`dhis2w_core.plugin`) walks two sources at CLI
startup:

1. A package scan over `dhis2w_core.v42.plugins.*` — this picks up every
   first-party plugin under `packages/dhis2w-core/src/dhis2w_core/v42/plugins/`.
2. `importlib.metadata.entry_points(group="dhis2.plugins")` — any
   separately-installed Python package can register a plugin here.

**External plugins are full first-class citizens.** They get the same
access to `Dhis2Client`, the same profile resolution, the same MCP
integration, and the same CLI mounting — no hooks, no registry file, no
core code changes.

## The reference implementation

`examples/plugin-external/` ships a minimal runnable plugin
(`dhis2-plugin-hello`) that greets the authenticated DHIS2 user:

```
examples/plugin-external/
├── pyproject.toml              [project.entry-points."dhis2.plugins"]
│                                  hello = "dhis2_plugin_hello:plugin"
└── src/dhis2_plugin_hello/
    ├── __init__.py             exports `plugin = _HelloPlugin()`
    ├── service.py              uses `open_client(profile)` like first-party plugins
    ├── cli.py                  Typer sub-app; `register(app)` mounts `dhis2 hello`
    └── mcp.py                  FastMCP tool `hello_say`
```

Install + verify:

```bash
uv add --editable examples/plugin-external/
dhis2 --help | grep hello
# hello        External plugin example.

dhis2 hello say
# Hello, admin admin!
```

## The contract

Two things make a package a valid external plugin:

1. A module-level `plugin` attribute that satisfies `dhis2w_core.plugin.Plugin`
   — pydantic model with `name`, `description`, `register_cli(app)`,
   `register_mcp(mcp)`. The hello example uses a frozen `BaseModel`;
   first-party plugins do the same.
2. An entry-point line in `pyproject.toml` pointing at that attribute:
   ```toml
   [project.entry-points."dhis2.plugins"]
   <surface-name> = "your_package:plugin"
   ```
   The group name `dhis2.plugins` is fixed — the loader only looks
   there. The surface-name on the left of `=` is free (but usually
   matches what ends up in `dhis2 <name>`).

That's the entire contract. Everything else (service.py / cli.py / mcp.py
file split) is convention, not requirement — a plugin that only registers
a CLI (and no MCP tool) simply implements `register_mcp` as a no-op, or
vice versa.

## Why CLI + MCP parity is voluntary

Every first-party plugin ships both — same typed call from either surface
is a hard rule in this workspace. External plugins aren't obligated. A
plugin that only makes sense in a terminal can skip MCP registration; an
agent-only tool can skip the CLI side. Just make the corresponding
`register_*` a no-op:

```python
def register_cli(self, app: Any) -> None:
    return None  # MCP-only plugin
```

## Error behaviour

If an entry-point's import fails (package not installed in the current
env, typo in the import path), the loader silently skips it —
`ImportError` isn't propagated. Broken plugins shouldn't take down
`dhis2 --help`.

If a plugin raises during `register_cli` / `register_mcp`, that *does*
propagate, and the CLI aborts. Fail loudly when the plugin itself is
broken; stay quiet when the environment doesn't have it installed.

## Testing an external plugin

Same tooling as first-party: respx for HTTP mocking, Typer's `CliRunner`
for CLI verification, `fastmcp.Client` for MCP tools. Nothing plugin-
specific — test `service.py` directly, test `cli.py` via `CliRunner`
against a fake `Resources` or a mocked `open_client`.

## Publishing

`uv build` → `uv publish` (or PyPI Trusted Publishing via your own GitHub
Actions workflow). Users install your plugin alongside their `dhis2w-cli`
install — `uv tool install --with your-plugin-name dhis2w-cli` for a
global tool, or `uv add your-plugin-name` inside a project that already
has `dhis2w-cli`. Version-pin `dhis2w-client` / `dhis2w-core` in your
`dependencies` if your plugin uses generated models that might move.
