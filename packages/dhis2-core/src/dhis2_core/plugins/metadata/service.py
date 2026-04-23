"""Service layer for the `metadata` plugin — thin wrapper over generated resources."""

from __future__ import annotations

import re
from collections.abc import AsyncIterator, Mapping, Sequence
from typing import Any

from dhis2_client import JsonPatchOp, SearchResults, WebMessageResponse
from dhis2_client.generated.v42.oas import (
    AtomicMode,
    FlushMode,
    ImportStrategy,
    MergeMode,
    PreheatIdentifier,
    PreheatMode,
)
from pydantic import BaseModel, ConfigDict, Field

from dhis2_core.client_context import open_client
from dhis2_core.plugins.metadata.models import MetadataBundle, MetadataItem
from dhis2_core.profile import Profile

_CAMEL_RE = re.compile(r"(?<!^)(?=[A-Z])")
_STREAM_PAGE_SIZE = 500


class UnknownResourceError(LookupError):
    """Raised when a caller asks for a metadata resource not present on this instance."""


def _attr_name(resource: str) -> str:
    """Convert a DHIS2 resource name (camelCase plural) to a Resources attribute name."""
    return _CAMEL_RE.sub("_", resource).lower()


def _resource_names(resources: object) -> list[str]:
    """List the Resources attribute names that map to real metadata types."""
    return sorted(name for name in dir(resources) if not name.startswith("_"))


async def list_resource_types(profile: Profile) -> list[str]:
    """Return every metadata resource type exposed by the instance's generated client."""
    async with open_client(profile) as client:
        return _resource_names(client.resources)


async def list_metadata(
    profile: Profile,
    resource: str,
    *,
    fields: str | None = None,
    filters: list[str] | None = None,
    root_junction: str | None = None,
    order: list[str] | None = None,
    page: int | None = None,
    page_size: int | None = None,
    paging: bool | None = None,
    translate: bool | None = None,
    locale: str | None = None,
) -> list[BaseModel]:
    """List a metadata resource (e.g. `dataElements`, `indicators`) as typed generated models.

    Returns the generated pydantic models the resource accessor parses — e.g.
    `list[DataElement]` for `dataElements`. Callers that need JSON-friendly
    dicts (MCP tools, CLI JSON output) dump at the edge via
    `model.model_dump(...)`.

    Every DHIS2 `/api/<resource>` query parameter is forwarded. `filters` and
    `order` may repeat — a list of strings becomes `?filter=a&filter=b`.
    `root_junction` is `"AND"` (default) or `"OR"`. `paging=False` returns the
    full catalog in one response; for memory-friendly streaming use
    `iter_metadata`.
    """
    async with open_client(profile) as client:
        accessor = _resolve_accessor(client.resources, resource)
        models: list[BaseModel] = await accessor.list(
            fields=fields,
            filters=filters,
            root_junction=root_junction,
            order=order,
            page=page,
            page_size=page_size,
            paging=paging,
            translate=translate,
            locale=locale,
        )
        return models


async def iter_metadata(
    profile: Profile,
    resource: str,
    *,
    fields: str | None = None,
    filters: list[str] | None = None,
    root_junction: str | None = None,
    order: list[str] | None = None,
    page_size: int = _STREAM_PAGE_SIZE,
    translate: bool | None = None,
    locale: str | None = None,
) -> AsyncIterator[BaseModel]:
    """Stream every row of a metadata resource as typed generated models, one at a time.

    Walks successive pages server-side (`page=1`, `page=2`, ...) stopping when
    a page returns fewer rows than `page_size`. `page_size` defaults to 500 —
    large enough to keep request count low, small enough not to blow memory on
    heavy fields selectors.
    """
    page = 1
    async with open_client(profile) as client:
        accessor = _resolve_accessor(client.resources, resource)
        while True:
            models = await accessor.list(
                fields=fields,
                filters=filters,
                root_junction=root_junction,
                order=order,
                page=page,
                page_size=page_size,
                paging=True,
                translate=translate,
                locale=locale,
            )
            if not models:
                return
            for model in models:
                yield model
            if len(models) < page_size:
                return
            page += 1


async def export_metadata(
    profile: Profile,
    *,
    resources: list[str] | None = None,
    fields: str | None = None,
    skip_sharing: bool = False,
    skip_translation: bool = False,
    skip_validation: bool = False,
    per_resource_filters: Mapping[str, list[str]] | None = None,
    per_resource_fields: Mapping[str, str] | None = None,
) -> MetadataBundle:
    """Download a metadata bundle from `GET /api/metadata` and return a typed `MetadataBundle`.

    `resources` limits the export to specific types (e.g. `["dataElements",
    "indicators"]`); omit for everything. `fields` is the standard DHIS2
    selector — `":owner"` (the default DHIS2 uses internally for
    cross-instance imports) preserves every field required for a faithful
    round-trip, while `:identifiable` / `:all` / a custom list give tighter
    control.

    `per_resource_filters` narrows an export to a subset of each resource,
    using DHIS2's per-resource filter wire format
    (`?dataElements:filter=name:like:ANC`). The dict key is the resource
    name (matching `resources`); the value is a list of
    `property:operator:value` filter strings — same DSL as
    `dhis2 metadata list --filter`. Repeated filters are AND'd by DHIS2.

    `per_resource_fields` per-resource-overrides the global `fields`
    selector (`?dataElements:fields=:identifiable`). Useful when one
    resource type needs a heavy `:owner` selector and another just needs
    `id,name`.

    The returned `MetadataBundle` has typed accessors (`resources()`,
    `get_resource(name)`, `all_uids()`, `summary()`, `total()`) so callers
    never see the raw dict shape.
    """
    params: dict[str, Any] = {}
    if resources:
        for name in resources:
            params[name] = "true"
    if fields is not None:
        params["fields"] = fields
    if skip_sharing:
        params["skipSharing"] = "true"
    if skip_translation:
        params["skipTranslation"] = "true"
    if skip_validation:
        params["skipValidation"] = "true"
    if per_resource_filters:
        for resource, filter_exprs in per_resource_filters.items():
            if filter_exprs:
                # httpx serialises a list-valued param as repeated query
                # params — exactly what DHIS2 expects for per-resource filters.
                params[f"{resource}:filter"] = list(filter_exprs)
    if per_resource_fields:
        for resource, selector in per_resource_fields.items():
            params[f"{resource}:fields"] = selector
    async with open_client(profile) as client:
        raw = await client.get_raw("/api/metadata", params=params)
    return MetadataBundle.from_raw(raw)


async def import_metadata(
    profile: Profile,
    bundle: MetadataBundle,
    *,
    import_strategy: ImportStrategy | str = ImportStrategy.CREATE_AND_UPDATE,
    atomic_mode: AtomicMode | str = AtomicMode.ALL,
    dry_run: bool = False,
    skip_sharing: bool = False,
    skip_translation: bool = False,
    skip_validation: bool = False,
    identifier: PreheatIdentifier | str = PreheatIdentifier.UID,
    merge_mode: MergeMode | str | None = None,
    preheat_mode: PreheatMode | str | None = None,
    flush_mode: FlushMode | str | None = None,
) -> WebMessageResponse:
    """Upload a metadata bundle via `POST /api/metadata` and return the parsed import report.

    Strategy defaults match DHIS2's own defaults: `CREATE_AND_UPDATE` (upsert),
    `ALL` (atomic — roll back every object if any fails), `identifier=UID`.
    `dry_run=True` runs validation + preheat but commits nothing — use it to
    pre-check a bundle before a real import. Returns the `WebMessageResponse`
    envelope; `.import_count()`, `.conflicts()`, and
    `.web_message`'s typed `ImportReport` body are all available on it.

    Every enum-typed argument accepts either the generated `StrEnum` member
    (e.g. `ImportStrategy.CREATE`) or the raw string — `StrEnum` members ARE
    strings, so both go on the wire identically.
    """
    params: dict[str, Any] = {
        "importStrategy": str(import_strategy),
        "atomicMode": str(atomic_mode),
        "identifier": str(identifier),
    }
    if dry_run:
        params["importMode"] = "VALIDATE"
    if skip_sharing:
        params["skipSharing"] = "true"
    if skip_translation:
        params["skipTranslation"] = "true"
    if skip_validation:
        params["skipValidation"] = "true"
    if merge_mode is not None:
        params["mergeMode"] = str(merge_mode)
    if preheat_mode is not None:
        params["preheatMode"] = str(preheat_mode)
    if flush_mode is not None:
        params["flushMode"] = str(flush_mode)
    async with open_client(profile) as client:
        raw = await client.post_raw("/api/metadata", bundle.to_wire(), params=params)
    return WebMessageResponse.model_validate(raw)


# Fields whose nested references are structurally expected to sit outside the
# bundle (user ownership, sharing blocks). Otherwise every filtered export
# would drown in "dangling user" / "dangling userGroupAccess" warnings. Pass
# `skip_fields=frozenset()` to `bundle_dangling_references` to check these too.
_REFERENCE_NOISE_FIELDS: frozenset[str] = frozenset(
    {
        "createdBy",
        "lastUpdatedBy",
        "user",
        "userAccesses",
        "userGroupAccesses",
        "sharing",
    }
)


class DanglingReference(BaseModel):
    """One reference-field bucket: field name + UIDs it points at that aren't in the bundle."""

    model_config = ConfigDict(frozen=True)

    field_name: str
    missing_uids: list[str] = Field(default_factory=list)

    @property
    def count(self) -> int:
        """Number of missing UIDs in this bucket."""
        return len(self.missing_uids)


class DanglingReferences(BaseModel):
    """Summary of references inside a bundle that point at UIDs not present in the bundle.

    `items` groups every missing reference by the field name where it was
    found (`categoryCombo`, `optionSet`, `legendSets`, ...) — this is
    usually enough to decide which resource type is missing from the
    export. `bundle_uid_count` is the denominator.
    """

    items: list[DanglingReference] = Field(default_factory=list)
    bundle_uid_count: int = 0
    skipped_fields: list[str] = Field(default_factory=list)

    @property
    def total_missing(self) -> int:
        """Total missing UIDs summed across every field bucket."""
        return sum(item.count for item in self.items)

    @property
    def is_clean(self) -> bool:
        """True when every reference in the bundle resolves to a UID present in the bundle."""
        return self.total_missing == 0


def bundle_dangling_references(
    bundle: MetadataBundle,
    *,
    skip_fields: frozenset[str] = _REFERENCE_NOISE_FIELDS,
) -> DanglingReferences:
    """Walk `bundle` and report references to UIDs not present in the bundle.

    A reference is any nested `{"id": "<uid>"}` dict — DHIS2's wire shape
    for object-to-object pointers. The parent field name (e.g.
    `categoryCombo`, `optionSet`) is what gets reported so the user knows
    what to add to their export.

    `skip_fields` defaults to a curated noise list (user ownership blocks,
    sharing blocks) that almost always points at UIDs outside a typical
    metadata export; pass `frozenset()` to check everything.
    """
    known_uids = bundle.all_uids()
    missing_by_field: dict[str, set[str]] = {}
    for _, items in bundle.resources():
        for item in items:
            # Typed id/name on the item aren't references — they identify the
            # item itself. Only walk the extras for nested reference shapes.
            _collect_reference_uids(item.model_extra or {}, missing_by_field, known_uids, skip_fields)

    return DanglingReferences(
        items=[
            DanglingReference(field_name=field, missing_uids=sorted(uids))
            for field, uids in sorted(missing_by_field.items())
        ],
        bundle_uid_count=len(known_uids),
        skipped_fields=sorted(skip_fields),
    )


def _collect_reference_uids(
    obj: Any,
    missing: dict[str, set[str]],
    known_uids: set[str],
    skip_fields: frozenset[str],
) -> None:
    """Recursively walk `obj`, recording `(field_name, uid)` refs that aren't in `known_uids`."""
    if not isinstance(obj, dict):
        return
    for key, value in obj.items():
        if key in skip_fields:
            continue
        if isinstance(value, dict):
            uid = value.get("id")
            if isinstance(uid, str) and uid not in known_uids:
                missing.setdefault(key, set()).add(uid)
            _collect_reference_uids(value, missing, known_uids, skip_fields)
        elif isinstance(value, list):
            for element in value:
                if isinstance(element, dict):
                    uid = element.get("id")
                    if isinstance(uid, str) and uid not in known_uids:
                        missing.setdefault(key, set()).add(uid)
                    _collect_reference_uids(element, missing, known_uids, skip_fields)


class ObjectChange(BaseModel):
    """One object affected by a metadata diff."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str | None = None
    changed_fields: list[str] = Field(default_factory=list)


class ResourceDiff(BaseModel):
    """Per-resource diff — what happens to `<resource>` when going from left → right."""

    model_config = ConfigDict(frozen=True)

    resource: str
    created: list[ObjectChange] = Field(default_factory=list)
    deleted: list[ObjectChange] = Field(default_factory=list)
    updated: list[ObjectChange] = Field(default_factory=list)
    unchanged_count: int = 0

    @property
    def total_changed(self) -> int:
        """Count of objects that differ between the two bundles (create + update + delete)."""
        return len(self.created) + len(self.deleted) + len(self.updated)


class MetadataDiff(BaseModel):
    """Structured comparison between two metadata bundles.

    `left` and `right` refer to the two bundles passed in. `created` objects
    are in `right` but not `left`; `deleted` are in `left` but not `right`;
    `updated` exist in both but differ on at least one non-ignored field.
    """

    left_label: str
    right_label: str
    resources: list[ResourceDiff] = Field(default_factory=list)
    ignored_fields: list[str] = Field(default_factory=list)

    @property
    def total_created(self) -> int:
        """Sum of created counts across every resource."""
        return sum(len(r.created) for r in self.resources)

    @property
    def total_updated(self) -> int:
        """Sum of updated counts across every resource."""
        return sum(len(r.updated) for r in self.resources)

    @property
    def total_deleted(self) -> int:
        """Sum of deleted counts across every resource."""
        return sum(len(r.deleted) for r in self.resources)

    @property
    def total_unchanged(self) -> int:
        """Sum of unchanged counts across every resource."""
        return sum(r.unchanged_count for r in self.resources)


# Metadata noise that differs across instances without being a "real" change.
# Skipped by default on field comparison so diff output stays meaningful.
_DEFAULT_IGNORED_FIELDS: frozenset[str] = frozenset(
    {
        "lastUpdated",
        "lastUpdatedBy",
        "created",
        "createdBy",
        "translations",
        "access",
        "favorites",
        "href",
    }
)


def _item_field_map(item: MetadataItem) -> dict[str, Any]:
    """Flatten typed id/name + extras into one key-indexed view for field comparison."""
    # id + name are typed on MetadataItem; everything else lives in model_extra.
    flat: dict[str, Any] = dict(item.model_extra or {})
    if item.id is not None:
        flat["id"] = item.id
    if item.name is not None:
        flat["name"] = item.name
    return flat


def _changed_fields(left_flat: Mapping[str, Any], right_flat: Mapping[str, Any], ignored: frozenset[str]) -> list[str]:
    """Return top-level field names whose values differ between the two objects."""
    keys = (set(left_flat) | set(right_flat)) - ignored
    return sorted(key for key in keys if left_flat.get(key) != right_flat.get(key))


def diff_bundles(
    left: MetadataBundle,
    right: MetadataBundle,
    *,
    left_label: str = "left",
    right_label: str = "right",
    ignored_fields: frozenset[str] = _DEFAULT_IGNORED_FIELDS,
) -> MetadataDiff:
    """Structurally compare two metadata bundles; returns a typed `MetadataDiff`.

    Bundles are the shape `dhis2 metadata export` produces. Default
    `ignored_fields` skips DHIS2's per-instance noise (`lastUpdated`,
    `createdBy`, `access`, ...) so a round-trip `export → import → export`
    diff shows zero real changes instead of every object as "updated"
    because timestamps bumped.
    """
    resources: list[ResourceDiff] = []
    # Union the resource names present in either bundle — something could be
    # entirely absent on one side.
    resource_names = sorted({*left.resource_names(), *right.resource_names()})
    for name in resource_names:
        left_items = {item.id: item for item in left.get_resource(name) if item.id}
        right_items = {item.id: item for item in right.get_resource(name) if item.id}
        created: list[ObjectChange] = []
        deleted: list[ObjectChange] = []
        updated: list[ObjectChange] = []
        unchanged = 0
        for uid in sorted(set(left_items) | set(right_items)):
            left_item = left_items.get(uid)
            right_item = right_items.get(uid)
            if left_item is None and right_item is not None:
                created.append(ObjectChange(id=uid, name=right_item.name))
            elif right_item is None and left_item is not None:
                deleted.append(ObjectChange(id=uid, name=left_item.name))
            elif left_item is not None and right_item is not None:
                changed = _changed_fields(_item_field_map(left_item), _item_field_map(right_item), ignored_fields)
                if changed:
                    updated.append(ObjectChange(id=uid, name=right_item.name, changed_fields=changed))
                else:
                    unchanged += 1
        resources.append(
            ResourceDiff(
                resource=name,
                created=created,
                deleted=deleted,
                updated=updated,
                unchanged_count=unchanged,
            )
        )
    return MetadataDiff(
        left_label=left_label,
        right_label=right_label,
        resources=resources,
        ignored_fields=sorted(ignored_fields),
    )


async def diff_bundle_against_instance(
    profile: Profile,
    bundle: MetadataBundle,
    *,
    bundle_label: str = "file",
    resources: list[str] | None = None,
    ignored_fields: frozenset[str] = _DEFAULT_IGNORED_FIELDS,
) -> MetadataDiff:
    """Export the live instance + diff it against `bundle`.

    `resources` narrows the export to specific types (defaults to every
    resource present in `bundle`, so we don't drag down the entire
    catalog just to compare one slice).
    """
    if resources is None:
        resources = bundle.resource_names()
    live_bundle = await export_metadata(profile, resources=resources or None, fields=":owner")
    return diff_bundles(
        live_bundle,
        bundle,
        left_label=f"instance:{profile.base_url}",
        right_label=bundle_label,
        ignored_fields=ignored_fields,
    )


async def diff_profiles(
    profile_a: Profile,
    profile_b: Profile,
    *,
    resources: list[str],
    left_label: str | None = None,
    right_label: str | None = None,
    fields: str = ":owner",
    per_resource_filters: Mapping[str, list[str]] | None = None,
    ignored_fields: frozenset[str] = _DEFAULT_IGNORED_FIELDS,
) -> MetadataDiff:
    """Export `resources` from two profiles in parallel and diff them structurally.

    Staging-vs-prod drift monitoring: pick a narrow resource slice + filters
    (stage and prod always differ on user accounts, timestamps, and
    incidental config — filter those out first) and compare the remainder
    structurally.

    `resources` must be explicit — there's no "diff everything" default,
    because a whole-instance diff is rarely what an operator actually
    wants (drift in e.g. `userRoles` / `organisationUnits` is usually
    expected + noise-dominated).

    `per_resource_filters` takes the same shape `export_metadata` uses:
    `{resource: [filter_expr, ...]}` with the standard DHIS2
    `property:operator:value` syntax. Every exported side gets the
    same filters so what you're comparing on each profile is apples-to-apples.

    `ignored_fields` extends the default `lastUpdated` / `createdBy` /
    `access` skip list. Pass `frozenset({*_DEFAULT_IGNORED_FIELDS, "sharing"})`
    to also ignore per-instance sharing blocks, or pass a custom frozenset
    to override entirely.

    Runs the two exports concurrently — one profile shouldn't block the
    other, and staging instances tend to be slower than prod.
    """
    if not resources:
        raise ValueError("diff_profiles requires at least one resource type")

    import asyncio as _asyncio

    bundle_a, bundle_b = await _asyncio.gather(
        export_metadata(
            profile_a,
            resources=resources,
            fields=fields,
            per_resource_filters=per_resource_filters,
        ),
        export_metadata(
            profile_b,
            resources=resources,
            fields=fields,
            per_resource_filters=per_resource_filters,
        ),
    )
    return diff_bundles(
        bundle_a,
        bundle_b,
        left_label=left_label or f"profile-a:{profile_a.base_url}",
        right_label=right_label or f"profile-b:{profile_b.base_url}",
        ignored_fields=ignored_fields,
    )


async def search_metadata(
    profile: Profile,
    query: str,
    *,
    page_size: int = 50,
    resource: str | None = None,
    fields: str | None = None,
    exact: bool = False,
) -> SearchResults:
    """Cross-resource text search via `client.metadata.search`.

    Three concurrent `/api/metadata?filter=<field>:<op>:<query>` calls (one
    per match axis: `id`, `code`, `name`) merged client-side with UID
    dedup. `resource` narrows to one DHIS2 resource plural; `fields` asks
    DHIS2 for extra columns (stored on `SearchHit.extras`); `exact=True`
    switches the operator from `ilike` substring to `eq` strict match.
    """
    async with open_client(profile) as client:
        return await client.metadata.search(
            query,
            page_size=page_size,
            resource=resource,
            fields=fields,
            exact=exact,
        )


async def usage_metadata(
    profile: Profile,
    uid: str,
    *,
    page_size: int = 100,
) -> SearchResults:
    """Reverse lookup — find every object that references the given UID.

    Resolves the UID's owning resource via `/api/identifiableObjects/{uid}`,
    then fans out concurrent `/api/<target>?filter=<path>:eq:<uid>` calls
    against every known reference path for that owning type. Useful as a
    deletion-safety probe before `dhis2 metadata patch` / `delete_bulk`.
    """
    async with open_client(profile) as client:
        return await client.metadata.usage(uid, page_size=page_size)


async def get_metadata(
    profile: Profile,
    resource: str,
    uid: str,
    *,
    fields: str | None = None,
) -> BaseModel:
    """Fetch one metadata object by UID; returns the typed generated model."""
    async with open_client(profile) as client:
        accessor = _resolve_accessor(client.resources, resource)
        model: BaseModel = await accessor.get(uid, fields=fields)
        return model


async def patch_metadata(
    profile: Profile,
    resource: str,
    uid: str,
    ops: Sequence[JsonPatchOp | dict[str, Any]],
) -> WebMessageResponse:
    """Apply an RFC 6902 JSON Patch to a single metadata object.

    Wraps `PATCH /api/<resource>/{uid}`. `ops` accepts typed `JsonPatchOp`
    variants (e.g. `ReplaceOp(path="/name", value="New")`) and raw
    `{op, path, ...}` dicts interchangeably — dicts are validated through
    `JsonPatchOpAdapter` at the wire boundary.

    Returns a typed `WebMessageResponse`; read `.import_count()`,
    `.conflicts()`, `.status` as usual.
    """
    async with open_client(profile) as client:
        accessor = _resolve_accessor(client.resources, resource)
        raw = await accessor.patch(uid, ops)
    return WebMessageResponse.model_validate(raw)


def _resolve_accessor(resources: object, resource: str) -> Any:
    """Resolve `client.resources.<attr>` for a resource name; raise UnknownResourceError on miss."""
    attr = _attr_name(resource)
    accessor = getattr(resources, attr, None)
    if accessor is None:
        available = _resource_names(resources)
        raise UnknownResourceError(
            f"unknown metadata resource {resource!r} (tried attribute {attr!r}); "
            f"this instance exposes {len(available)} types — call `list_resource_types` to see them"
        )
    return accessor


async def resolve_option_set_uid(profile: Profile, uid_or_code: str) -> str:
    """Resolve an OptionSet identifier to its DHIS2 UID.

    Accepts either the literal 11-char DHIS2 UID or the business `code`
    the set was registered under. The `code` path hits
    `/api/optionSets?filter=code:eq:{code}` via the accessor; UID inputs
    are returned unchanged (no round-trip).

    Raises `LookupError` if the input is a code that doesn't resolve.
    """
    from dhis2_client.uids import is_valid_uid  # noqa: PLC0415 — local import keeps the main file's surface lean

    if is_valid_uid(uid_or_code):
        return uid_or_code
    async with open_client(profile) as client:
        option_set = await client.option_sets.get_by_code(uid_or_code, include_options=False)
    if option_set is None or option_set.id is None:
        raise LookupError(f"no OptionSet with code {uid_or_code!r} (and not a valid UID)")
    return option_set.id


async def show_option_set(profile: Profile, uid_or_code: str) -> Any:
    """Fetch one OptionSet (with options resolved inline) by UID or business code; None on miss."""
    from dhis2_client.generated.v42.schemas import OptionSet  # noqa: PLC0415
    from dhis2_client.uids import is_valid_uid  # noqa: PLC0415

    async with open_client(profile) as client:
        if is_valid_uid(uid_or_code):
            raw = await client.get_raw(
                f"/api/optionSets/{uid_or_code}",
                params={
                    "fields": "id,code,name,description,valueType,version,options[id,code,name,sortOrder]",
                },
            )
            return OptionSet.model_validate(raw)
        return await client.option_sets.get_by_code(uid_or_code)


async def find_option_in_set(
    profile: Profile,
    *,
    option_set_uid_or_code: str,
    option_code: str | None = None,
    option_name: str | None = None,
) -> Any:
    """Pinpoint a single option inside a set by code or name; None on miss."""
    async with open_client(profile) as client:
        set_uid = await resolve_option_set_uid(profile, option_set_uid_or_code)
        return await client.option_sets.find_option(
            set_uid,
            option_code=option_code,
            option_name=option_name,
        )


async def sync_option_set(
    profile: Profile,
    *,
    option_set_uid_or_code: str,
    spec: Sequence[Any],
    remove_missing: bool = False,
    dry_run: bool = False,
) -> Any:
    """Run `upsert_options` against a set identified by UID or code; return the typed report."""
    async with open_client(profile) as client:
        set_uid = await resolve_option_set_uid(profile, option_set_uid_or_code)
        return await client.option_sets.upsert_options(
            set_uid,
            spec,
            remove_missing=remove_missing,
            dry_run=dry_run,
        )


async def get_option_attribute_value(
    profile: Profile,
    *,
    option_uid: str,
    attribute_code_or_uid: str,
) -> str | None:
    """Read one attribute value off an Option; None if unset."""
    async with open_client(profile) as client:
        return await client.option_sets.get_option_attribute_value(option_uid, attribute_code_or_uid)


async def set_option_attribute_value(
    profile: Profile,
    *,
    option_uid: str,
    attribute_code_or_uid: str,
    value: str,
) -> None:
    """Set / replace one attribute value on an Option (read-merge-write)."""
    async with open_client(profile) as client:
        await client.option_sets.set_option_attribute_value(option_uid, attribute_code_or_uid, value)


async def find_option_by_attribute(
    profile: Profile,
    *,
    option_set_uid_or_code: str,
    attribute_code_or_uid: str,
    value: str,
) -> Any:
    """Reverse lookup: Option in a set whose attribute value matches."""
    async with open_client(profile) as client:
        set_uid = await resolve_option_set_uid(profile, option_set_uid_or_code)
        return await client.option_sets.find_option_by_attribute(
            set_uid,
            attribute_code_or_uid,
            value,
        )


async def get_attribute_value(
    profile: Profile,
    *,
    resource: str,
    resource_uid: str,
    attribute_code_or_uid: str,
) -> str | None:
    """Generic read — any resource with `attributeValues` (DEs, OUs, options, …)."""
    async with open_client(profile) as client:
        return await client.attribute_values.get_value(resource, resource_uid, attribute_code_or_uid)


async def set_attribute_value(
    profile: Profile,
    *,
    resource: str,
    resource_uid: str,
    attribute_code_or_uid: str,
    value: str,
) -> None:
    """Generic set — any resource with `attributeValues` (DEs, OUs, options, …)."""
    async with open_client(profile) as client:
        await client.attribute_values.set_value(resource, resource_uid, attribute_code_or_uid, value)


async def delete_attribute_value(
    profile: Profile,
    *,
    resource: str,
    resource_uid: str,
    attribute_code_or_uid: str,
) -> bool:
    """Generic delete — returns True if an attribute value was removed, False on no-op."""
    async with open_client(profile) as client:
        return await client.attribute_values.delete_value(resource, resource_uid, attribute_code_or_uid)


async def find_resources_by_attribute(
    profile: Profile,
    *,
    resource: str,
    attribute_code_or_uid: str,
    value: str,
    extra_filters: list[str] | None = None,
) -> list[str]:
    """Generic reverse lookup — UIDs of every resource whose attribute matches."""
    async with open_client(profile) as client:
        return await client.attribute_values.find_uids_by_value(
            resource,
            attribute_code_or_uid,
            value,
            extra_filters=extra_filters,
        )


async def show_program_rule(profile: Profile, rule_uid: str) -> Any:
    """Fetch one ProgramRule with actions resolved inline."""
    async with open_client(profile) as client:
        return await client.program_rules.get_rule(rule_uid)


async def list_program_rules(profile: Profile, program_uid: str | None = None) -> list[Any]:
    """List every ProgramRule (optionally scoped to a program) sorted by priority."""
    async with open_client(profile) as client:
        return await client.program_rules.list_rules(program_uid=program_uid)


async def list_program_rule_variables(profile: Profile, program_uid: str) -> list[Any]:
    """List every `ProgramRuleVariable` in scope for a program."""
    async with open_client(profile) as client:
        return await client.program_rules.variables_for(program_uid)


async def validate_program_rule_expression(
    profile: Profile,
    expression: str,
    *,
    context: str = "program-indicator",
) -> Any:
    """Parse-check a program-rule condition expression via DHIS2's description endpoint."""
    from typing import cast  # noqa: PLC0415

    from dhis2_client.validation import ExpressionContext  # noqa: PLC0415

    typed_context = cast(ExpressionContext, context)
    async with open_client(profile) as client:
        return await client.program_rules.validate_expression(expression, context=typed_context)


async def program_rules_using_data_element(profile: Profile, data_element_uid: str) -> list[Any]:
    """Impact analysis: every ProgramRule whose actions reference the DE."""
    async with open_client(profile) as client:
        return await client.program_rules.where_de_is_used(data_element_uid)


async def list_sql_views(profile: Profile, view_type: str | None = None) -> list[Any]:
    """List every SqlView (optionally filtered by type), sorted by name."""
    async with open_client(profile) as client:
        return await client.sql_views.list_views(view_type=view_type)


async def show_sql_view(profile: Profile, view_uid: str) -> Any:
    """Fetch one SqlView, including its `sqlQuery` text."""
    async with open_client(profile) as client:
        return await client.sql_views.get(view_uid)


async def execute_sql_view(
    profile: Profile,
    view_uid: str,
    *,
    variables: Mapping[str, str] | None = None,
    criteria: Mapping[str, str] | None = None,
) -> Any:
    """Execute a SqlView and return its typed `SqlViewResult`."""
    async with open_client(profile) as client:
        return await client.sql_views.execute(view_uid, variables=variables, criteria=criteria)


async def refresh_sql_view(profile: Profile, view_uid: str) -> Any:
    """Refresh a MATERIALIZED_VIEW or lazily create a VIEW's DB object."""
    async with open_client(profile) as client:
        return await client.sql_views.refresh(view_uid)


async def adhoc_sql_view(
    profile: Profile,
    name: str,
    sql: str,
    *,
    view_type: str = "QUERY",
    keep: bool = False,
    variables: Mapping[str, str] | None = None,
) -> Any:
    """Register a throwaway SqlView, execute it once, delete it on the way out."""
    async with open_client(profile) as client:
        kwargs = dict(variables) if variables else {}
        return await client.sql_views.runner.adhoc(
            name,
            sql,
            view_type=view_type,
            keep=keep,
            **kwargs,
        )


async def list_visualizations(profile: Profile, viz_type: str | None = None) -> list[Any]:
    """List every Visualization (optionally filtered by type), sorted by name."""
    async with open_client(profile) as client:
        return await client.visualizations.list_all(viz_type=viz_type)


async def show_visualization(profile: Profile, viz_uid: str) -> Any:
    """Fetch one Visualization with axes + data dimensions resolved inline."""
    async with open_client(profile) as client:
        return await client.visualizations.get(viz_uid)


async def create_visualization(
    profile: Profile,
    *,
    name: str,
    viz_type: str,
    data_elements: Sequence[str],
    periods: Sequence[str],
    organisation_units: Sequence[str],
    description: str | None = None,
    uid: str | None = None,
    category_dimension: str | None = None,
    series_dimension: str | None = None,
    filter_dimension: str | None = None,
) -> Any:
    """Create a Visualization from a typed VisualizationSpec."""
    from dhis2_client import VisualizationSpec  # noqa: PLC0415 — local import to keep import cost low
    from dhis2_client.generated.v42.enums import VisualizationType  # noqa: PLC0415

    spec_kwargs: dict[str, Any] = {
        "name": name,
        "viz_type": VisualizationType(viz_type),
        "data_elements": list(data_elements),
        "periods": list(periods),
        "organisation_units": list(organisation_units),
        "description": description,
        "uid": uid,
    }
    if category_dimension is not None:
        spec_kwargs["category_dimension"] = category_dimension
    if series_dimension is not None:
        spec_kwargs["series_dimension"] = series_dimension
    if filter_dimension is not None:
        spec_kwargs["filter_dimension"] = filter_dimension
    spec = VisualizationSpec.model_validate(spec_kwargs)
    async with open_client(profile) as client:
        return await client.visualizations.create_from_spec(spec)


async def clone_visualization(
    profile: Profile,
    source_uid: str,
    *,
    new_name: str,
    new_uid: str | None = None,
    new_description: str | None = None,
) -> Any:
    """Duplicate a Visualization with a fresh UID + new name."""
    async with open_client(profile) as client:
        return await client.visualizations.clone(
            source_uid,
            new_name=new_name,
            new_uid=new_uid,
            new_description=new_description,
        )


async def delete_visualization(profile: Profile, viz_uid: str) -> None:
    """DELETE a Visualization by UID."""
    async with open_client(profile) as client:
        await client.visualizations.delete(viz_uid)


async def list_dashboards(profile: Profile) -> list[Any]:
    """List every Dashboard on the instance, sorted by name."""
    async with open_client(profile) as client:
        return await client.dashboards.list_all()


async def show_dashboard(profile: Profile, dashboard_uid: str) -> Any:
    """Fetch one Dashboard with every item resolved inline."""
    async with open_client(profile) as client:
        return await client.dashboards.get(dashboard_uid)


async def dashboard_add_item(
    profile: Profile,
    dashboard_uid: str,
    target_uid: str,
    *,
    kind: str = "visualization",
    x: int | None = None,
    y: int | None = None,
    width: int | None = None,
    height: int | None = None,
) -> Any:
    """Add a metadata-backed item (viz / map / event chart / …) to a dashboard."""
    from typing import cast  # noqa: PLC0415

    from dhis2_client import DashboardSlot  # noqa: PLC0415
    from dhis2_client.dashboards import DashboardItemKind  # noqa: PLC0415

    slot: DashboardSlot | None = None
    if any(v is not None for v in (x, y, width, height)):
        slot = DashboardSlot(
            x=x if x is not None else 0,
            y=y if y is not None else 0,
            width=width if width is not None else 60,
            height=height if height is not None else 20,
        )
    async with open_client(profile) as client:
        return await client.dashboards.add_item(
            dashboard_uid,
            target_uid,
            kind=cast(DashboardItemKind, kind),
            slot=slot,
        )


async def dashboard_remove_item(profile: Profile, dashboard_uid: str, item_uid: str) -> Any:
    """Remove one dashboard item by its UID."""
    async with open_client(profile) as client:
        return await client.dashboards.remove_item(dashboard_uid, item_uid)


async def list_maps(profile: Profile) -> list[Any]:
    """List every Map on the instance, sorted by name."""
    async with open_client(profile) as client:
        return await client.maps.list_all()


async def show_map(profile: Profile, map_uid: str) -> Any:
    """Fetch one Map with every mapViews layer resolved inline."""
    async with open_client(profile) as client:
        return await client.maps.get(map_uid)


async def create_map(
    profile: Profile,
    *,
    name: str,
    data_elements: Sequence[str],
    periods: Sequence[str],
    organisation_units: Sequence[str],
    organisation_unit_levels: Sequence[int],
    description: str | None = None,
    uid: str | None = None,
    longitude: float = 15.0,
    latitude: float = 0.0,
    zoom: int = 4,
    basemap: str = "openStreetMap",
    classes: int = 5,
    color_low: str = "#fef0d9",
    color_high: str = "#b30000",
) -> Any:
    """Create a single-layer thematic choropleth Map from flags."""
    from dhis2_client import MapLayerSpec, MapSpec  # noqa: PLC0415

    spec = MapSpec(
        name=name,
        description=description,
        uid=uid,
        longitude=longitude,
        latitude=latitude,
        zoom=zoom,
        basemap=basemap,
        layers=[
            MapLayerSpec(
                layer_kind="thematic",
                data_elements=list(data_elements),
                periods=list(periods),
                organisation_units=list(organisation_units),
                organisation_unit_levels=list(organisation_unit_levels),
                classes=classes,
                color_low=color_low,
                color_high=color_high,
            ),
        ],
    )
    async with open_client(profile) as client:
        return await client.maps.create_from_spec(spec)


async def clone_map(
    profile: Profile,
    source_uid: str,
    *,
    new_name: str,
    new_uid: str | None = None,
    new_description: str | None = None,
) -> Any:
    """Duplicate a Map with a fresh UID + new name."""
    async with open_client(profile) as client:
        return await client.maps.clone(
            source_uid,
            new_name=new_name,
            new_uid=new_uid,
            new_description=new_description,
        )


async def delete_map(profile: Profile, map_uid: str) -> None:
    """DELETE a Map by UID."""
    async with open_client(profile) as client:
        await client.maps.delete(map_uid)


# ---------------------------------------------------------------------------
# OrganisationUnitGroupSet / OrganisationUnitGroup introspection
# ---------------------------------------------------------------------------

# These reads feed the `dhis2 metadata ou-groups ...` verbs. DHIS2 already
# exposes the resources via the generic `metadata list` path, but knowing
# how many OUs each group contains + resolving the group→members relation
# in one pass is the workflow gap this sub-app closes.


async def list_ou_group_sets(profile: Profile) -> list[dict[str, Any]]:
    """List every OrganisationUnitGroupSet with its groups resolved inline.

    Returns a list of dicts (the JSON boundary with `extra="allow"`-style
    shape that `/api/organisationUnitGroupSets` emits). The CLI renderer
    expects `id`, `name`, `code`, and an `organisationUnitGroups` list
    with `id` + `name` for each referenced group.
    """
    async with open_client(profile) as client:
        raw = await client.get_raw(
            "/api/organisationUnitGroupSets",
            params={
                "fields": "id,name,code,description,organisationUnitGroups[id,name]",
                "paging": "false",
            },
        )
    return list(raw.get("organisationUnitGroupSets") or [])


async def show_ou_group_set(profile: Profile, group_set_uid: str) -> dict[str, Any]:
    """Fetch one OrganisationUnitGroupSet with its groups + per-group member count.

    Two round-trips: the group-set itself (one shot), then one
    `organisationUnits:count` call per referenced group. Gives a
    reporting-friendly "how many OUs in each slice?" view without
    needing the analytics API.
    """
    async with open_client(profile) as client:
        group_set = await client.get_raw(
            f"/api/organisationUnitGroupSets/{group_set_uid}",
            params={"fields": "id,name,code,description,organisationUnitGroups[id,name,code]"},
        )
        groups = list(group_set.get("organisationUnitGroups") or [])
        for group in groups:
            gid = group.get("id")
            if not isinstance(gid, str):
                group["memberCount"] = 0
                continue
            members = await client.get_raw(
                f"/api/organisationUnitGroups/{gid}",
                params={"fields": "id,organisationUnits~size"},
            )
            size_raw = members.get("organisationUnits")
            try:
                group["memberCount"] = int(size_raw) if isinstance(size_raw, int | str) else 0
            except (TypeError, ValueError):
                group["memberCount"] = 0
    return group_set


async def list_ou_group_members(
    profile: Profile,
    group_uid: str,
    *,
    page_size: int = 50,
    page: int = 1,
) -> dict[str, Any]:
    """List organisation units that are members of one OrganisationUnitGroup.

    Paged for groups with hundreds or thousands of members (province
    groupings in large countries). Hits the OU list endpoint with a
    `organisationUnitGroups.id:eq:<uid>` filter — DHIS2 supports
    server-side paging there out of the box. Returns the raw pager
    envelope so the CLI can render pagination metadata alongside rows.
    """
    async with open_client(profile) as client:
        raw = await client.get_raw(
            "/api/organisationUnits",
            params={
                "filter": f"organisationUnitGroups.id:eq:{group_uid}",
                "fields": "id,name,code,level,path",
                "pageSize": str(page_size),
                "page": str(page),
            },
        )
    return raw
