# `dhis2` CLI

`dhis2w-cli` is a thin workspace member. Its only job is to build a Typer root and mount every discovered plugin's sub-app. All real work lives in `dhis2w-core` plugin `service.py` modules.

## Entry point

```toml
# packages/dhis2w-cli/pyproject.toml
[project.scripts]
dhis2 = "dhis2w_cli.main:app"
```

`uv sync --all-packages` installs the script; after that, `dhis2` is on PATH (via `uv run`).

## The root

```python
# packages/dhis2w-cli/src/dhis2w_cli/main.py
def build_app() -> typer.Typer:
    app = typer.Typer(
        help="dhis2 — command-line interface for DHIS2 (discovers plugins from dhis2w-core).",
        no_args_is_help=True,
        add_completion=False,
    )
    for plugin in discover_plugins():
        plugin.register_cli(app)
    return app


app = build_app()
```

`build_app()` returns a fresh app per call. The module-level `app` is a single pre-built instance that the `dhis2` console script binds to. Tests call `build_app()` so they get an isolated app without the side effect of re-registering on the module-level instance.

## Sample `--help` output

```
$ dhis2 --help
 Usage: dhis2 [OPTIONS] COMMAND [ARGS]...

 dhis2 — command-line interface for DHIS2 (discovers plugins from dhis2w-core).

╭─ Commands ───────────────────────────────────────────────────────────────╮
│ system   DHIS2 system info.                                              │
│ codegen  Generate version-aware DHIS2 client code from /api/schemas.     │
╰──────────────────────────────────────────────────────────────────────────╯
```

- `system` comes from `dhis2w_core.v42.plugins.system` (built-in).
- `codegen` comes from `dhis2w-codegen`'s entry point registration. No `dhis2w-core` code knows about it.

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

## Global flags

The root callback exposes two flags that apply to every sub-command:

| Flag | Effect |
| --- | --- |
| `--profile, -p <name>` | Overrides the active profile (beats `DHIS2_PROFILE` env + the TOML default). |
| `--debug, -d` | Enables stderr HTTP logging — every request emits `method URL -> status (bytes, ms)`. Useful when debugging why a command talked to a surprising endpoint. |

The debug flag wires the stdlib `logging` module at DEBUG level for `dhis2w_client` + `dhis2w_core`. Each per-version `dhis2w_client.v{N}.client.Dhis2Client._request` emits structured `%s %s -> %d (%d bytes, %.0fms)` lines via the `dhis2w_client.http` logger; plugins that log via their own namespace also surface under `-d`. The active plugin tree (`v41` / `v42` / `v43`) is visible via `dhis2 --version` — see the version banner section below.

Output is written to stderr so `dhis2 -d route list > routes.json` still produces clean JSON on stdout.

## Polling long-running tasks (`--watch`)

Commands that kick off async DHIS2 jobs (`analytics refresh`, `maintenance dataintegrity run`, `maintenance task watch`) take `--watch/-w` to poll the task to completion. The shared renderer in `dhis2w_core.cli_task_watch` uses `rich.progress.Progress` with a spinner + elapsed-time column and streams each notification as it arrives, colour-coded by level (`INFO`/`WARN`/`ERROR`). The Rich console writes to stderr so stdout stays free when piping.

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

Add a new CLI command by creating a new plugin folder under `dhis2w_core/plugins/<name>/`. As soon as the package is importable, `dhis2 <name>` is available. No edits to `dhis2w-cli`.

External plugins declare:

```toml
[project.entry-points."dhis2.plugins"]
<name> = "<package>.<module>:plugin"
```

— and they appear in `dhis2 --help` on next run.
