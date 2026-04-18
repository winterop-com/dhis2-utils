# dhis2-client examples

Small, runnable scripts that exercise `dhis2-client` against a real DHIS2 instance. Each one is self-contained: pick the auth mode that matches your setup, set a couple of environment variables, and `uv run python examples/<name>.py`.

All examples target the committed `infra/dhis.sql.gz` by default — i.e. `make dhis2-run` (or `make dhis2-up-seeded` if you also want freshly-minted PATs) and they just work.

## Running

```bash
# bring up the bundled DHIS2 + seed PATs / OAuth2 client
make dhis2-run                    # foreground; Ctrl+C to stop

# in another terminal, source the seeded creds
set -a; source infra/home/credentials/.env.auth; set +a

uv run python examples/01_whoami.py
uv run python examples/02_list_data_elements.py
uv run python examples/03_push_data_value.py
```

## Index

| File | Shows | Auth |
| --- | --- | --- |
| [`01_whoami.py`](01_whoami.py) | Minimal client lifecycle — connect, call `/api/me`, close. | PAT or Basic |
| [`02_list_data_elements.py`](02_list_data_elements.py) | Typed generated resources — list data elements with pagination. | PAT or Basic |
| [`03_push_data_value.py`](03_push_data_value.py) | Writing aggregate data via the client's raw escape hatch. | PAT or Basic |
| [`04_oidc_login.py`](04_oidc_login.py) | OIDC login — OAuth 2.1 authorization-code flow with PKCE against `/oauth2/authorize` + `/oauth2/token`, FastAPI redirect receiver, SQLite token store, automatic refresh. | OAuth2 / OIDC |

## Environment

The examples read these env vars (with `setdefault` so missing ones fall back to the seeded local stack):

- `DHIS2_URL` — default `http://localhost:8080`
- `DHIS2_PAT` — a Personal Access Token (from `.env.auth`)
- `DHIS2_USERNAME`, `DHIS2_PASSWORD` — for Basic auth fallback

If you're running against a real instance, override `DHIS2_URL` and use an appropriate credential.
