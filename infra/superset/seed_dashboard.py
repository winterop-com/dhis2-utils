"""Seed a portfolio of generic Superset dashboards against any DHIS2 instance.

Builds:
- One virtual dataset (`dhis2_aggregate`) joining the universal `analytics`
  parent table with `analytics_rs_dataelementstructure` and
  `analytics_rs_orgunitstructure` for friendly column names. Works on any
  DHIS2 dump because it never references program- or DE-specific UIDs.
- Multiple dashboards, each defined declaratively in DASHBOARDS below.
  Each dashboard filters by data element name patterns (ILIKE) instead of
  UIDs, so it auto-populates against any dump that happens to have matching
  data and gracefully shows zero rows on dumps that do not.
- Charts are recreated on every run; the dashboard's position layout is
  rebuilt from the chart specs.

Idempotent: re-running updates the in-place objects rather than duplicating.

Run from the host with the project's uv venv:
    uv run python superset/seed_dashboard.py

Or automatically as the `superset-seed` sidecar in compose.superset.yml.
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import time
from collections.abc import Callable
from typing import Any

import httpx

VIEWS_SQL_PATH = pathlib.Path(__file__).parent / "views.sql"
DHIS2_POSTGRES_DSN = os.environ.get(
    "DHIS2_POSTGRES_DSN",
    "postgresql://dhis:dhis@postgresql:5432/dhis",
)
DHIS2_POSTGRES_CONTAINER = os.environ.get("DHIS2_POSTGRES_CONTAINER", "dhis2-docker-postgresql-1")


def apply_views_sql(sql_path: pathlib.Path) -> None:
    """Apply views.sql to the DHIS2 postgres.

    Tries psycopg2 first (for in-container or accessible-postgres setups),
    then falls back to `docker exec ... psql -f -` for the host-side
    workflow where postgres is not exposed on a port.
    """
    sql = sql_path.read_text()
    try:
        import psycopg2  # type: ignore
    except ImportError:
        psycopg2 = None  # type: ignore

    if psycopg2 is not None:
        try:
            conn = psycopg2.connect(DHIS2_POSTGRES_DSN, connect_timeout=3)
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.close()
            print(f"  applied {sql_path.name} via psycopg2 (DSN={DHIS2_POSTGRES_DSN.split('@')[-1]})")
            return
        except Exception as exc:
            print(f"  psycopg2 path failed ({exc.__class__.__name__}: {exc}), trying docker exec")

    # Fallback: pipe through docker exec psql
    proc = subprocess.run(
        [
            "docker",
            "exec",
            "-i",
            DHIS2_POSTGRES_CONTAINER,
            "psql",
            "-U",
            "dhis",
            "-d",
            "dhis",
            "-v",
            "ON_ERROR_STOP=1",
            "-q",
        ],
        input=sql,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        raise RuntimeError(f"docker exec psql failed (rc={proc.returncode}). Is the container running?")
    print(f"  applied {sql_path.name} via docker exec ({DHIS2_POSTGRES_CONTAINER})")


def _retry(
    method: Callable[..., httpx.Response],
    *args: Any,
    **kwargs: Any,
) -> httpx.Response:
    """Wrap a httpx request method with retry-on-429 + exponential backoff.

    Superset's default flask-limiter is per-IP and trips fast when you POST
    or PUT 20+ times in a row. We sleep and retry on 429 instead of erroring.
    """
    delay = 0.5
    response = method(*args, **kwargs)
    for _ in range(6):
        if response.status_code != 429:
            return response
        time.sleep(delay)
        delay = min(delay * 2, 8.0)
        response = method(*args, **kwargs)
    return response


BASE = os.environ.get("SUPERSET_BASE", "http://localhost:8088")
USER = os.environ.get("SUPERSET_USER", "admin")
PASSWORD = os.environ.get("SUPERSET_PASSWORD", "admin")
DATASET_NAME = "dhis2_aggregate"
# (table_name, main_dttm_col) — main_dttm_col is what the dashboard-level
# time filter binds to. Each live view exposes a "primary" datetime column
# (when the event happened, when the value was last updated, etc).
LIVE_DATASETS = [
    ("v_live_datavalue", "lastupdated"),
    ("v_live_event", "occurreddate"),
    ("v_live_enrollment", "enrollmentdate"),
    ("v_live_trackedentity", "lastupdated"),
]

POPULATION_MAP_SQL = """SELECT
  geo.ou_uid,
  geo.orgunit                      AS province,
  COALESCE(d.population, 0)        AS population,
  jsonb_set(
    geo.geojson::jsonb,
    '{properties}',
    (geo.geojson::jsonb -> 'properties') || jsonb_build_object(
      'population', COALESCE(d.population, 0),
      'province',   geo.orgunit,
      'fillColor',  jsonb_build_array(
        LEAST(255, ROUND(255 * COALESCE(d.population, 0)::numeric
                             / GREATEST(max_val.v, 1))),
        GREATEST(0, ROUND(120 * (1 - COALESCE(d.population, 0)::numeric
                                     / GREATEST(max_val.v, 1)))),
        30,
        200
      )
    )
  )::text                          AS geojson
FROM v_orgunit_geojson geo
CROSS JOIN (
  SELECT MAX(sub.population) AS v
  FROM (
    SELECT ou.uidlevel2 AS prov_uid,
           ROUND(SUM(a.value)::numeric, 0) AS population
    FROM analytics a
    JOIN analytics_rs_dataelementstructure des ON des.dataelementuid = a.dx
    JOIN analytics_rs_orgunitstructure ou      ON ou.organisationunituid = a.ou
    WHERE des.dataelementname ILIKE '%population%'
    GROUP BY ou.uidlevel2
  ) sub
) max_val
LEFT JOIN (
  SELECT
    ou.uidlevel2                       AS prov_uid,
    ROUND(SUM(a.value)::numeric, 0)    AS population
  FROM analytics a
  JOIN analytics_rs_dataelementstructure des ON des.dataelementuid = a.dx
  JOIN analytics_rs_orgunitstructure ou     ON ou.organisationunituid = a.ou
  WHERE des.dataelementname ILIKE '%population%'
  GROUP BY ou.uidlevel2
) d ON d.prov_uid = geo.ou_uid
WHERE geo.ou_level = 2"""

DATASET_SQL = """SELECT
  a.dx AS dataelement_uid,
  COALESCE(des.dataelementname, a.dx) AS dataelement,
  des.valuetype,
  des.aggregationtype,
  des.datasetname AS dataset,
  a.pe AS period_iso,
  a.pestartdate AS period_start,
  a.peenddate AS period_end,
  a.petype AS period_type,
  a.year,
  a.ou AS ou_uid,
  COALESCE(ou.name, a.ou) AS orgunit,
  ou.namelevel1 AS country,
  ou.namelevel2 AS province,
  ou.namelevel3 AS district,
  ou.namelevel4 AS facility,
  ou.namelevel5 AS village,
  ou.level AS ou_level,
  a.value,
  a.textvalue
FROM analytics a
LEFT JOIN analytics_rs_dataelementstructure des ON des.dataelementuid = a.dx
LEFT JOIN analytics_rs_orgunitstructure ou ON ou.organisationunituid = a.ou"""


# ---------------------------------------------------------------------------
# Superset client
# ---------------------------------------------------------------------------


class Superset:
    def __init__(self, base: str, user: str, password: str) -> None:
        self.base = base.rstrip("/")
        self.client = httpx.Client(base_url=self.base, timeout=30.0, follow_redirects=True)
        self._login(user, password)
        # Cache the lists once so we do not hit the per-IP rate limit when
        # processing many charts in a row.
        self._chart_cache: dict[str, dict[str, Any]] | None = None
        self._dataset_cache: dict[str, dict[str, Any]] | None = None
        self._dashboard_cache: dict[str, dict[str, Any]] | None = None

    def _refresh_chart_cache(self) -> None:
        r = self.client.get("/api/v1/chart/?q=(page_size:500)")
        r.raise_for_status()
        self._chart_cache = {row["slice_name"]: row for row in r.json().get("result", [])}

    def _refresh_dataset_cache(self) -> None:
        r = self.client.get("/api/v1/dataset/?q=(page_size:500)")
        r.raise_for_status()
        self._dataset_cache = {row["table_name"]: row for row in r.json().get("result", [])}

    def _refresh_dashboard_cache(self) -> None:
        r = self.client.get("/api/v1/dashboard/?q=(page_size:500)")
        r.raise_for_status()
        self._dashboard_cache = {row["slug"]: row for row in r.json().get("result", []) if row.get("slug")}

    def _login(self, user: str, password: str) -> None:
        r = self.client.post(
            "/api/v1/security/login",
            json={"username": user, "password": password, "provider": "db", "refresh": True},
        )
        r.raise_for_status()
        token = r.json()["access_token"]
        self.client.headers["Authorization"] = f"Bearer {token}"
        r = self.client.get("/api/v1/security/csrf_token/")
        r.raise_for_status()
        self.client.headers["X-CSRFToken"] = r.json()["result"]
        self.client.headers["Referer"] = self.base + "/"

    def db_id(self, name: str) -> int:
        r = self.client.get("/api/v1/database/?q=(page_size:100)")
        r.raise_for_status()
        for row in r.json()["result"]:
            if row["database_name"] == name:
                return row["id"]
        raise RuntimeError(f"database {name!r} not found in Superset")

    # ----- datasets ------------------------------------------------------

    def get_dataset(self, table_name: str) -> dict[str, Any] | None:
        if self._dataset_cache is None:
            self._refresh_dataset_cache()
        return (self._dataset_cache or {}).get(table_name)

    def upsert_dataset(
        self,
        *,
        db_id: int,
        table_name: str,
        sql: str | None = None,
        schema: str = "public",
        main_dttm_col: str | None = None,
    ) -> int:
        """Upsert a Superset dataset.

        If `sql` is given, the dataset is virtual (Superset wraps the query
        as a subquery). If `sql` is None, the dataset is physical and points
        at a real table or view named `table_name` in `schema`.

        `main_dttm_col` sets the dataset-level default time column, which is
        what dashboard-level native time filters bind to.
        """
        existing = self.get_dataset(table_name)
        if existing:
            ds_id = existing["id"]
            update_body: dict[str, Any] = {"schema": schema}
            if sql is not None:
                update_body["sql"] = sql
            if main_dttm_col is not None:
                update_body["main_dttm_col"] = main_dttm_col
            r = _retry(self.client.put, f"/api/v1/dataset/{ds_id}", json=update_body)
            r.raise_for_status()
            print(f"  updated dataset {table_name!r} (id={ds_id})")
            return ds_id
        body: dict[str, Any] = {
            "database": db_id,
            "schema": schema,
            "table_name": table_name,
        }
        if sql is not None:
            body["sql"] = sql
        r = _retry(self.client.post, "/api/v1/dataset/", json=body)
        if r.status_code >= 400:
            print(f"  CREATE failed: {r.status_code} {r.text}", file=sys.stderr)
            r.raise_for_status()
        ds_id = r.json()["id"]
        if main_dttm_col is not None:
            r = _retry(
                self.client.put,
                f"/api/v1/dataset/{ds_id}",
                json={"main_dttm_col": main_dttm_col},
            )
            r.raise_for_status()
        print(f"  created dataset {table_name!r} (id={ds_id})")
        return ds_id

    # ----- charts --------------------------------------------------------

    def get_chart(self, slice_name: str) -> dict[str, Any] | None:
        if self._chart_cache is None:
            self._refresh_chart_cache()
        return (self._chart_cache or {}).get(slice_name)

    def upsert_chart(
        self,
        *,
        slice_name: str,
        viz_type: str,
        datasource_id: int,
        params: dict[str, Any],
    ) -> int:
        body = {
            "slice_name": slice_name,
            "viz_type": viz_type,
            "datasource_id": datasource_id,
            "datasource_type": "table",
            "params": json.dumps(params),
        }
        existing = self.get_chart(slice_name)
        if existing:
            chart_id = existing["id"]
            r = _retry(self.client.put, f"/api/v1/chart/{chart_id}", json=body)
            if r.status_code >= 400:
                print(f"  PUT failed: {r.status_code} {r.text}", file=sys.stderr)
                r.raise_for_status()
            return chart_id
        r = _retry(self.client.post, "/api/v1/chart/", json=body)
        if r.status_code >= 400:
            print(f"  POST failed: {r.status_code} {r.text}", file=sys.stderr)
            r.raise_for_status()
        chart_id = r.json()["id"]
        # Update local cache so subsequent get_chart calls in this run see it
        if self._chart_cache is not None:
            self._chart_cache[slice_name] = {"id": chart_id, "slice_name": slice_name}
        return chart_id

    # ----- dashboards ----------------------------------------------------

    def get_dashboard(self, slug: str) -> dict[str, Any] | None:
        if self._dashboard_cache is None:
            self._refresh_dashboard_cache()
        return (self._dashboard_cache or {}).get(slug)

    def upsert_dashboard(
        self,
        *,
        title: str,
        slug: str,
        position_json: dict[str, Any],
        json_metadata: dict[str, Any] | None = None,
    ) -> int:
        body: dict[str, Any] = {
            "dashboard_title": title,
            "slug": slug,
            "published": True,
            "position_json": json.dumps(position_json),
        }
        if json_metadata is not None:
            body["json_metadata"] = json.dumps(json_metadata)
        existing = self.get_dashboard(slug)
        if existing:
            dash_id = existing["id"]
            r = _retry(self.client.put, f"/api/v1/dashboard/{dash_id}", json=body)
            if r.status_code >= 400:
                print(f"  PUT failed: {r.status_code} {r.text}", file=sys.stderr)
                r.raise_for_status()
            return dash_id
        r = _retry(self.client.post, "/api/v1/dashboard/", json=body)
        if r.status_code >= 400:
            print(f"  POST failed: {r.status_code} {r.text}", file=sys.stderr)
            r.raise_for_status()
        return r.json()["id"]


# ---------------------------------------------------------------------------
# Metric and chart-param builders
# ---------------------------------------------------------------------------


def metric_count() -> dict[str, Any]:
    return {
        "label": "rows",
        "expressionType": "SQL",
        "sqlExpression": "COUNT(*)",
        "hasCustomLabel": True,
    }


def metric_count_distinct(col: str, label: str) -> dict[str, Any]:
    return {
        "label": label,
        "expressionType": "SQL",
        "sqlExpression": f"COUNT(DISTINCT {col})",
        "hasCustomLabel": True,
    }


def metric_sum(col: str, label: str) -> dict[str, Any]:
    return {
        "label": label,
        "expressionType": "SQL",
        "sqlExpression": f"SUM({col})",
        "hasCustomLabel": True,
    }


def metric_avg(col: str, label: str) -> dict[str, Any]:
    return {
        "label": label,
        "expressionType": "SQL",
        "sqlExpression": f"AVG({col})",
        "hasCustomLabel": True,
    }


def adhoc_sql(expr: str) -> dict[str, Any]:
    return {
        "expressionType": "SQL",
        "clause": "WHERE",
        "sqlExpression": expr,
    }


def filters_for(dashboard_filter: str | None) -> list[dict[str, Any]]:
    return [adhoc_sql(dashboard_filter)] if dashboard_filter else []


def big_number_params(
    ds_id: int,
    metric: dict[str, Any],
    subheader: str,
    sql_filter: str | None = None,
) -> dict[str, Any]:
    return {
        "datasource": f"{ds_id}__table",
        "viz_type": "big_number_total",
        "metric": metric,
        "adhoc_filters": filters_for(sql_filter),
        "header_font_size": 0.4,
        "subheader_font_size": 0.15,
        "subheader": subheader,
        "y_axis_format": "SMART_NUMBER",
    }


def dist_bar_params(
    ds_id: int,
    groupby: list[str],
    metric: dict[str, Any],
    row_limit: int,
    sql_filter: str | None = None,
) -> dict[str, Any]:
    return {
        "datasource": f"{ds_id}__table",
        "viz_type": "dist_bar",
        "groupby": groupby,
        "metrics": [metric],
        "row_limit": row_limit,
        "order_desc": True,
        "color_scheme": "supersetColors",
        "show_legend": False,
        "adhoc_filters": filters_for(sql_filter),
    }


def pie_params(
    ds_id: int,
    groupby: list[str],
    metric: dict[str, Any],
    sql_filter: str | None = None,
) -> dict[str, Any]:
    return {
        "datasource": f"{ds_id}__table",
        "viz_type": "pie",
        "groupby": groupby,
        "metric": metric,
        "adhoc_filters": filters_for(sql_filter),
        "color_scheme": "supersetColors",
        "donut": True,
        "show_legend": True,
        "label_type": "key_percent",
    }


def table_params(
    ds_id: int,
    groupby: list[str],
    metrics: list[dict[str, Any]],
    row_limit: int,
    sql_filter: str | None = None,
) -> dict[str, Any]:
    return {
        "datasource": f"{ds_id}__table",
        "viz_type": "table",
        "groupby": groupby,
        "metrics": metrics,
        "row_limit": row_limit,
        "order_desc": True,
        "include_search": True,
        "adhoc_filters": filters_for(sql_filter),
    }


def timeseries_bar_params(
    ds_id: int,
    time_col: str,
    metric: dict[str, Any],
    sql_filter: str | None = None,
    time_grain: str = "P1Y",
) -> dict[str, Any]:
    return {
        "datasource": f"{ds_id}__table",
        "viz_type": "echarts_timeseries_bar",
        "x_axis": time_col,
        "metrics": [metric],
        "groupby": [],
        "row_limit": 1000,
        "color_scheme": "supersetColors",
        "show_legend": False,
        "adhoc_filters": filters_for(sql_filter),
        "time_grain_sqla": time_grain,
    }


def timeseries_line_params(
    ds_id: int,
    time_col: str,
    metric: dict[str, Any],
    sql_filter: str | None = None,
    time_grain: str = "P1Y",
    groupby: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "datasource": f"{ds_id}__table",
        "viz_type": "echarts_timeseries_line",
        "x_axis": time_col,
        "metrics": [metric],
        "groupby": groupby or [],
        "row_limit": 5000,
        "color_scheme": "supersetColors",
        "show_legend": True,
        "adhoc_filters": filters_for(sql_filter),
        "time_grain_sqla": time_grain,
    }


def deck_geojson_params(
    ds_id: int,
    geojson_col: str = "geojson",
    tooltip_cols: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "datasource": f"{ds_id}__table",
        "viz_type": "deck_geojson",
        "geojson": geojson_col,
        "row_limit": 10000,
        "mapbox_style": "mapbox://styles/mapbox/light-v9",
        "viewport": {
            "longitude": 0,
            "latitude": 0,
            "zoom": 1,
            "bearing": 0,
            "pitch": 0,
        },
        "autozoom": True,
        "fill_color_picker": {"r": 0, "g": 0, "b": 0, "a": 0},
        "stroke_color_picker": {"r": 255, "g": 255, "b": 255, "a": 1},
        "filled": True,
        "stroked": True,
        "extruded": False,
        "point_radius_fixed": {"type": "fix", "value": 2000},
        "line_width": 1,
        "line_width_unit": "pixels",
        "opacity": 70,
        "reverse_long_lat": False,
        "adhoc_filters": [],
        "js_columns": tooltip_cols or [],
    }


# ---------------------------------------------------------------------------
# Layout builder
# ---------------------------------------------------------------------------


def build_position_json(
    rows: list[list[tuple[str, int, int]]],
    chart_ids: dict[str, int],
    slug: str,
) -> dict[str, Any]:
    """Build a Superset dashboard position_json from a row spec.

    rows is a list of rows; each row is a list of (chart_key, width, height) tuples.
    Widths in a row should sum to 12 (Superset's grid width).
    chart_ids maps each chart_key to its slice id.
    slug is used to namespace row/chart node ids so multiple dashboards do not collide.
    """
    pos: dict[str, Any] = {
        "DASHBOARD_VERSION_KEY": "v2",
        "ROOT_ID": {
            "type": "ROOT",
            "id": "ROOT_ID",
            "children": ["GRID_ID"],
        },
        "GRID_ID": {
            "type": "GRID",
            "id": "GRID_ID",
            "children": [],
            "parents": ["ROOT_ID"],
        },
    }
    for r_idx, row in enumerate(rows):
        row_id = f"ROW-{slug}-{r_idx}"
        pos["GRID_ID"]["children"].append(row_id)
        pos[row_id] = {
            "type": "ROW",
            "id": row_id,
            "children": [],
            "parents": ["ROOT_ID", "GRID_ID"],
            "meta": {"background": "BACKGROUND_TRANSPARENT"},
        }
        for c_idx, (chart_key, width, height) in enumerate(row):
            node_id = f"CHART-{slug}-{r_idx}-{c_idx}"
            pos[row_id]["children"].append(node_id)
            pos[node_id] = {
                "type": "CHART",
                "id": node_id,
                "children": [],
                "parents": ["ROOT_ID", "GRID_ID", row_id],
                "meta": {
                    "width": width,
                    "height": height,
                    "chartId": chart_ids[chart_key],
                },
            }
    return pos


# ---------------------------------------------------------------------------
# Dashboard registry
# ---------------------------------------------------------------------------


# Filters use ILIKE on the friendly `dataelement` name so they auto-populate
# against any DHIS2 dump that happens to have matching data, and produce empty
# (but valid) charts on dumps that do not.
F_CLIMATE = (
    "(dataelement ILIKE '%temperature%' OR dataelement ILIKE '%temp%' "
    "OR dataelement ILIKE '%precipitation%' OR dataelement ILIKE '%rain%' "
    "OR dataelement ILIKE '%humidity%' OR dataelement ILIKE '%climate%')"
)
F_POPULATION = "dataelement ILIKE '%population%'"
F_CASES = (
    "(dataelement ILIKE '%cases%' OR dataelement ILIKE '%incidence%' "
    "OR dataelement ILIKE '%case (%' OR dataelement ILIKE '%cases (%')"
)


def time_range_native_filter() -> dict[str, Any]:
    """Dashboard-wide native filter that lets the user pick a time range.

    Defaults to "No filter" so the dashboard headlines preserve their
    all-time semantics until the user explicitly picks a window. The filter
    binds to each dataset's `main_dttm_col`, so for the live dashboard it
    will use lastupdated / occurreddate / enrollmentdate respectively.
    """
    return {
        "native_filter_configuration": [
            {
                "id": "NATIVE_FILTER-time_range",
                "name": "Time range",
                "filterType": "filter_time",
                "type": "NATIVE_FILTER",
                "scope": {"rootPath": ["ROOT_ID"], "excluded": []},
                "targets": [{}],
                "controlValues": {},
                "cascadeParentIds": [],
                "defaultDataMask": {
                    "extraFormData": {"time_range": "No filter"},
                    "filterState": {"value": "No filter"},
                    "ownState": {},
                },
            }
        ],
        "show_native_filters": True,
        "color_scheme": "supersetColors",
    }


def build_live_dashboard(dv_id: int, ev_id: int, en_id: int) -> dict[str, Any]:
    """Live-data dashboard built on top of v_live_datavalue / v_live_event /
    v_live_enrollment. These query DHIS2's raw transactional tables directly
    instead of the analytics_* materialization, so they are always current.
    """
    return {
        "title": "DHIS2 Live Data",
        "slug": "dhis2-live-data",
        "json_metadata": time_range_native_filter(),
        "charts": [
            (
                "l_dv",
                "Live — Total Data Values",
                "big_number_total",
                big_number_params(dv_id, metric_count(), "rows in datavalue (live)"),
            ),
            (
                "l_ev",
                "Live — Total Events",
                "big_number_total",
                big_number_params(ev_id, metric_count(), "rows in event (live)"),
            ),
            (
                "l_en",
                "Live — Total Enrollments",
                "big_number_total",
                big_number_params(en_id, metric_count(), "rows in enrollment (live)"),
            ),
            (
                "l_dv_year",
                "Live — Data Values per Year",
                "echarts_timeseries_bar",
                timeseries_bar_params(dv_id, "period_start", metric_count()),
            ),
            (
                "l_dv_de",
                "Live — Top 15 Data Elements (live)",
                "dist_bar",
                dist_bar_params(dv_id, ["dataelement"], metric_count(), 15),
            ),
            (
                "l_ev_prog",
                "Live — Events by Program",
                "dist_bar",
                dist_bar_params(ev_id, ["program"], metric_count(), 25),
            ),
            (
                "l_ev_year",
                "Live — Events per Month",
                "echarts_timeseries_bar",
                timeseries_bar_params(ev_id, "occurreddate", metric_count(), time_grain="P1M"),
            ),
            (
                "l_dv_recent",
                "Live — Most Recent Data Value Updates",
                "table",
                table_params(
                    dv_id,
                    ["dataelement", "orgunit"],
                    [
                        {
                            "label": "last_updated",
                            "expressionType": "SQL",
                            "sqlExpression": "MAX(lastupdated)",
                            "hasCustomLabel": True,
                        }
                    ],
                    50,
                ),
            ),
        ],
        "layout": [
            [("l_dv", 4, 50), ("l_ev", 4, 50), ("l_en", 4, 50)],
            [("l_dv_year", 12, 60)],
            [("l_dv_de", 12, 60)],
            [("l_ev_prog", 6, 60), ("l_ev_year", 6, 60)],
            [("l_dv_recent", 12, 60)],
        ],
    }


def build_population_map_dashboard(geo_ds_id: int, agg_ds_id: int) -> dict[str, Any]:
    """Population choropleth map dashboard. Uses the dhis2_population_map
    virtual dataset for the deck_geojson map chart and the main
    dhis2_aggregate dataset for the supporting bar/table charts.
    Generic: works on any DHIS2 instance with population data and org unit
    geometry.
    """
    return {
        "title": "DHIS2 Population Map",
        "slug": "dhis2-population-map",
        "charts": [
            (
                "pm_map",
                "Population -- Province Choropleth",
                "deck_geojson",
                deck_geojson_params(geo_ds_id, tooltip_cols=["province", "population"]),
            ),
            (
                "pm_total",
                "Population -- Reported Total",
                "big_number_total",
                big_number_params(
                    agg_ds_id, metric_sum("value", "people"), "sum of all reported population values", F_POPULATION
                ),
            ),
            (
                "pm_provs",
                "Population -- Provinces Reporting",
                "big_number_total",
                big_number_params(
                    agg_ds_id, metric_count_distinct("province", "provinces"), "distinct provinces", F_POPULATION
                ),
            ),
            (
                "pm_year",
                "Population -- Reported Total by Year",
                "echarts_timeseries_bar",
                timeseries_bar_params(agg_ds_id, "period_start", metric_sum("value", "people"), F_POPULATION),
            ),
            (
                "pm_prov",
                "Population -- Reported Total by Province",
                "dist_bar",
                dist_bar_params(agg_ds_id, ["province"], metric_sum("value", "people"), 20, F_POPULATION),
            ),
            (
                "pm_tbl",
                "Population -- Province x Year",
                "table",
                table_params(agg_ds_id, ["province", "year"], [metric_sum("value", "people")], 100, F_POPULATION),
            ),
        ],
        "layout": [
            [("pm_map", 6, 80), ("pm_total", 3, 40), ("pm_provs", 3, 40)],
            [("pm_year", 6, 60), ("pm_prov", 6, 60)],
            [("pm_tbl", 12, 60)],
        ],
    }


def build_dashboards(ds_id: int) -> list[dict[str, Any]]:
    """Each entry: title, slug, charts (list of (key, name, viz, params)), layout."""
    return [
        # ─── 1. Aggregate Overview ──────────────────────────────────────
        {
            "title": "DHIS2 Aggregate Overview",
            "slug": "dhis2-aggregate-overview",
            "charts": [
                (
                    "o_total",
                    "DHIS2 — Total Data Points",
                    "big_number_total",
                    big_number_params(ds_id, metric_count(), "rows in analytics"),
                ),
                (
                    "o_des",
                    "DHIS2 — Distinct Data Elements",
                    "big_number_total",
                    big_number_params(
                        ds_id, metric_count_distinct("dataelement_uid", "data_elements"), "distinct data elements"
                    ),
                ),
                (
                    "o_ous",
                    "DHIS2 — Distinct Org Units",
                    "big_number_total",
                    big_number_params(
                        ds_id, metric_count_distinct("ou_uid", "org_units"), "distinct org units reporting"
                    ),
                ),
                (
                    "o_topdes",
                    "DHIS2 — Top 10 Data Elements by Volume",
                    "dist_bar",
                    dist_bar_params(ds_id, ["dataelement"], metric_count(), 10),
                ),
                (
                    "o_petype",
                    "DHIS2 — Period Type Distribution",
                    "pie",
                    pie_params(ds_id, ["period_type"], metric_count()),
                ),
                (
                    "o_year",
                    "DHIS2 — Data Points per Year",
                    "echarts_timeseries_bar",
                    timeseries_bar_params(ds_id, "period_start", metric_count()),
                ),
                (
                    "o_prov",
                    "DHIS2 — Province Reporting Volume",
                    "table",
                    table_params(ds_id, ["province"], [metric_count(), metric_avg("value", "avg_value")], 50),
                ),
            ],
            "layout": [
                [("o_total", 4, 50), ("o_des", 4, 50), ("o_ous", 4, 50)],
                [("o_topdes", 8, 60), ("o_petype", 4, 60)],
                [("o_year", 12, 50)],
                [("o_prov", 12, 60)],
            ],
        },
        # ─── 2. Climate ─────────────────────────────────────────────────
        {
            "title": "DHIS2 Climate",
            "slug": "dhis2-climate",
            "charts": [
                (
                    "c_rows",
                    "Climate — Total Readings",
                    "big_number_total",
                    big_number_params(ds_id, metric_count(), "matching readings", F_CLIMATE),
                ),
                (
                    "c_des",
                    "Climate — Distinct Metrics",
                    "big_number_total",
                    big_number_params(
                        ds_id,
                        metric_count_distinct("dataelement_uid", "metrics"),
                        "distinct climate data elements",
                        F_CLIMATE,
                    ),
                ),
                (
                    "c_ous",
                    "Climate — Reporting Locations",
                    "big_number_total",
                    big_number_params(
                        ds_id,
                        metric_count_distinct("ou_uid", "locations"),
                        "org units with climate readings",
                        F_CLIMATE,
                    ),
                ),
                (
                    "c_byde",
                    "Climate — Readings by Metric",
                    "dist_bar",
                    dist_bar_params(ds_id, ["dataelement"], metric_count(), 20, F_CLIMATE),
                ),
                (
                    "c_year",
                    "Climate — Average Value by Year",
                    "echarts_timeseries_line",
                    timeseries_line_params(
                        ds_id, "period_start", metric_avg("value", "avg_value"), F_CLIMATE, "P1Y", ["dataelement"]
                    ),
                ),
                (
                    "c_prov",
                    "Climate — Reading Volume by Province",
                    "table",
                    table_params(
                        ds_id, ["province"], [metric_count(), metric_avg("value", "avg_value")], 30, F_CLIMATE
                    ),
                ),
            ],
            "layout": [
                [("c_rows", 4, 50), ("c_des", 4, 50), ("c_ous", 4, 50)],
                [("c_byde", 12, 60)],
                [("c_year", 12, 60)],
                [("c_prov", 12, 60)],
            ],
        },
        # ─── 3. Population ──────────────────────────────────────────────
        {
            "title": "DHIS2 Population",
            "slug": "dhis2-population",
            "charts": [
                (
                    "p_rows",
                    "Population — Total Records",
                    "big_number_total",
                    big_number_params(ds_id, metric_count(), "matching records", F_POPULATION),
                ),
                (
                    "p_sum",
                    "Population — Reported Total",
                    "big_number_total",
                    big_number_params(
                        ds_id, metric_sum("value", "people"), "sum of all reported population values", F_POPULATION
                    ),
                ),
                (
                    "p_des",
                    "Population — Distinct Indicators",
                    "big_number_total",
                    big_number_params(
                        ds_id,
                        metric_count_distinct("dataelement_uid", "indicators"),
                        "distinct population data elements",
                        F_POPULATION,
                    ),
                ),
                (
                    "p_year",
                    "Population — Reported Total by Year",
                    "echarts_timeseries_bar",
                    timeseries_bar_params(ds_id, "period_start", metric_sum("value", "people"), F_POPULATION),
                ),
                (
                    "p_prov",
                    "Population — Reported Total by Province",
                    "dist_bar",
                    dist_bar_params(ds_id, ["province"], metric_sum("value", "people"), 25, F_POPULATION),
                ),
                (
                    "p_tbl",
                    "Population — By Province and Year",
                    "table",
                    table_params(ds_id, ["province", "year"], [metric_sum("value", "people")], 100, F_POPULATION),
                ),
            ],
            "layout": [
                [("p_rows", 4, 50), ("p_sum", 4, 50), ("p_des", 4, 50)],
                [("p_year", 12, 60)],
                [("p_prov", 12, 60)],
                [("p_tbl", 12, 60)],
            ],
        },
        # ─── 4. Disease Surveillance ────────────────────────────────────
        {
            "title": "DHIS2 Disease Surveillance",
            "slug": "dhis2-disease-surveillance",
            "charts": [
                (
                    "d_rows",
                    "Disease — Total Case Records",
                    "big_number_total",
                    big_number_params(ds_id, metric_count(), "matching records", F_CASES),
                ),
                (
                    "d_sum",
                    "Disease — Total Cases Reported",
                    "big_number_total",
                    big_number_params(ds_id, metric_sum("value", "cases"), "sum of reported case counts", F_CASES),
                ),
                (
                    "d_des",
                    "Disease — Distinct Case Indicators",
                    "big_number_total",
                    big_number_params(
                        ds_id,
                        metric_count_distinct("dataelement_uid", "indicators"),
                        "distinct case-count data elements",
                        F_CASES,
                    ),
                ),
                (
                    "d_byde",
                    "Disease — Top Case Indicators",
                    "dist_bar",
                    dist_bar_params(ds_id, ["dataelement"], metric_sum("value", "cases"), 15, F_CASES),
                ),
                (
                    "d_year",
                    "Disease — Cases per Year",
                    "echarts_timeseries_bar",
                    timeseries_bar_params(ds_id, "period_start", metric_sum("value", "cases"), F_CASES),
                ),
                (
                    "d_prov",
                    "Disease — Cases by Province",
                    "dist_bar",
                    dist_bar_params(ds_id, ["province"], metric_sum("value", "cases"), 25, F_CASES),
                ),
            ],
            "layout": [
                [("d_rows", 4, 50), ("d_sum", 4, 50), ("d_des", 4, 50)],
                [("d_byde", 12, 60)],
                [("d_year", 12, 60)],
                [("d_prov", 12, 60)],
            ],
        },
    ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    print(f"Connecting to Superset at {BASE} as {USER!r}")
    sup = Superset(BASE, USER, PASSWORD)
    db_id = sup.db_id("DHIS2")
    print(f"DHIS2 database id: {db_id}")

    print("\n[1] Live SQL views in DHIS2 postgres")
    apply_views_sql(VIEWS_SQL_PATH)

    print("\n[2] Datasets")
    ds_id = sup.upsert_dataset(db_id=db_id, table_name=DATASET_NAME, sql=DATASET_SQL)
    live_ids: dict[str, int] = {}
    for table_name, dttm_col in LIVE_DATASETS:
        live_ids[table_name] = sup.upsert_dataset(
            db_id=db_id,
            table_name=table_name,
            sql=None,
            main_dttm_col=dttm_col,
        )

    # Population map dataset (virtual, joins population with GeoJSON geometry)
    pop_geo_ds_id = sup.upsert_dataset(db_id=db_id, table_name="dhis2_population_map", sql=POPULATION_MAP_SQL)

    # Build the live-data dashboard now that we have its dataset ids.
    live_dashboard = build_live_dashboard(
        dv_id=live_ids["v_live_datavalue"],
        ev_id=live_ids["v_live_event"],
        en_id=live_ids["v_live_enrollment"],
    )
    population_map_dashboard = build_population_map_dashboard(
        geo_ds_id=pop_geo_ds_id,
        agg_ds_id=ds_id,
    )
    dashboards = build_dashboards(ds_id) + [live_dashboard, population_map_dashboard]
    print(f"\n[3] Charts and dashboards ({len(dashboards)} dashboards)")

    for dash in dashboards:
        print(f"\n  --- {dash['title']} ({dash['slug']}) ---")
        chart_ids: dict[str, int] = {}
        for key, name, viz, params in dash["charts"]:
            # Each chart's params["datasource"] is "<id>__table"; use that
            # as the source of truth so different charts in the same dashboard
            # can target different datasets.
            chart_ds_id = int(params["datasource"].split("__")[0])
            chart_ids[key] = sup.upsert_chart(
                slice_name=name,
                viz_type=viz,
                datasource_id=chart_ds_id,
                params=params,
            )
            print(f"    chart {name!r} (id={chart_ids[key]})")

        position = build_position_json(dash["layout"], chart_ids, dash["slug"])
        dash_id = sup.upsert_dashboard(
            title=dash["title"],
            slug=dash["slug"],
            position_json=position,
            json_metadata=dash.get("json_metadata"),
        )
        print(f"    dashboard (id={dash_id})")

        # Attach the charts to this dashboard so they show up in chart filters
        for chart_id in chart_ids.values():
            _retry(sup.client.put, f"/api/v1/chart/{chart_id}", json={"dashboards": [dash_id]})

    print("\nOK — dashboards created. Open:")
    for dash in dashboards:
        print(f"  http://localhost:8088/superset/dashboard/{dash['slug']}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
