# Running DHIS2 locally

`infra/` holds everything needed to stand up a local DHIS2 instance (plus pgAdmin and optionally Superset) for development and integration tests. It's the workspace's answer to "how do I run a real DHIS2 I can point the client at?"

## Prerequisites

- Docker Desktop (or `docker compose` on Linux)
- `dhis.sql.gz` — a PostgreSQL dump of DHIS2 metadata + data. The repo does not ship one. Drop yours at `infra/dhis.sql.gz` before first run. Without it, Postgres starts empty.
- Workspace installed: `make install`

## Quick start

```bash
# one-shot: bring it up, wait for readiness, seed standard PATs + OAuth2 client
make dhis2-up-seeded DHIS2_VERSION=42

# credentials file written to:
cat infra/home/credentials/.env.auth

# stop when done
make dhis2-down
```

Or step-by-step from `infra/`:

```bash
cd infra

# what DHIS2 images can I pull from Docker Hub?
make versions

# pull + start the base stack (DHIS2 + pgAdmin) on http://localhost:8080
make up DHIS2_VERSION=42

# block until /api/me responds
make wait

# seed standard auth (6 PAT variations + OAuth2 client)
make seed

# watch the logs
make logs

# verify it's up
make status

# stop when done
make down
```

You talk to **one** DHIS2 instance at a time. `DHIS2_VERSION` just picks which Docker image to run — it has nothing to do with URL paths. DHIS2 APIs are always at `/api/...`, never `/api/v42/...`. Version differences are in payload/response shapes, and those are handled by `dhis2-client`'s per-version generated modules (see [Version-aware clients](architecture/versioning.md)).

Defaults: DHIS2 42, admin / district, http://localhost:8080.

## Targets

| Target | What it does |
| --- | --- |
| `make versions` | Queries Docker Hub for `dhis2/core:*` tags |
| `make pull DHIS2_VERSION=X` | Pulls the selected DHIS2 image |
| `make build` | Builds the supporting images (postgres + glowroot-installer) |
| `make up DHIS2_VERSION=X` | Starts the base stack in the background (keeps volumes) |
| `make up-fresh DHIS2_VERSION=X` | Wipes volumes + logs and starts clean |
| `make up-full DHIS2_VERSION=X` | Starts the base stack plus Superset BI on :8088 |
| `make up-full-fresh DHIS2_VERSION=X` | Wipe + full stack |
| `make down` | Stops the stack (keeps volumes) |
| `make clean` | Nukes volumes, logs, and runtime data |
| `make status` | `docker compose ps` + DHIS2 reachability probe |
| `make ps` | `docker compose ps` only |
| `make logs` | Follows DHIS2 + Postgres logs |
| `make pat` | Mints a single Playwright PAT against the running instance (delegates to `dhis2-browser`) |
| `make wait` | Blocks until `/api/me` responds — readiness gate before seeding |
| `make seed` | Creates 6 PAT variations + OAuth2 client; writes `infra/home/credentials/.env.auth` |
| `make up-seeded` | `up` + `wait` + `seed` — one-shot DHIS2 with auth ready to use |

All targets honor `DHIS2_VERSION`, `DHIS2_URL`, `DHIS2_USER`, `DHIS2_PASS` environment overrides.

## What's in `infra/`

```
infra/
├── Makefile                 # top-level targets listed above
├── compose.yml              # core: postgres + dhis2 + glowroot-installer + analytics-trigger
├── compose.pgadmin.yml      # adds pgAdmin on :5050
├── compose.superset.yml     # adds Superset BI on :8088
├── Dockerfile               # custom postgres image with bcrypt
├── Dockerfile.superset      # custom Superset image
├── initdb.sh                # first-boot Postgres init: load dump, reset all user passwords
├── run.sh                   # convenience wrapper (pre-existing)
├── scripts/
│   ├── list_versions.py     # queries Docker Hub for dhis2/core tags
│   └── startup.sh           # DHIS2 runtime entry (from source repo)
├── glowroot/admin.json      # glowroot JVM profiler seed config
├── pgadmin4/                # pgAdmin bootstrap (pre-registered server, masked pgpass)
├── superset/                # Superset config + seed dashboard scripts + views.sql
├── home/                    # bind-mounted into DHIS2 container (dhis.conf, logs, glowroot jar)
├── .env.example             # template for overrides (never commit filled-in .env)
└── .gitignore               # ignores logs, .env, local SQL dumps, generated PNGs
```

## How this ties into the workspace

- Integration tests (`make test-slow`) that hit `DHIS2_LOCAL_URL` (default `http://localhost:8080`) rely on the stack being up.
- The `local_pat` pytest fixture minting PATs via Playwright works against whatever URL you've set — so point it at this stack, or any other local DHIS2.
- `make pat` inside `infra/` is the quickest way to mint a PAT for the running stack and print it.

## Seeded auth

`make seed` creates these credentials on each run (all tied to the admin user):

| Variable | What it is |
| --- | --- |
| `DHIS2_PAT_DEFAULT` | Unrestricted PAT, no expiry |
| `DHIS2_PAT_READ_ONLY` | GET-only method allowlist |
| `DHIS2_PAT_WRITE` | GET/POST/PUT/PATCH/DELETE allowlist |
| `DHIS2_PAT_SHORT_EXPIRY` | Expires in 1 day — exercise refresh handling |
| `DHIS2_PAT_LOCAL_ONLY` | IP allowlist: loopback only |
| `DHIS2_PAT_REFERRER_BOUND` | Referrer allowlist for `https://example.com` |
| `DHIS2_PAT`, `DHIS2_LOCAL_PAT` | Aliases for `DEFAULT` — what most code looks at |
| `DHIS2_OAUTH_CLIENT_ID` | `dhis2-utils-local` — deterministic client id |
| `DHIS2_OAUTH_CLIENT_SECRET` | Deterministic local-only secret |
| `DHIS2_OAUTH_REDIRECT_URI` | `http://localhost:8765` — matches dhis2-client's OAuth2 default |
| `DHIS2_OAUTH_SCOPES` | `openid email ALL` |

The variation list is in `infra/scripts/_seed_auth_variations.py`; the OAuth2 client config is in `infra/scripts/_seed_auth_oauth2.py`. Edit either to change what gets seeded.

Source an integration test's env with:

```bash
set -a; source infra/home/credentials/.env.auth; set +a
make test-slow
```

## What's intentionally not committed

- `dhis.sql.gz` — huge, user-specific, carries real data.
- `.env` — may contain real credentials.
- `home/logs/`, `home/glowroot/`, `home/files/` — runtime state that a fresh clone shouldn't inherit.
- `home/credentials/` — the seeded `.env.auth` file lives here; regenerate with `make dhis2-seed`.
- `home/dhis-google-auth.json` — OAuth client secrets for DHIS2's Google integration.

## Origin

`infra/` was imported from `github.com/mortenoh/dhis2-docker` on 2026-04-17. The original repo remains the upstream; changes made here may later be pushed back if we stick to that arrangement.
