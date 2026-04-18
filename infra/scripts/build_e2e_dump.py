"""Build the committed e2e DHIS2 dump against a fresh-bootstrapped instance.

Usage (from repo root): `make dhis2-build-e2e-dump` — brings up an empty DHIS2,
runs this script to populate metadata + monthly data 2015-2025 + the standard
OAuth2 client + admin openId mapping, triggers analytics, and pg_dump's the
result into `infra/dhis.sql.gz`.

Deterministic everywhere that matters: UIDs, org unit structure, data-element
codes, OAuth2 client id/secret. The only per-run randomness is the data values
themselves (seeded RNG, so they're also reproducible) and BCrypt's salt on the
client secret (same plaintext verifies regardless).

Produces a dump small enough (~1–3 MB gzipped) to commit next to the compose
file, so `make dhis2-up` on a fresh clone gives you a ready-to-login DHIS2
with realistic analytics data.
"""

from __future__ import annotations

import argparse
import asyncio
import gzip
import random
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dhis2_client import BasicAuth, Dhis2Client  # noqa: E402 — path-prepend above is intentional
from pydantic import BaseModel, ConfigDict  # noqa: E402
from seed_auth import ensure_user_openid_mapping, upsert_oauth2_client, wait_for_ready  # noqa: E402

# ---------------------------------------------------------------------------
# Deterministic identifiers
# ---------------------------------------------------------------------------


class OrgUnitSpec(BaseModel):
    """Deterministic identifiers for a seeded org unit."""

    model_config = ConfigDict(frozen=True)

    uid: str
    code: str
    name: str


class DataElementSpec(BaseModel):
    """Deterministic identifiers for a seeded data element."""

    model_config = ConfigDict(frozen=True)

    uid: str
    code: str
    name: str


# DHIS2 UIDs are 11 chars, [A-Za-z][A-Za-z0-9]{10}. Human-readable so it's
# obvious in the UI / logs what these refer to. Org-unit hierarchy is:
#
#   Norway
#   ├── Oslo
#   ├── Vestland
#   ├── Trøndelag
#   └── Nordland
#
# A small, real-world tree gives the analytics dashboards something
# recognisable to aggregate — better for manual smoke-testing than a
# synthetic "District 1/2/3" setup.
OU_ROOT_UID = "NORNorway01"

# One spec per fylke. UIDs stay ASCII; names can carry Norwegian chars.
PROVINCES: list[OrgUnitSpec] = [
    OrgUnitSpec(uid="NOROsloProv", code="NOR_OSLO", name="Oslo"),
    OrgUnitSpec(uid="NORVestland", code="NOR_VESTLAND", name="Vestland"),
    OrgUnitSpec(uid="NORTrondlag", code="NOR_TRONDELAG", name="Trøndelag"),
    OrgUnitSpec(uid="NORNordland", code="NOR_NORDLAND", name="Nordland"),
]
OU_PROVINCE_UIDS = [p.uid for p in PROVINCES]

DS_UID = "NORMonthDS1"


# 7 data elements — the maternal/child health set gives realistic seasonal
# variation when the analytics tables render. DHIS2 UIDs must match
# `[A-Za-z][A-Za-z0-9]{10}` — 11 chars, no underscores, no hyphens.
# (Learned the hard way: `DE_ANC01vst` fails with E4014 Invalid UID.)
DATA_ELEMENTS: list[DataElementSpec] = [
    DataElementSpec(uid="DEancVisit1", code="ANC1ST", name="ANC 1st visit"),
    DataElementSpec(uid="DEancVisit4", code="ANC4TH", name="ANC 4th visit"),
    DataElementSpec(uid="DEdelFacilt", code="DELFAC", name="Deliveries in facility"),
    DataElementSpec(uid="DEliveBirth", code="BIRTH", name="Live births"),
    DataElementSpec(uid="DEbcgVaccin", code="VACBCG", name="Child vaccinations (BCG)"),
    DataElementSpec(uid="DEmesVaccin", code="VACMES", name="Child vaccinations (measles)"),
    DataElementSpec(uid="DEopdConsul", code="OPD", name="OPD consultations (total)"),
]

START_YEAR = 2015
END_YEAR = 2025  # inclusive

# Where to write the gzipped dump
DUMP_PATH = Path(__file__).resolve().parents[1] / "dhis.sql.gz"

# Matches the compose project's auto-generated postgres container name.
POSTGRES_CONTAINER_DEFAULT = "dhis2-docker-postgresql-1"


# ---------------------------------------------------------------------------
# Metadata + data population
# ---------------------------------------------------------------------------


async def resolve_default_category_combo(client: Dhis2Client) -> str:
    """Return the UID of DHIS2's built-in `default` category combo.

    DHIS2's Flyway migrations always seed a category combo named `default`;
    every aggregate data element and dataset must reference it when no
    disaggregation is needed.
    """
    response = await client.get_raw(
        "/api/categoryCombos",
        params={"filter": "name:eq:default", "fields": "id"},
    )
    items = response.get("categoryCombos", [])
    if not items:
        raise RuntimeError("no 'default' category combo found — DHIS2 may not be fully bootstrapped yet")
    return str(items[0]["id"])


async def create_org_units(client: Dhis2Client) -> None:
    """Create the 2-level org unit tree: Norway → 4 fylker (Oslo, Vestland, Trøndelag, Nordland)."""
    org_units: list[dict[str, Any]] = [
        {
            "id": OU_ROOT_UID,
            "code": "NOR",
            "name": "Norway",
            "shortName": "Norway",
            "openingDate": "2000-01-01",
        },
    ]
    for spec in PROVINCES:
        org_units.append(
            {
                "id": spec.uid,
                "code": spec.code,
                "name": spec.name,
                "shortName": spec.name,
                "openingDate": "2000-01-01",
                "parent": {"id": OU_ROOT_UID},
            }
        )
    payload = {"organisationUnits": org_units}
    await client.post_raw("/api/metadata", payload)
    print(f"    created {len(org_units)} org units (Norway + {len(PROVINCES)} fylker)")


async def create_data_elements(client: Dhis2Client, category_combo_uid: str) -> None:
    """Create the 7 monthly aggregate data elements."""
    data_elements: list[dict[str, Any]] = [
        {
            "id": spec.uid,
            "code": spec.code,
            "name": spec.name,
            "shortName": spec.code,
            "domainType": "AGGREGATE",
            "valueType": "INTEGER_ZERO_OR_POSITIVE",
            "aggregationType": "SUM",
            "categoryCombo": {"id": category_combo_uid},
        }
        for spec in DATA_ELEMENTS
    ]
    await client.post_raw("/api/metadata", {"dataElements": data_elements})
    print(f"    created {len(data_elements)} data elements")


async def create_dataset(client: Dhis2Client, category_combo_uid: str) -> None:
    """Create a Monthly dataset holding all data elements and assigned to all districts."""
    data_set = {
        "id": DS_UID,
        "code": "NOR_MONTHLY_DS",
        "name": "Norway Monthly Indicators",
        "shortName": "Norway Monthly",
        "periodType": "Monthly",
        "categoryCombo": {"id": category_combo_uid},
        "dataSetElements": [{"dataElement": {"id": spec.uid}, "dataSet": {"id": DS_UID}} for spec in DATA_ELEMENTS],
        "organisationUnits": [{"id": uid} for uid in OU_PROVINCE_UIDS],
        "openFuturePeriods": 0,
        "timelyDays": 15,
    }
    await client.post_raw("/api/metadata", {"dataSets": [data_set]})
    print(f"    created dataset {DS_UID}")


async def assign_admin_capture_scope(client: Dhis2Client) -> None:
    """Attach the 3 districts to admin's organisationUnits so admin has capture scope."""
    me = await client.get_raw("/api/me", params={"fields": "id"})
    admin_uid = me["id"]
    await client.patch_raw(
        f"/api/users/{admin_uid}",
        [
            {
                "op": "add",
                "path": "/organisationUnits",
                "value": [{"id": uid} for uid in OU_PROVINCE_UIDS],
            }
        ],
    )
    print(f"    assigned {len(OU_PROVINCE_UIDS)} fylker to admin capture scope")


def generate_data_values(seed: int = 42) -> list[dict[str, Any]]:
    """Produce deterministic monthly values for every (district × data-element × period).

    Numbers are randomised within realistic bounds so analytics aggregations
    produce varied charts — but seeded so rebuilds are byte-reproducible.
    """
    rng = random.Random(seed)
    periods = [f"{year}{month:02d}" for year in range(START_YEAR, END_YEAR + 1) for month in range(1, 13)]
    values: list[dict[str, Any]] = []
    for ou_uid in OU_PROVINCE_UIDS:
        for de_spec in DATA_ELEMENTS:
            base = rng.randint(50, 400)
            trend = rng.uniform(0.98, 1.03)
            level = float(base)
            for period in periods:
                noise = rng.randint(-25, 40)
                value = max(0, int(level + noise))
                values.append(
                    {
                        "dataElement": de_spec.uid,
                        "period": period,
                        "orgUnit": ou_uid,
                        "value": str(value),
                    }
                )
                level *= trend
    return values


async def upload_data_values(client: Dhis2Client, values: list[dict[str, Any]], chunk_size: int = 2000) -> None:
    """POST data values in chunks so the payload stays small and errors are localised."""
    total = len(values)
    print(f"    uploading {total} data values in chunks of {chunk_size}")
    for start in range(0, total, chunk_size):
        chunk = values[start : start + chunk_size]
        response = await client.post_raw("/api/dataValueSets", {"dataValues": chunk})
        status = response.get("status")
        if status not in (None, "SUCCESS", "OK"):
            raise RuntimeError(f"dataValueSets import failed: {response}")
    print(f"    uploaded {total} values")


def run_analytics(analytics_container: str = "analytics-trigger") -> None:
    """Trigger analytics by restarting the compose's `analytics-trigger` sidecar and waiting for it to exit.

    The sidecar already POSTs `/api/resourceTables/analytics` and polls the
    resulting task until it reports completion — reusing it means we don't
    re-implement the retry/poll logic (and we inherit the memory-aware
    waiting behaviour tuned for DHIS2). The sidecar runs once on stack-up
    against an empty DB (no-op), so we restart it explicitly after loading
    data and block until it exits.
    """
    print(f"    restarting {analytics_container} to populate analytics tables")
    subprocess.run(["docker", "restart", analytics_container], check=True, capture_output=True)
    print("    waiting for analytics task to finish (docker wait)...")
    result = subprocess.run(
        ["docker", "wait", analytics_container],
        check=True,
        capture_output=True,
        text=True,
    )
    exit_code = int(result.stdout.strip() or "1")
    if exit_code != 0:
        logs = subprocess.run(
            ["docker", "logs", "--tail", "50", analytics_container],
            capture_output=True,
            text=True,
            check=False,
        ).stdout
        raise RuntimeError(f"analytics-trigger exited with {exit_code}:\n{logs}")
    print("    analytics tables populated")


# ---------------------------------------------------------------------------
# DB dump
# ---------------------------------------------------------------------------


def pg_dump(container: str, output: Path, *, postgres_user: str, postgres_db: str) -> None:
    """Run `pg_dump | gzip` via `docker exec` and write the result to `output`.

    Skips the derived `analytics_*` and `_*` materialised-table families — they're
    regenerable from base metadata + data values by `analytics-trigger` on
    restore, and they roughly triple the compressed dump size for no benefit.
    """
    print(f">>> Dumping database to {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "docker",
        "exec",
        container,
        "pg_dump",
        "--no-owner",
        "--no-privileges",
        "--no-sync",  # skip fsync — we're dumping an already-durable state
        "--clean",
        "--if-exists",
        # Skip every family of derived/materialised table — they're all
        # regenerated by `analytics-trigger` on restore in a few seconds,
        # and they roughly triple the compressed dump size otherwise.
        "--exclude-table=analytics_*",
        "--exclude-table=aggregated_*",
        "--exclude-table=completeness_*",
        "--exclude-table=_*",  # DHIS2 resource/periodstructure caches etc.
        "-U",
        postgres_user,
        "-d",
        postgres_db,
    ]
    with output.open("wb") as gz_handle, gzip.GzipFile(fileobj=gz_handle, mode="wb", compresslevel=9) as gz:
        proc = subprocess.run(cmd, check=True, capture_output=True)
        gz.write(proc.stdout)
    size = output.stat().st_size
    print(f">>> Wrote {size:,} bytes to {output}")


def detect_postgres_container(default: str) -> str:
    """Return the running postgres container name, falling back to `default`."""
    if shutil.which("docker") is None:
        raise RuntimeError("`docker` CLI not found — need it for pg_dump")
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
        check=True,
    )
    names = [line.strip() for line in result.stdout.splitlines()]
    candidates = [n for n in names if "postgres" in n.lower()]
    if default in names:
        return default
    if len(candidates) == 1:
        return candidates[0]
    if candidates:
        print(f"!!! multiple postgres containers found: {candidates}; defaulting to {candidates[0]}")
        return candidates[0]
    raise RuntimeError(f"no running postgres container detected; expected {default!r}")


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


async def build(url: str, username: str, password: str, output: Path, container: str) -> None:
    """End-to-end: populate DHIS2 → seed auth → dump."""
    print(f">>> Waiting for DHIS2 at {url}")
    await wait_for_ready(url, username, password)
    async with Dhis2Client(url, BasicAuth(username=username, password=password)) as client:
        info = await client.system.info()
        print(f">>> Connected to DHIS2 {info.version} as {username}")

        print(">>> Resolving default category combo")
        cc_uid = await resolve_default_category_combo(client)

        print(">>> Creating metadata")
        await create_org_units(client)
        await create_data_elements(client, cc_uid)
        await create_dataset(client, cc_uid)
        await assign_admin_capture_scope(client)

        print(">>> Generating data values")
        values = generate_data_values()

        print(">>> Uploading data values")
        await upload_data_values(client, values)

        print(">>> Running analytics")
        run_analytics()

        print(">>> Seeding OAuth2 client + admin openId mapping")
        await upsert_oauth2_client(client)
        await ensure_user_openid_mapping(client, username)

    pg_dump(container, output, postgres_user="dhis", postgres_db="dhis")


def main() -> int:
    """Parse args and run the build."""
    parser = argparse.ArgumentParser(description="Populate a fresh DHIS2 and dump it to infra/dhis.sql.gz.")
    parser.add_argument("--url", default="http://localhost:8080")
    parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="district")
    parser.add_argument("--output", default=str(DUMP_PATH), help="where to write the gzipped dump")
    parser.add_argument(
        "--container",
        default=POSTGRES_CONTAINER_DEFAULT,
        help="name of the running postgres container (auto-detected if not found)",
    )
    args = parser.parse_args()

    output_path = Path(args.output).resolve()
    container = detect_postgres_container(args.container)

    try:
        asyncio.run(build(args.url, args.username, args.password, output_path, container))
    except Exception as exc:  # noqa: BLE001 — top-level runner
        print(f"!!! build failed: {exc}", file=sys.stderr)
        return 1
    print(">>> Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
