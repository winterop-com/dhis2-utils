"""Snapshot a curated immunization subset of play.dhis2.org into `infra/fixtures/play/`.

Runs against the `play42` profile and produces four committed fixture files
that `infra/scripts/build_e2e_dump.py` feeds into a fresh local DHIS2
during `make dhis2-build-e2e-dump`:

- `metadata.json` — every DataSet / Program / Dashboard / Visualization /
  Map / DataElement / Category* / OptionSet / Indicator / IndicatorType /
  ProgramRule / ProgramIndicator / TrackedEntityType / TrackedEntityAttribute
  transitively required by the curated roots. Org-unit geometry is stripped
  out (lives in the adjacent .geojson file) to keep the JSON diff-friendly.

- `organisation_units.json` — every OU on play42 (~1332 rows), name / code /
  parent / level / path / openingDate — NO geometry (same split rationale).

- `geometry.geojson` — single FeatureCollection with one feature per OU that
  has geometry on play. The loader side joins on `feature.id == ou.id`.

- `data_values.json.gz` — gzipped aggregate dataValueSet for Child Health +
  EPI Stock, last 12 months, country root + descendants. Captures ~190 k
  values; gzipped to keep the committed blob under ~3 MB.

- `tracker_payload.json.gz` — 500 sampled Child Programme tracked entities
  + their enrollments + events, gzipped. Gives the tracker plugin realistic
  volume without committing the full 19 k-entity play snapshot.

## Curated roots (immunization vertical)

- `BfMAe6Itzgt` Child Health (aggregate dataset — EPI monthly DEs)
- `TuL8IOPzpHh` EPI Stock (vaccine-stock dataset)
- `IpHINAT79UW` Child Programme (tracker program — child immunization schedule)
- `lxAQ7Zs9VYR` Antenatal care visit (event program — complements maternal cycle)
- `TAMlzYkstb7` Immunization dashboard
- `L1BtjXgpUpd` Immunization data dashboard
- `KQVXh5tlzW2` Measles (user org unit) dashboard

Run:
    DHIS2_PROFILE=play42 uv run python infra/scripts/pull_play_fixtures.py

The script is idempotent — every run overwrites the fixture files in place.
"""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
import sys
from pathlib import Path
from typing import Any

from dhis2w_core.client_context import open_client
from dhis2w_core.profile import resolve_profile

FIXTURE_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "play"

# Curated immunization-vertical roots.
DATASET_UIDS: tuple[str, ...] = (
    "BfMAe6Itzgt",  # Child Health
    "TuL8IOPzpHh",  # EPI Stock
)
PROGRAM_UIDS: tuple[str, ...] = (
    "IpHINAT79UW",  # Child Programme (tracker)
    "lxAQ7Zs9VYR",  # Antenatal care visit (event)
)
DASHBOARD_UIDS: tuple[str, ...] = (
    "TAMlzYkstb7",  # Immunization
    "L1BtjXgpUpd",  # Immunization data
    "KQVXh5tlzW2",  # Measles (user org unit)
)

# DHIS2's per-root /metadata endpoints return different top-level keys. The
# common shape is {sectionName: [...objects]} plus a "system" block we strip.
_SYSTEM_KEY = "system"

# Aggregate data window — 12 months ending at play42's most recent period.
# Conservative choice so the dump stays ~3-5 MB; widen via --months when needed.
DATA_START_DATE_DEFAULT = "2024-01-01"
DATA_END_DATE_DEFAULT = "2024-12-31"

# Tracker sample size — play42 ships 19 k Child Programme entities; we snapshot
# 500 for realistic volume without bloating the committed payload.
TRACKER_SAMPLE_DEFAULT = 500


async def _pull_one_metadata_bundle(client: Any, path: str) -> dict[str, list[dict[str, Any]]]:
    """Fetch `/api/.../metadata` for a root and drop the system block."""
    raw = await client.get_raw(path)
    bundle: dict[str, list[dict[str, Any]]] = {}
    for key, value in raw.items():
        if key == _SYSTEM_KEY:
            continue
        if isinstance(value, list):
            bundle[key] = value
    return bundle


def _merge_into(target: dict[str, dict[str, dict[str, Any]]], bundle: dict[str, list[dict[str, Any]]]) -> None:
    """Merge a per-root metadata bundle into `target` keyed by (section, uid)."""
    for section, entries in bundle.items():
        bucket = target.setdefault(section, {})
        for entry in entries:
            uid = entry.get("id")
            if not isinstance(uid, str):
                continue
            bucket[uid] = entry


async def pull_metadata(client: Any) -> dict[str, list[dict[str, Any]]]:
    """Pull metadata for every curated root and merge + dedupe by UID."""
    merged: dict[str, dict[str, dict[str, Any]]] = {}
    for uid in DATASET_UIDS:
        print(f"  /api/dataSets/{uid}/metadata", file=sys.stderr)
        _merge_into(merged, await _pull_one_metadata_bundle(client, f"/api/dataSets/{uid}/metadata"))
    for uid in PROGRAM_UIDS:
        print(f"  /api/programs/{uid}/metadata", file=sys.stderr)
        _merge_into(merged, await _pull_one_metadata_bundle(client, f"/api/programs/{uid}/metadata"))
    for uid in DASHBOARD_UIDS:
        print(f"  /api/dashboards/{uid}/metadata", file=sys.stderr)
        _merge_into(merged, await _pull_one_metadata_bundle(client, f"/api/dashboards/{uid}/metadata"))
    # Flatten back to list shape; sort entries by UID so the JSON is diff-stable.
    flat: dict[str, list[dict[str, Any]]] = {
        section: sorted(entries.values(), key=lambda row: row.get("id") or "") for section, entries in merged.items()
    }
    return flat


async def pull_legend_sets(client: Any) -> list[dict[str, Any]]:
    """Pull every LegendSet + its Legends (small table; simpler than dependency-chasing)."""
    raw = await client.get_raw(
        "/api/legendSets",
        params={"fields": ":owner", "paging": "false"},
    )
    rows = raw.get("legendSets") or []
    return sorted(
        [row for row in rows if isinstance(row, dict)],
        key=lambda row: row.get("id") or "",
    )


async def pull_ou_group_sets(client: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Pull every OrganisationUnitGroupSet + its groups (Maps reference them for split layers)."""
    gs_raw = await client.get_raw(
        "/api/organisationUnitGroupSets",
        params={"fields": ":owner", "paging": "false"},
    )
    g_raw = await client.get_raw(
        "/api/organisationUnitGroups",
        params={"fields": ":owner", "paging": "false"},
    )
    return (
        sorted(
            [row for row in (gs_raw.get("organisationUnitGroupSets") or []) if isinstance(row, dict)],
            key=lambda row: row.get("id") or "",
        ),
        sorted(
            [row for row in (g_raw.get("organisationUnitGroups") or []) if isinstance(row, dict)],
            key=lambda row: row.get("id") or "",
        ),
    )


async def pull_org_units(client: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Pull every OU + split geometry into a standalone FeatureCollection.

    Returns `(ou_rows_without_geometry, feature_collection)`. OU rows keep
    their `id / name / code / shortName / displayName / level / parent / path
    / openingDate / closedDate / featureType` and drop the bulky `geometry`
    blob, which lives in the FeatureCollection instead.
    """
    raw = await client.get_raw(
        "/api/organisationUnits",
        params={
            "fields": (
                "id,name,code,shortName,displayName,level,parent[id],path,openingDate,closedDate,featureType,geometry"
            ),
            "paging": "false",
        },
    )
    rows = raw.get("organisationUnits") or []
    ou_rows: list[dict[str, Any]] = []
    features: list[dict[str, Any]] = []
    for ou in rows:
        if not isinstance(ou, dict):
            continue
        geometry = ou.pop("geometry", None)
        ou_rows.append(ou)
        if isinstance(geometry, dict) and geometry.get("type") and geometry.get("coordinates"):
            features.append(
                {
                    "type": "Feature",
                    "id": ou["id"],
                    "properties": {
                        "name": ou.get("name"),
                        "level": ou.get("level"),
                        "code": ou.get("code"),
                    },
                    "geometry": geometry,
                },
            )
    feature_collection = {"type": "FeatureCollection", "features": sorted(features, key=lambda f: f["id"])}
    ou_rows.sort(key=lambda row: row.get("path") or row.get("id") or "")
    return ou_rows, feature_collection


async def pull_data_values(client: Any, *, start: str, end: str) -> dict[str, Any]:
    """Pull aggregate data values for Child Health + EPI Stock over [start, end]."""
    bundle: dict[str, Any] = {"dataValues": []}
    seen: set[tuple[str, str, str, str, str]] = set()
    for ds_uid in DATASET_UIDS:
        print(f"  /api/dataValueSets dataSet={ds_uid} {start}..{end}", file=sys.stderr)
        raw = await client.get_raw(
            "/api/dataValueSets",
            params={
                "dataSet": ds_uid,
                "orgUnit": "ImspTQPwCqd",  # Sierra Leone root
                "children": "true",
                "startDate": start,
                "endDate": end,
            },
        )
        for dv in raw.get("dataValues") or []:
            # Dedup: (dataElement, period, orgUnit, categoryOptionCombo, attributeOptionCombo)
            key = (
                dv.get("dataElement") or "",
                dv.get("period") or "",
                dv.get("orgUnit") or "",
                dv.get("categoryOptionCombo") or "",
                dv.get("attributeOptionCombo") or "",
            )
            if key in seen:
                continue
            seen.add(key)
            bundle["dataValues"].append(dv)
    bundle["dataValues"].sort(
        key=lambda dv: (
            dv.get("period") or "",
            dv.get("orgUnit") or "",
            dv.get("dataElement") or "",
        ),
    )
    return bundle


async def pull_tracker(client: Any, *, sample_size: int) -> dict[str, Any]:
    """Pull a capped sample of Child Programme tracked entities + full context."""
    print(f"  /api/tracker/trackedEntities program={PROGRAM_UIDS[0]} sample={sample_size}", file=sys.stderr)
    raw = await client.get_raw(
        "/api/tracker/trackedEntities",
        params={
            "program": PROGRAM_UIDS[0],
            "orgUnit": "ImspTQPwCqd",
            "ouMode": "DESCENDANTS",
            "pageSize": str(sample_size),
            "fields": "*,attributes,enrollments[*,events[*,dataValues]]",
        },
    )
    tes = raw.get("instances") or raw.get("trackedEntities") or []
    return {"trackedEntities": tes}


def _write_json(path: Path, payload: Any) -> None:
    """Write a JSON fixture with stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(f"  wrote {path.relative_to(Path.cwd())} ({path.stat().st_size:,} bytes)", file=sys.stderr)


def _write_gz_json(path: Path, payload: Any) -> None:
    """Write a gzipped JSON fixture."""
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    with gzip.open(path, "wb", compresslevel=9) as f:
        f.write(raw)
    print(f"  wrote {path.relative_to(Path.cwd())} ({path.stat().st_size:,} bytes)", file=sys.stderr)


async def _run(profile_name: str, *, start: str, end: str, sample: int) -> None:
    """Execute the pull against `profile_name` and write every fixture."""
    profile = resolve_profile(profile_name)
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    async with open_client(profile) as client:
        print(f"==> pulling metadata from {profile.base_url}", file=sys.stderr)
        metadata = await pull_metadata(client)
        summary = {section: len(entries) for section, entries in metadata.items()}
        print(f"    metadata sections: {summary}", file=sys.stderr)

        print("==> pulling all LegendSets (covers transitive LegendSet refs from maps + DEs)", file=sys.stderr)
        legend_sets = await pull_legend_sets(client)
        metadata["legendSets"] = legend_sets
        print(f"    {len(legend_sets)} legend sets", file=sys.stderr)

        print("==> pulling all OU group sets + groups (maps reference them for split layers)", file=sys.stderr)
        oug_sets, oug_groups = await pull_ou_group_sets(client)
        metadata["organisationUnitGroupSets"] = oug_sets
        metadata["organisationUnitGroups"] = oug_groups
        print(f"    {len(oug_sets)} OU group sets, {len(oug_groups)} OU groups", file=sys.stderr)

        print("==> pulling org units + geometry", file=sys.stderr)
        ou_rows, feature_collection = await pull_org_units(client)
        print(
            f"    {len(ou_rows)} org units, {len(feature_collection['features'])} geometries",
            file=sys.stderr,
        )

        print("==> pulling aggregate data values", file=sys.stderr)
        data_values = await pull_data_values(client, start=start, end=end)
        print(f"    {len(data_values['dataValues'])} data values", file=sys.stderr)

        print("==> pulling tracker sample", file=sys.stderr)
        tracker = await pull_tracker(client, sample_size=sample)
        print(f"    {len(tracker['trackedEntities'])} tracked entities", file=sys.stderr)

        print("==> writing fixtures", file=sys.stderr)
        _write_json(FIXTURE_DIR / "metadata.json", metadata)
        _write_json(FIXTURE_DIR / "organisation_units.json", ou_rows)
        _write_json(FIXTURE_DIR / "geometry.geojson", feature_collection)
        _write_gz_json(FIXTURE_DIR / "data_values.json.gz", data_values)
        _write_gz_json(FIXTURE_DIR / "tracker_payload.json.gz", tracker)


def main() -> int:
    """Parse args + run the pull."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        default="play42",
        help="Profile name (defaults to play42; any profile pointing at the DHIS2 Play demo).",
    )
    parser.add_argument(
        "--start-date",
        default=DATA_START_DATE_DEFAULT,
        help="Aggregate data window start (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--end-date",
        default=DATA_END_DATE_DEFAULT,
        help="Aggregate data window end (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--tracker-sample",
        type=int,
        default=TRACKER_SAMPLE_DEFAULT,
        help="How many Child Programme tracked entities to sample (default 500).",
    )
    args = parser.parse_args()
    asyncio.run(
        _run(
            args.profile,
            start=args.start_date,
            end=args.end_date,
            sample=args.tracker_sample,
        ),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
