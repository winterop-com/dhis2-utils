"""Service layer for the `metadata` plugin — thin wrapper over generated resources."""

from __future__ import annotations

import re
from collections.abc import AsyncIterator, Iterator, Mapping
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

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile

_CAMEL_RE = re.compile(r"(?<!^)(?=[A-Z])")
_STREAM_PAGE_SIZE = 500

# Metadata-wide keys in a /api/metadata export that aren't resource collections
# — skipping them lets callers iterate only over real metadata types.
_BUNDLE_META_KEYS = frozenset({"system", "date"})


class UnknownResourceError(LookupError):
    """Raised when a caller asks for a metadata resource not present on this instance."""


def _attr_name(resource: str) -> str:
    """Convert a DHIS2 resource name (camelCase plural) to a Resources attribute name."""
    return _CAMEL_RE.sub("_", resource).lower()


def _resource_names(resources: object) -> list[str]:
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
) -> list[dict[str, Any]]:
    """List a metadata resource (e.g. `dataElements`, `indicators`).

    Every DHIS2 `/api/<resource>` query parameter is forwarded. `filters` and
    `order` may repeat — a list of strings becomes `?filter=a&filter=b`.
    `root_junction` is `"AND"` (default) or `"OR"`. `paging=False` returns the
    full catalog in one response; for memory-friendly streaming use
    `iter_metadata`.

    Returns dumped-dict form so MCP tool calls can serialise the result.
    """
    async with open_client(profile) as client:
        accessor = _resolve_accessor(client.resources, resource)
        models = await accessor.list(
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
        return [_dump(model) for model in models]


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
) -> AsyncIterator[dict[str, Any]]:
    """Stream every row of a metadata resource as dumped dicts, one at a time.

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
                yield _dump(model)
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
) -> dict[str, Any]:
    """Download a metadata bundle from `GET /api/metadata`.

    `resources` limits the export to specific types (e.g. `["dataElements",
    "indicators"]`); omit for everything. `fields` is the standard DHIS2
    selector — `":owner"` (the default DHIS2 uses internally for
    cross-instance imports) preserves every field required for a faithful
    round-trip, while `:identifiable` / `:all` / a custom list give tighter
    control.

    Returns the raw bundle dict. The resource-collection keys (e.g.
    `dataElements`) live alongside metadata-wide `system` + `date` fields —
    call `iter_bundle_resources` to walk just the resource collections.
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
    async with open_client(profile) as client:
        return await client.get_raw("/api/metadata", params=params)


async def import_metadata(
    profile: Profile,
    bundle: Mapping[str, Any],
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
        raw = await client.post_raw("/api/metadata", dict(bundle), params=params)
    return WebMessageResponse.model_validate(raw)


def iter_bundle_resources(bundle: Mapping[str, Any]) -> Iterator[tuple[str, list[dict[str, Any]]]]:
    """Iterate over resource collections in a bundle — yields `(resource, [items])` pairs.

    Skips `system` and `date` (metadata-wide fields, not resource collections).
    Returns the collections in the order DHIS2 emits them, which is dependency-safe
    — caller can re-POST them individually without violating FK constraints.
    """
    for key, value in bundle.items():
        if key in _BUNDLE_META_KEYS:
            continue
        if isinstance(value, list):
            yield key, value


def summarise_bundle(bundle: Mapping[str, Any]) -> dict[str, int]:
    """Return a `{resource: count}` summary of a bundle — useful for CLI output."""
    return {
        key: len(value) for key, value in bundle.items() if key not in _BUNDLE_META_KEYS and isinstance(value, list)
    }


async def get_metadata(
    profile: Profile,
    resource: str,
    uid: str,
    *,
    fields: str | None = None,
) -> dict[str, Any]:
    """Fetch one metadata object by UID; returns the dumped-dict form."""
    async with open_client(profile) as client:
        accessor = _resolve_accessor(client.resources, resource)
        model = await accessor.get(uid, fields=fields)
        return _dump(model)


def _resolve_accessor(resources: object, resource: str) -> Any:
    attr = _attr_name(resource)
    accessor = getattr(resources, attr, None)
    if accessor is None:
        available = _resource_names(resources)
        raise UnknownResourceError(
            f"unknown metadata resource {resource!r} (tried attribute {attr!r}); "
            f"this instance exposes {len(available)} types — call `list_resource_types` to see them"
        )
    return accessor


def _dump(model: Any) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        dumped = model.model_dump(by_alias=True, exclude_none=True, mode="json")
        if isinstance(dumped, dict):
            return dumped
    if isinstance(model, dict):
        return model
    raise TypeError(f"cannot dump {type(model).__name__} to a dict")
