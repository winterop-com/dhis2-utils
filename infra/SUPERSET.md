# Apache Superset for DHIS2 — local introduction

A short tour of the Superset stack that ships with this repo: what it is, how it's wired into the DHIS2 stack, the dashboards you get out of the box, and how to extend them.

## What is Superset?

[Apache Superset](https://superset.apache.org/) is an open-source business-intelligence tool — think "Tableau / Power BI, except free and SQL-first". It connects to any database with a SQLAlchemy driver, lets you write SQL or build queries through a UI, and then turns the results into charts and dashboards. For DHIS2 specifically, Superset is gaining traction as a way to do ad-hoc analysis and custom reporting on top of the `analytics_*` tables that DHIS2 generates after running its analytics export job — without going through DHIS2's own Data Visualizer.

In this repo, Superset is **opt-in**: a regular `make run` does not bring it up, since it adds 4 containers and ~1.5 GB of RAM. Use `make run-full` when you want it.

```bash
make run-full
```

That brings up the lean stack (DHIS2 + postgres + glowroot + pgadmin) plus:

| Container | Image | Role |
|---|---|---|
| `superset-db` | `postgres:16-alpine` | Superset's own metadata DB (its dashboards, queries, users) |
| `superset-redis` | `redis:7-alpine` | Cache backend |
| `superset-init` | custom (`apache/superset:4.1.1` + `psycopg2-binary` + `httpx`) | One-shot: `superset db upgrade` + create admin user + register the DHIS2 postgres as a Superset database |
| `superset` | same custom image | Web UI on port `8088` |
| `superset-seed` | same custom image | One-shot: runs `superset/seed_dashboard.py` against the freshly-started web service to seed datasets, charts, and dashboards |

When `make run-full` finishes you can browse to **http://localhost:8088** and log in as `admin` / `admin`. The DHIS2 database is already registered, four pre-built dashboards are already populated, and the data is already there. No clicks to set anything up.

## The dashboards you get for free

All four dashboards live on top of the same virtual dataset (`dhis2_aggregate`) which joins the universal `analytics` parent inheritance table with `analytics_rs_dataelementstructure` and `analytics_rs_orgunitstructure` for friendly column names. Filters use `ILIKE` substring patterns on data element *names*, never UIDs — so a dashboard automatically shows whatever data your dump happens to contain and stays empty if there's nothing matching.

### 1. DHIS2 Aggregate Overview

URL: http://localhost:8088/superset/dashboard/dhis2-aggregate-overview/

Generic structural overview of the dump. No filters. Shows total data points, distinct DEs, distinct OUs, top 10 DEs by volume, period-type distribution, time series, and a province table. **Always populated** — runs against the entire `analytics` table.

### 2. DHIS2 Climate

URL: http://localhost:8088/superset/dashboard/dhis2-climate/

Filtered on `dataelement ILIKE '%temperature%' OR '%temp%' OR '%precipitation%' OR '%rain%' OR '%humidity%' OR '%climate%'`. Designed for dumps that integrate climate data (ERA5-Land, CHIRPS, AirGradient sensors, or DHIS2-native climate indicators). Shows readings count, distinct metrics, reporting locations, a per-metric breakdown, multi-line time series of average value by metric, and a province table.

### 3. DHIS2 Population

URL: http://localhost:8088/superset/dashboard/dhis2-population/

Filtered on `dataelement ILIKE '%population%'`. For any dump that includes population estimate data elements (most do — DHIS2 ships with population by single age, by 5-year band, etc). Shows record count, total reported population, distinct indicators, year-on-year totals, by-province bar chart, and a province × year matrix table.

### 4. DHIS2 Disease Surveillance

URL: http://localhost:8088/superset/dashboard/dhis2-disease-surveillance/

Filtered on `dataelement ILIKE '%cases%' OR '%incidence%' OR '%case (%' OR '%cases (%'`. For dumps with case-count surveillance data (dengue, SARI, malaria, cholera, etc — DHIS2's NCLE / IDSR programs). Shows total case records, total cases reported, top case indicators, time series, and by-province distribution.

## How the seeding works

The whole dashboard set is defined declaratively in `superset/seed_dashboard.py`. Each dashboard is a dict with a title, slug, list of charts (each chart specifies its viz type, metric, groupby, and optional SQL filter), and a layout (12-column grid). On every `make run-full`, the `superset-seed` sidecar:

1. Waits for the `superset` web service to become healthy (health-check on `/health`)
2. Logs in as `admin/admin` via the Superset REST API
3. Upserts the `dhis2_aggregate` virtual dataset
4. Upserts every chart in the registry (about 25 charts across the four dashboards)
5. Upserts every dashboard with its grid layout
6. Attaches the charts to their parent dashboards

It's idempotent: re-running updates the in-place objects, never duplicates them. So if you `make run-full` again with the same seed script, nothing changes. If you edit the seed script, the next `make run-full` reconciles the changes.

You can also run the seeder manually from the host without restarting the stack:

```bash
uv run python superset/seed_dashboard.py
```

This is the fast iteration loop: edit the script, re-run, refresh the dashboard in the browser.

## Adding your own charts and dashboards

Two paths.

### Path 1: edit the seed script

Open `superset/seed_dashboard.py` and find the `build_dashboards()` function. Each dashboard is a dict in the returned list. Copy one and adjust:

```python
{
    "title": "DHIS2 Maternal Health",
    "slug": "dhis2-maternal-health",
    "charts": [
        ("m_anc1", "ANC 1st Visit", "big_number_total",
         big_number_params(
             ds_id,
             metric_sum("value", "visits"),
             "first antenatal visit count",
             "dataelement ILIKE '%anc 1%' OR dataelement ILIKE '%anc1%'",
         )),
        # ... more charts ...
    ],
    "layout": [
        [("m_anc1", 12, 50)],
    ],
},
```

Filter expressions go in the last positional argument of each chart-param builder. They are raw SQL fragments that Superset puts in the `WHERE` clause via an `adhoc_filters` entry.

Then re-run the seeder:

```bash
uv run python superset/seed_dashboard.py
```

Refresh the browser. Your new dashboard appears under `/superset/dashboard/dhis2-maternal-health/`.

### Path 2: build it in the UI, then forget the seed script

Superset's UI is fully usable for ad-hoc work. Make a chart in **Charts → + Chart**, save it, then add it to a dashboard via **Dashboards → + Dashboard**. The catch is that anything you build this way **lives only in the `superset_db` volume** and is wiped by the next `make run-full` (which does `down -v`). So this path is fine for exploration but if you want it permanent, port it back into `seed_dashboard.py`.

If you want to preserve UI-built dashboards across `down -v`, export them via Superset's built-in YAML export (`Dashboards → ... → Export`) and commit the result somewhere — or import them back via the Superset import API in a follow-up sidecar.

## SQL Lab and writing queries directly

The `analytics.md` document in the repo root walks through the DHIS2 analytics schema in detail and includes ~8 useful example queries (dengue trend, PM2.5 spikes, province climatology, reporting-gap detection, etc). All of those queries paste straight into Superset's **SQL Lab** with the `DHIS2` database picked from the dropdown — no setup required.

To get there: top menu → **SQL → SQL Lab**, pick `DHIS2` from the database dropdown, pick `public` as the schema, paste your query, hit **Run**. Save interesting results as datasets if you want to chart them later.

## Common gotchas

**Dashboards show "No results"** — your dump probably doesn't have data matching the dashboard's `ILIKE` filter. The dashboard itself is fine; it's just a query that found nothing. Check **SQL Lab** to confirm: `SELECT DISTINCT dataelement FROM dhis2_aggregate WHERE dataelement ILIKE '%temperature%';`. If that returns 0 rows, your dump has no temperature data and the climate dashboard will be empty until you swap dumps.

**`make run-full` says "service superset-init didn't complete successfully"** — this almost always means Superset's metadata database (`superset-db`) wasn't ready or got into a half-initialized state from an earlier failed run. Fix:

```bash
make down
docker volume rm dhis2-docker_superset_db
make run-full
```

**Charts show but the time series is blank** — Superset's time-series charts need a properly typed datetime column on the X axis. The seed script uses `period_start` (a `date`) which should always work. If you build a chart in the UI against a column that Superset doesn't recognize as a time dimension, mark it as one in the dataset's column metadata.

**429 Too Many Requests during seeding** — Superset's flask-limiter is per-IP and trips fast under bursts of API writes. The seed script handles this with retry-and-backoff (`_retry()` helper in `seed_dashboard.py`). If you see 429s in your own scripts, copy that pattern.

**"Database is not allowed for SQL Lab"** — when adding a database manually through the UI, the **Expose in SQL Lab** checkbox is off by default. The seed script flips it on for you (`expose_in_sqllab=True`), so any database registered through the script is immediately usable in SQL Lab.

## What this is *not*

- **Not a DHIS2 production replacement.** The Superset stack here ships with `admin/admin`, no TLS, no auth hardening, and a known dev secret key. It is strictly for local exploration. Do not put this on a network anyone else can reach.
- **Not real-time.** Queries hit the DHIS2 postgres directly, but the `analytics_*` tables are only as fresh as the last run of DHIS2's "Generate Analytics Tables" job (triggered automatically by `analytics-trigger` after every `make run` / `make run-full`). For up-to-the-minute live data you'd query the raw `datavalue` / `programstageinstance` tables instead — slower but live.
- **Not ClickHouse-backed (yet).** The DHIS2 community is moving toward `dhis2 → CDC via wal2json → ClickHouse → Superset` for big-data scenarios. We already ship `wal2json` in the postgres image, so the first half of that pipeline is in place — but adding the ClickHouse + CDC consumer side is a future project.

## Reference

- Config file: [`superset/superset_config.py`](superset/superset_config.py) — minimal Python config that reads env vars
- Seed script: [`superset/seed_dashboard.py`](superset/seed_dashboard.py) — declarative dashboard registry, run via `uv run python superset/seed_dashboard.py`
- Custom image: [`Dockerfile.superset`](Dockerfile.superset) — `apache/superset:4.1.1` + `psycopg2-binary` + `httpx`
- Compose overlay: [`compose.superset.yml`](compose.superset.yml) — 5 services (db, redis, init, web, seed)
- Analytics schema reference: [`analytics.md`](analytics.md) — what every `analytics_*` table contains, with example queries
