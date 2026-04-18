# Running DHIS2 locally

`infra/` holds everything needed to stand up a local DHIS2 instance (plus pgAdmin and Glowroot APM) for development and integration tests. It's the workspace's answer to "how do I run a real DHIS2 I can point the client at?"

## Prerequisites

- Docker Desktop (or `docker compose` on Linux)
- `dhis.sql.gz` — a PostgreSQL dump of DHIS2 metadata + data. The repo does not ship one. Drop yours at `infra/dhis.sql.gz` before first run. Without it, Postgres starts empty.
- Workspace installed: `make install`

## Quick start

```bash
# one-shot: bring it up, wait for readiness, seed standard PATs + OAuth2 client
make dhis2-run DHIS2_VERSION=42

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
| `make up DHIS2_VERSION=X` | Starts the stack in the background (keeps volumes) |
| `make up-fresh DHIS2_VERSION=X` | Wipes volumes + logs and starts clean |
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
├── Dockerfile               # custom postgres image with bcrypt
├── initdb.sh                # first-boot Postgres init: load dump, reset all user passwords
├── run.sh                   # convenience wrapper (pre-existing)
├── scripts/
│   ├── list_versions.py     # queries Docker Hub for dhis2/core tags
│   └── startup.sh           # DHIS2 runtime entry (from source repo)
├── glowroot/admin.json      # glowroot JVM profiler seed config
├── pgadmin4/                # pgAdmin bootstrap (pre-registered server, masked pgpass)
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
| `DHIS2_OAUTH_SCOPES` | `ALL` — DHIS2 only recognises the single `ALL` scope |

The variation list is in `infra/scripts/_seed_auth_variations.py`; the OAuth2 client config is in `infra/scripts/_seed_auth_oauth2.py`. Edit either to change what gets seeded.

Source an integration test's env with:

```bash
set -a; source infra/home/credentials/.env.auth; set +a
make test-slow
```

### OAuth2 / OIDC requires extra `dhis.conf` keys

The PAT variants work out of the box against a vanilla DHIS2 instance. **OAuth2 does not.** DHIS2 ships Spring Authorization Server but ships it switched off, and its `/api` JWT validator only trusts issuers registered in `dhis.conf`. The seeded `make dhis2-seed` creates the OAuth2 client but cannot toggle server-side config — you need the following in `dhis.conf` before `dhis2 profile login <name>` will work end-to-end.

For the full walkthrough, including troubleshooting and why each key matters, see [Connecting to DHIS2 § OAuth2 / OIDC](guides/connecting-to-dhis2.md#option-3-oauth2-oidc).

```properties
oauth2.server.enabled                  = on
server.base.url                        = http://localhost:8080
oidc.jwt.token.authentication.enabled  = on
oidc.oauth2.login.enabled              = on

oidc.provider.dhis2.client_id         = dhis2-utils-local
oidc.provider.dhis2.client_secret     = dhis2-utils-local-secret-do-not-use-in-prod
oidc.provider.dhis2.issuer_uri        = http://localhost:8080
oidc.provider.dhis2.authorization_uri = http://localhost:8080/oauth2/authorize
oidc.provider.dhis2.token_uri         = http://localhost:8080/oauth2/token
oidc.provider.dhis2.jwk_uri           = http://localhost:8080/oauth2/jwks
oidc.provider.dhis2.user_info_uri     = http://localhost:8080/userinfo
oidc.provider.dhis2.redirect_url      = http://localhost:8765
oidc.provider.dhis2.scopes            = ALL
oidc.provider.dhis2.mapping_claim     = sub
```

See `docs/architecture/auth.md` for what each key does and which failure mode it unblocks. After editing `dhis.conf`, restart the stack (`make dhis2-down && make dhis2-run`).

## The committed `dhis.sql.gz`

**`infra/dhis.sql.gz` is the one exception** to the usual "no DB dumps in repo" rule. It's a tiny, synthetic dump (~1–3 MB compressed) that makes a fresh clone usable end-to-end without any external data. After `make dhis2-run` (or `make dhis2-run`) it gives you:

- **Org unit tree** — `Norway` → `Oslo`, `Vestland`, `Trøndelag`, `Nordland` (4 fylker)
- **7 monthly data elements** — ANC 1st/4th visit, deliveries in facility, live births, BCG + measles vaccinations, OPD consultations
- **1 dataset** (`Norway Monthly Indicators`, period type Monthly) with all 7 DEs assigned to all 4 fylker
- **~3,700 data values** covering Jan-2015 through Dec-2025, monthly, deterministic but randomised so analytics produce varied charts
- **Pre-populated analytics tables** so dashboards render immediately
- **Pre-seeded OAuth2 client** `dhis2-utils-local` (see [Connecting to DHIS2 guide](guides/connecting-to-dhis2.md))
- **Admin user** with `openId=admin` already set so OIDC JWTs validate

### Committed credentials

These are deterministic and documented here on purpose — the dump is a synthetic test fixture, not a real instance. Never reuse these values outside local dev.

| What | Value |
| --- | --- |
| DHIS2 URL | `http://localhost:8080` |
| Login | `admin` / `district` |
| OAuth2 client id | `dhis2-utils-local` |
| OAuth2 client secret (plaintext) | `dhis2-utils-local-secret-do-not-use-in-prod` |
| OAuth2 redirect URI | `http://localhost:8765` |
| OAuth2 scope | `ALL` |

PATs are **not** committed (DHIS2 generates them per-request, so there's nothing deterministic to bake in). Run `make dhis2-run` (brings up the stack detached and seeds in one shot) — PATs land in `infra/home/credentials/.env.auth`.

### Regenerating the dump

```bash
make dhis2-build-e2e-dump
```

Wipes the postgres volume, brings up an empty DHIS2, runs `infra/scripts/build_e2e_dump.py` (metadata + data + analytics + OAuth2 client + openId mapping), then `pg_dump`'s the result into `infra/dhis.sql.gz`. Commit the resulting diff.

**Only re-run when you intentionally want the committed dump to change** — for example, to add more data elements, extend the date range, or refresh the OAuth2 client config. Everyday workflows use the existing dump.

## What's intentionally not committed

- `dhis.sql.gz` variants other than `infra/dhis.sql.gz` — `*.sql.gz` is still the default ignore pattern; only the one filename is whitelisted.
- `.env` — may contain real credentials.
- `home/logs/`, `home/glowroot/`, `home/files/` — runtime state that a fresh clone shouldn't inherit.
- `home/credentials/` — the seeded `.env.auth` file lives here; regenerate with `make dhis2-seed`.
- `home/dhis-google-auth.json` — OAuth client secrets for DHIS2's Google integration.

## Origin

`infra/` was imported from `github.com/mortenoh/dhis2-docker` on 2026-04-17. The original repo remains the upstream; changes made here may later be pushed back if we stick to that arrangement.
