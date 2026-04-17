# `dhis2` CLI

`dhis2-cli` is a thin workspace member. Its only job is to build a Typer root and mount every discovered plugin's sub-app. All real work lives in `dhis2-core` plugin `service.py` modules.

## Entry point

```toml
# packages/dhis2-cli/pyproject.toml
[project.scripts]
dhis2 = "dhis2_cli.main:app"
```

`uv sync --all-packages` installs the script; after that, `dhis2` is on PATH (via `uv run`).

## The root

```python
# packages/dhis2-cli/src/dhis2_cli/main.py
def build_app() -> typer.Typer:
    app = typer.Typer(
        help="dhis2 — command-line interface for DHIS2 (discovers plugins from dhis2-core).",
        no_args_is_help=True,
        add_completion=False,
    )
    for plugin in discover_plugins():
        plugin.register_cli(app)
    return app


app = build_app()
```

`build_app()` returns a fresh app per call. The module-level `app` is a single pre-built instance that the `dhis2` console script binds to. Tests call `build_app()` so they get an isolated app without the side effect of re-registering on the module-level instance.

## Today's surface

```
$ dhis2 --help
 Usage: dhis2 [OPTIONS] COMMAND [ARGS]...

 dhis2 — command-line interface for DHIS2 (discovers plugins from dhis2-core).

╭─ Commands ───────────────────────────────────────────────────────────────╮
│ system   DHIS2 system info.                                              │
│ codegen  Generate version-aware DHIS2 client code from /api/schemas.     │
╰──────────────────────────────────────────────────────────────────────────╯
```

- `system` comes from `dhis2_core.plugins.system` (built-in).
- `codegen` comes from `dhis2-codegen`'s entry point registration. No `dhis2-core` code knows about it.

### `dhis2 system`

```
$ dhis2 system --help
 Usage: dhis2 system [OPTIONS] COMMAND [ARGS]...

 DHIS2 system info and current-user access.

╭─ Commands ───────────────────────────────────────────────────────────────╮
│ whoami   Print the authenticated DHIS2 user for the current environment. │
│ info     Print basic DHIS2 system info for the current environment.      │
╰──────────────────────────────────────────────────────────────────────────╯
```

### End-to-end example

```bash
# Source the seeded creds (see [Local DHIS2 setup](../local-setup.md))
set -a; source infra/home/credentials/.env.auth; set +a

dhis2 system whoami
# → admin (System Administrator)

dhis2 system info
# → version=2.42.4 revision=eaf4b70 name=DHIS 2
```

## Profile resolution

Each command resolves a `Profile` via `profile_from_env()` at invocation time. That reads:

1. `DHIS2_URL` — required.
2. `DHIS2_PAT` — preferred.
3. `DHIS2_USERNAME` + `DHIS2_PASSWORD` — fallback.

Missing env → the command raises `NoProfileError`. A future `dhis2 init` subcommand will walk the user through a one-time setup; it's not built yet.

## Testing

Two tiers:

### Unit (hermetic)

`tests/test_cli_surface.py` uses `typer.testing.CliRunner` with a fresh `build_app()` to verify:

- The help text lists the expected plugins (discovery works).
- Sub-app help lists the expected commands (registration works).

No DHIS2 needed.

### Integration (hits localhost)

`tests/test_cli_integration.py` is marked `@pytest.mark.slow`. Each test:

1. Skips if `DHIS2_PAT` isn't populated (no seeded stack).
2. Monkey-patches `DHIS2_URL` + `DHIS2_PAT` into the environment.
3. Invokes the CLI via `CliRunner` and asserts the live output.

The `conftest.py` auto-loads `infra/home/credentials/.env.auth` on import so `DHIS2_PAT` is available whenever the infra stack has been seeded.

## Why `CliRunner` instead of subprocess

Subprocess invocation (`uv run dhis2 ...`) works but is slow (~2s per test for venv setup). `CliRunner` invokes the Typer app in-process, which is ~5ms per test and gives us the same correctness guarantee. We sacrifice testing the console-script entry point itself (unlikely to be the bug site); we gain fast feedback.

## Extension

Add a new CLI command by creating a new plugin folder under `dhis2_core/plugins/<name>/`. As soon as the package is importable, `dhis2 <name>` is available. No edits to `dhis2-cli`.

External plugins declare:

```toml
[project.entry-points."dhis2.plugins"]
<name> = "<package>.<module>:plugin"
```

— and they appear in `dhis2 --help` on next run.
