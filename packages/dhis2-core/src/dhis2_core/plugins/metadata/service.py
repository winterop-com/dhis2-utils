"""Service layer for the `metadata` plugin — thin wrapper over generated resources."""

from __future__ import annotations

import re
from collections.abc import AsyncIterator, Mapping
from typing import Any

from dhis2_client import WebMessageResponse
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
