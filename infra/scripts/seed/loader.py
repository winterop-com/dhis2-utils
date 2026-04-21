"""Typed-model loader for the Sierra Leone immunization fixture snapshot.

See `infra/scripts/seed/__init__.py` for the high-level shape. This
module is the mechanical side: read the JSON fixtures off disk, rehydrate
into the matching generated pydantic models (for type-safety + client
validation), POST through the normal DHIS2 metadata importer, then stream
the aggregate data values + tracker payload.

Keep the module order-agnostic: DHIS2's `/api/metadata` importer handles
the dependency graph server-side as long as every referenced UID is
present in the bundle. That means we don't need to topo-sort sections
on the client — just validate + submit.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path
from typing import Any

from dhis2_client import DataValue, WebMessageResponse
from dhis2_client.client import Dhis2Client
from dhis2_client.errors import Dhis2ApiError
from dhis2_client.generated.v42.schemas import (
    Category,
    CategoryCombo,
    CategoryOption,
    Dashboard,
    DataElement,
    DataSet,
    Indicator,
    Map,
    OptionSet,
    OrganisationUnit,
    Program,
    ProgramRule,
    ProgramRuleAction,
    ProgramRuleVariable,
    ProgramStage,
    TrackedEntityAttribute,
    TrackedEntityType,
    Visualization,
)

FIXTURE_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "play"
SIERRA_LEONE_ROOT_UID = "ImspTQPwCqd"


# Map each metadata section to its typed model. Sections not listed here
# flow through as dicts (the `/api/metadata` importer doesn't care, and
# we don't have generated models for every DHIS2 resource type — e.g.
# `categoryOptionCombos`, `dataEntryForms`, `notificationTemplates`).
_TYPED_SECTIONS: dict[str, type[Any]] = {
    "organisationUnits": OrganisationUnit,
    "dataElements": DataElement,
    "dataSets": DataSet,
    "categories": Category,
    "categoryCombos": CategoryCombo,
    "categoryOptions": CategoryOption,
    "optionSets": OptionSet,
    "indicators": Indicator,
    "programs": Program,
    "programStages": ProgramStage,
    "programRules": ProgramRule,
    "programRuleActions": ProgramRuleAction,
    "programRuleVariables": ProgramRuleVariable,
    "trackedEntityAttributes": TrackedEntityAttribute,
    "trackedEntityTypes": TrackedEntityType,
    "dashboards": Dashboard,
    "visualizations": Visualization,
    "maps": Map,
}


def _load_json(path: Path) -> Any:
    """Read a JSON file + return the decoded payload."""
    return json.loads(path.read_text(encoding="utf-8"))


def _load_gzip_json(path: Path) -> Any:
    """Read a gzipped JSON file + return the decoded payload."""
    with gzip.open(path, "rb") as f:
        return json.loads(f.read().decode("utf-8"))


_STRIP_KEYS: frozenset[str] = frozenset(
    {
        # User / sharing refs — point at Sierra Leone accounts we don't
        # curate. Cleaning these is a common pattern when porting DHIS2
        # metadata between instances; the locally-created admin takes
        # over as de-facto owner after import. Smaller metadata too.
        "userAccesses",
        "userGroupAccesses",
        "user",
        "createdBy",
        "lastUpdatedBy",
        "notificationRecipients",
        "recipientUserGroup",
        "recipientUserGroups",
        # Computed / read-only fields that leak into `/api/.../metadata`
        # responses and confuse the importer — Hibernate tries to flush
        # them as first-class entities and fails on missing parent refs.
        "compulsoryDataElementOperands",
        "displayName",
        "displayShortName",
        "displayFormName",
        "displayDescription",
        "displayTitle",
        "displaySubtitle",
        "displayBaseLineLabel",
        "displayTargetLineLabel",
        "displayDomainAxisLabel",
        "displayRangeAxisLabel",
        "access",
        "favorite",
        "favorites",
        "subscribed",
        "subscribers",
        "interpretations",
        "translations",
        "href",
    },
)

# Uniform sharing block applied to every imported object so references to
# DHIS2 Play's users + groups don't reach the importer. Public read/write
# keeps the seed self-contained; the locally-created admin takes ownership
# via createdBy/lastUpdatedBy auto-population on write.
_DEFAULT_SHARING: dict[str, Any] = {
    "public": "rwrw----",
    "external": False,
    "users": {},
    "userGroups": {},
}


def _strip_dataset_self_refs(row: dict[str, Any]) -> dict[str, Any]:
    """Drop the self-referencing `dataSet` field from `dataSetElements`.

    Play's `/api/dataSets/{uid}/metadata` embeds
    `dataSetElements[].dataSet = {id: <parent>}`. DHIS2's importer treats
    each nested ref as a lazy proxy with no `periodType`, then Hibernate
    fails the whole flush with
    `PropertyValueException: not-null property references a null or
    transient value : org.hisp.dhis.dataset.DataSet.periodType` on a
    fresh stack. DHIS2 infers the parent from context so dropping the
    explicit back-ref is safe.
    """
    dse = row.get("dataSetElements")
    if not isinstance(dse, list):
        return row
    cleaned_items: list[dict[str, Any]] = []
    for entry in dse:
        if isinstance(entry, dict):
            cleaned_items.append({k: v for k, v in entry.items() if k != "dataSet"})
    copy = dict(row)
    copy["dataSetElements"] = cleaned_items
    return copy


def _strip_sharing(row: dict[str, Any]) -> dict[str, Any]:
    """Strip user-based sharing + computed fields + replace the sharing block.

    Common DHIS2 porting pattern: when migrating metadata between instances
    the source's users, user groups, createdBy / lastUpdatedBy, sharing
    arrays all reference identities that don't exist on the target. Scrub
    them aggressively and set a canonical `sharing` block so the
    locally-created admin becomes the de-facto owner after import.
    """
    cleaned: dict[str, Any] = {"sharing": dict(_DEFAULT_SHARING)}
    for key, value in row.items():
        if key in _STRIP_KEYS:
            continue
        if key == "sharing":
            # Replaced with _DEFAULT_SHARING above; skip the original.
            continue
        cleaned[key] = value
    return cleaned


def _strip_nested_sharing(rows: list[Any]) -> list[Any]:
    """Apply `_strip_sharing` + `_strip_dataset_self_refs` through rows."""
    out: list[Any] = []
    for row in rows:
        if hasattr(row, "model_dump"):
            dumped = row.model_dump(by_alias=True, exclude_none=True, mode="json")
            if isinstance(dumped, dict):
                out.append(_strip_dataset_self_refs(_strip_sharing(dumped)))
                continue
        if isinstance(row, dict):
            out.append(_strip_dataset_self_refs(_strip_sharing(row)))
            continue
        out.append(row)
    return out


def _merge_geometry_onto_org_units(
    org_units: list[dict[str, Any]],
    feature_collection: dict[str, Any],
) -> list[dict[str, Any]]:
    """Attach `geometry` to each OU row by matching feature.id."""
    by_id: dict[str, dict[str, Any]] = {}
    for feature in feature_collection.get("features") or []:
        uid = feature.get("id")
        if isinstance(uid, str):
            by_id[uid] = feature.get("geometry")
    result: list[dict[str, Any]] = []
    for ou in org_units:
        uid = ou.get("id")
        if isinstance(uid, str) and uid in by_id:
            result.append({**ou, "geometry": by_id[uid]})
        else:
            result.append(ou)
    return result


def load_metadata() -> dict[str, list[Any]]:
    """Read fixtures off disk + rehydrate into typed generated models.

    Returns a dict keyed by DHIS2 resource section name. Each value is a
    list of typed pydantic models (or dicts for sections not in
    `_TYPED_SECTIONS`). The return shape is directly consumable by
    `import_metadata_bundle` — no further massaging required.
    """
    bundle = _load_json(FIXTURE_DIR / "metadata.json")
    org_units = _load_json(FIXTURE_DIR / "organisation_units.json")
    geometry = _load_json(FIXTURE_DIR / "geometry.geojson")
    # Attach geometry to OUs + fold into the main bundle under the
    # canonical "organisationUnits" key.
    bundle["organisationUnits"] = _merge_geometry_onto_org_units(org_units, geometry)
    typed: dict[str, list[Any]] = {}
    for section, rows in bundle.items():
        if not isinstance(rows, list):
            continue
        model = _TYPED_SECTIONS.get(section)
        if model is None:
            # Pass untyped sections through — the importer still accepts them.
            typed[section] = [row for row in rows if isinstance(row, dict)]
            continue
        validated: list[Any] = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            validated.append(model.model_validate(row))
        typed[section] = validated
    return typed


def _dump_section(rows: list[Any]) -> list[dict[str, Any]]:
    """Dump typed models back to JSON-friendly dicts for the /api/metadata post."""
    out: list[dict[str, Any]] = []
    for row in rows:
        if hasattr(row, "model_dump"):
            dumped = row.model_dump(by_alias=True, exclude_none=True, mode="json")
            if isinstance(dumped, dict):
                out.append(dumped)
                continue
        if isinstance(row, dict):
            out.append(row)
    return out


_DISAMBIGUATE_SECTIONS: frozenset[str] = frozenset(
    {"trackedEntityTypes", "trackedEntityAttributes"},
)


def _disambiguate_common_names(section: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Append a " (Play)" suffix to TET + TEA names so they don't collide with DHIS2 built-ins.

    A fresh DHIS2 install ships with a "Person" TrackedEntityType and
    "First name" / "Last name" TrackedEntityAttributes whose UIDs differ
    from play's. Name + shortName are UNIQUE in DHIS2, so importing our
    copies fails `E5003`. The suffix side-steps the collision without
    touching any UID references downstream.
    """
    if section not in _DISAMBIGUATE_SECTIONS:
        return rows
    out: list[dict[str, Any]] = []
    for row in rows:
        copy = dict(row)
        for field in ("name", "shortName", "displayName"):
            value = copy.get(field)
            if isinstance(value, str) and not value.endswith(" (Play)"):
                copy[field] = f"{value} (Play)"
        out.append(copy)
    return out


_DEFERRED_SECTIONS: frozenset[str] = frozenset(
    {"dataSets", "sections", "dataEntryForms"},
)


async def _post_metadata(client: Dhis2Client, payload: dict[str, list[Any]]) -> WebMessageResponse:
    """POST one bundle to `/api/metadata` and return the parsed envelope."""
    raw = await client.post_raw(
        "/api/metadata",
        payload,
        params={
            "importStrategy": "CREATE_AND_UPDATE",
            "atomicMode": "OBJECT",
            "flushMode": "OBJECT",
            # Match existing metadata by CODE rather than UID during the
            # preheat — fixes the "default" Category / CategoryCombo
            # collision on a fresh DHIS2 install (both ours + DHIS2's
            # built-ins share code="default" but have different UIDs).
            "preheatIdentifier": "CODE",
            "skipSharing": "true",
        },
    )
    return WebMessageResponse.model_validate(raw)


async def import_metadata_bundle(
    client: Dhis2Client,
    bundle: dict[str, list[Any]],
    *,
    atomic_mode: str = "OBJECT",  # retained for back-compat; routed through _post_metadata
) -> WebMessageResponse:
    """POST the typed bundle in two passes.

    Pass 1: every section EXCEPT `dataSets`, `sections`, and
    `dataEntryForms`. These three don't pass DHIS2's validator when
    imported in the same transaction as their dependencies — Hibernate
    throws a `PropertyValueException: not-null property references a
    null or transient value : DataSet.periodType` during partial flushes.

    Pass 2: the deferred trio on its own, after everything else has
    landed. DHIS2 resolves the references cleanly this time round.

    `atomic_mode` is accepted for back-compat with callers that passed
    it explicitly; the new path always uses `OBJECT` under the hood so
    per-object rejections (e.g. DHIS2 built-in collisions) don't cascade.
    """
    del atomic_mode  # noqa: F841 — kept in signature for back-compat
    sanitise = lambda section, rows: _disambiguate_common_names(  # noqa: E731
        section,
        _strip_nested_sharing(_dump_section(rows)),
    )
    first_pass = {
        section: sanitise(section, rows)
        for section, rows in bundle.items()
        if rows and section not in _DEFERRED_SECTIONS
    }
    second_pass = {
        section: sanitise(section, rows)
        for section, rows in bundle.items()
        if rows and section in _DEFERRED_SECTIONS
    }
    first_response = await _post_metadata(client, first_pass)
    if second_pass:
        await _post_metadata(client, second_pass)
    return first_response


_DATA_VALUE_CHUNK: int = 10_000


async def import_data_values(client: Dhis2Client) -> WebMessageResponse:
    """Stream the gzipped aggregate data values into `/api/dataValueSets` in chunks.

    188 k values in a single POST blows past the client's default 30 s
    read timeout on a fresh stack. Chunk into 10 k-row batches — each
    round-trips in ~3-5 s and the aggregate import completes in ~90 s.

    Every row still round-trips through `DataValue.model_validate` so
    the typed shape is exercised on all 188 k rows.
    """
    raw_bundle = _load_gzip_json(FIXTURE_DIR / "data_values.json.gz")
    data_values = raw_bundle.get("dataValues") or []
    validated = [DataValue.model_validate(dv) for dv in data_values if isinstance(dv, dict)]
    dumped = [v.model_dump(by_alias=True, exclude_none=True, mode="json") for v in validated]
    total_imported = 0
    total_updated = 0
    total_ignored = 0
    last_response: WebMessageResponse | None = None
    for start in range(0, len(dumped), _DATA_VALUE_CHUNK):
        chunk = dumped[start : start + _DATA_VALUE_CHUNK]
        try:
            raw = await client.post_raw("/api/dataValueSets", body={"dataValues": chunk})
        except Dhis2ApiError as exc:
            # DHIS2 returns 409 even on partial success (e.g. a handful of
            # non-numeric values on play for numeric DEs — play data drift).
            # Treat 409 with a structured body as "warning" — extract the
            # import counts and keep going.
            if exc.status_code != 409 or not isinstance(exc.body, dict):
                raise
            raw = exc.body
        last_response = WebMessageResponse.model_validate(raw)
        counts = last_response.import_count()
        if counts is not None:
            total_imported += counts.imported or 0
            total_updated += counts.updated or 0
            total_ignored += counts.ignored or 0
    if last_response is None:
        raise RuntimeError("no data values to import")
    # Synthesise a summary envelope so seed_play's reporting shows totals.
    summary_raw = {
        "status": last_response.status,
        "importCount": {
            "imported": total_imported,
            "updated": total_updated,
            "ignored": total_ignored,
            "deleted": 0,
        },
    }
    return WebMessageResponse.model_validate(summary_raw)


async def assign_admin_to_sierra_leone(client: Dhis2Client) -> None:
    """Attach the Sierra Leone root to admin's capture + view + search scopes.

    Without this, data-value + tracker writes fail with
    E7617 "Organisation unit not in hierarchy of current user". Called
    from `seed_play` after metadata import (so the root OU exists) and
    before any data-values / tracker write.

    Uses PUT-replace on the user resource rather than JSON Patch — the
    patch endpoint's shape varies across DHIS2 minors, but the full
    user PUT is stable.
    """
    me_raw = await client.get_raw(f"/api/users/{(await client.system.me()).id}")
    if not me_raw.get("id"):
        raise RuntimeError("admin user has no id — DHIS2 bootstrap not ready")
    root_ref = {"id": SIERRA_LEONE_ROOT_UID}
    me_raw["organisationUnits"] = [root_ref]
    me_raw["dataViewOrganisationUnits"] = [root_ref]
    me_raw["teiSearchOrganisationUnits"] = [root_ref]
    await client.put_raw(f"/api/users/{me_raw['id']}", me_raw)


async def import_tracker(client: Dhis2Client) -> WebMessageResponse:
    """POST the sampled Child Programme tracker payload.

    Tracker bundle shape is too wide to fully re-validate via the
    generated TrackerBundle model (many optional fields missing on
    sampled data), so the payload round-trips as dict here. The
    POST itself still exercises the tracker endpoint end-to-end.
    """
    raw_bundle = _load_gzip_json(FIXTURE_DIR / "tracker_payload.json.gz")
    tes = raw_bundle.get("trackedEntities") or []
    body = {"trackedEntities": tes}
    raw = await client.post_raw(
        "/api/tracker",
        body=body,
        params={
            "importStrategy": "CREATE_AND_UPDATE",
            "atomicMode": "OBJECT",
            "async": "false",
        },
    )
    return WebMessageResponse.model_validate(raw)


async def seed_play(client: Dhis2Client) -> None:
    """End-to-end: metadata + geometry + data values + tracker."""
    print(">>> Loading typed metadata bundle", flush=True)
    bundle = load_metadata()
    summary = {section: len(rows) for section, rows in bundle.items()}
    print(f"    {summary}", flush=True)

    print(">>> Importing metadata bundle", flush=True)
    response = await import_metadata_bundle(client, bundle)
    counts = response.import_count()
    if counts is not None:
        print(
            f"    imported={counts.imported}  updated={counts.updated}  "
            f"ignored={counts.ignored}  deleted={counts.deleted}",
            flush=True,
        )

    print(">>> Assigning admin to Sierra Leone OU scope", flush=True)
    await assign_admin_to_sierra_leone(client)

    print(">>> Importing aggregate data values", flush=True)
    dv_response = await import_data_values(client)
    dv_counts = dv_response.import_count()
    if dv_counts is not None:
        print(
            f"    imported={dv_counts.imported}  updated={dv_counts.updated}  "
            f"ignored={dv_counts.ignored}  deleted={dv_counts.deleted}",
            flush=True,
        )

    print(">>> Importing Child Programme tracker sample", flush=True)
    tk_response = await import_tracker(client)
    stats = getattr(tk_response, "model_extra", None) or {}
    bundle_stats = stats.get("bundleReport") or stats.get("stats") or stats
    if isinstance(bundle_stats, dict):
        print(f"    tracker import stats: {bundle_stats}", flush=True)
