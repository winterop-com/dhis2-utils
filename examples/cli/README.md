# CLI examples

Shell invocations of the `dhis2` Typer CLI (installed with `uv sync`). Every CLI command resolves a DHIS2 profile first (from `.dhis2/profiles.toml`, `~/.config/dhis2/profiles.toml`, or `DHIS2_URL`+`DHIS2_PAT` env) and calls into the matching `dhis2-core` plugin.

## Prerequisites

```bash
make dhis2-run                               # starts DHIS2 + seeds auth in .env.auth
set -a; source infra/home/credentials/.env.auth; set +a

# create a local profile so `dhis2 ...` commands resolve it — secrets via env, never argv
dhis2 profile add local --url http://localhost:8080 --auth pat --default --verify
```

## Shell scripts

Each script is small and self-contained. Run with `bash examples/cli/<name>.sh`.
