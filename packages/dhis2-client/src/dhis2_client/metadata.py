"""`Dhis2Client.metadata` — bulk operations over `/api/metadata`.

One accessor for bulk-write paths that don't have a typed generated CRUD
entry (generated resources cover the per-UID `GET / POST / PUT / PATCH /
DELETE` surface per resource type). Covers:

- `delete_bulk` / `delete_bulk_multi` — fast-delete via `importStrategy=DELETE`.
- `dry_run` — validate a cross-resource bundle without committing
  (`importMode=VALIDATE`).
- `search` — cross-resource metadata search. Fans out three concurrent
  `/api/metadata?filter=<field>:ilike:<q>` calls (one per match axis:
  `id`, `code`, `name`) and merges the results with UID dedup. DHIS2's
  `/api/metadata` silently ignores `rootJunction` and ANDs multiple
  filters (see BUGS.md #29), so OR-across-fields needs N requests.
  Trading three HTTP round-trips for partial-UID + partial-code +
  substring-name matching in a single verb.

For typed bulk writes scoped to a single resource, reach for the generated
per-resource accessor's `save_bulk` method
(`client.resources.data_elements.save_bulk([DataElement(...), ...])`) —
IDE autocomplete gives you model-typed input on that path.
"""

from __future__ import annotations

import asyncio
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, Field

from dhis2_client.envelopes import WebMessageResponse
from dhis2_client.generated.v42.oas import Status

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client

# Match axes for `MetadataAccessor.search` — one `/api/metadata?filter=X:ilike:<q>`
# call per entry, results merged and deduplicated by UID.
_SEARCH_FIELDS: tuple[str, ...] = ("id", "code", "name")


class SearchHit(BaseModel):
    """One matching metadata object returned by `MetadataAccessor.search`."""

    model_config = ConfigDict(frozen=True)

    uid: str
    name: str
    code: str | None = None
    resource: str = Field(..., description="DHIS2 resource plural (e.g. 'dataElements', 'dashboards')")
    href: str | None = None


class SearchResults(BaseModel):
    """Grouped results from `MetadataAccessor.search` — one list per resource type.

    `hits` maps each DHIS2 resource plural (`dataElements`, `indicators`,
    `dashboards`, …) to the matching objects within that resource. Empty
    resources are omitted, so `SearchResults.total` plus
    `hits.keys()` answer "which resource types matched" in one look.
    """

    model_config = ConfigDict(frozen=True)

    query: str
    hits: dict[str, list[SearchHit]] = Field(default_factory=dict)

    @property
    def total(self) -> int:
        """Total hits across every resource type."""
        return sum(len(rows) for rows in self.hits.values())

    def flat(self) -> list[SearchHit]:
        """Return every hit as a flat list — convenient for sorted/ranked display."""
        return [hit for rows in self.hits.values() for hit in rows]


class MetadataAccessor:
    """Bulk metadata operations on `/api/metadata`.

    Per-resource CRUD lives on the generated `client.resources.<Resource>`
    accessors (one class per DHIS2 resource type, auto-generated from
    `/api/schemas`). This accessor is specifically for the
    multi-resource / multi-UID paths that need the `/api/metadata`
    bundle endpoint — they don't fit the single-resource accessor shape.
    """

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def search(
        self,
        query: str,
        *,
        page_size: int = 50,
    ) -> SearchResults:
        """Cross-resource metadata search — UID / code / name ilike, OR-merged.

        Fans out `len(_SEARCH_FIELDS)` concurrent `/api/metadata` calls, one
        per match axis (`id`, `code`, `name`), each filtered as
        `<field>:ilike:<query>`. DHIS2 returns a bundle
        `{dataElements: [...], indicators: [...], ...}` per call grouped
        by resource type; this method merges them, deduplicating by
        `(resource, uid)` so an object matching on both id and name
        doesn't appear twice.

        Works uniformly for:

        - **Full UID** — id:ilike hits the exact record, the other axes
          usually miss; result is one hit.
        - **Partial UID** — id:ilike:<prefix> matches every UID starting
          with or containing the substring across every resource.
        - **Code lookup** — code:ilike:<fragment> matches on the business
          identifier; indicators / DEs often carry meaningful codes.
        - **Name substring** — name:ilike:<fragment> is the broadest
          match and usually dominates the result set.

        A single `rootJunction=OR` call would be cleaner, but DHIS2's
        `/api/metadata` endpoint silently ignores `rootJunction` and
        ANDs multiple filters (BUGS.md #29), so N requests are the only
        way to get cross-field OR.
        """
        field_results = await asyncio.gather(
            *(self._search_one_field(field, query, page_size=page_size) for field in _SEARCH_FIELDS),
        )
        return _merge_search_results(query, field_results)

    async def _search_one_field(self, field: str, query: str, *, page_size: int) -> SearchResults:
        """Issue one `/api/metadata?filter=<field>:ilike:<query>` call."""
        params: dict[str, Any] = {
            "filter": f"{field}:ilike:{query}",
            "fields": "id,name,code,href",
            "pageSize": page_size,
        }
        raw = await self._client.get_raw("/api/metadata", params=params)
        return _search_results_from_bundle(query, raw)

    async def delete_bulk(self, resource_type: str, uids: Sequence[str]) -> WebMessageResponse:
        """Delete every UID in `uids` from one DHIS2 resource type in a single request.

        Wraps `POST /api/metadata?importStrategy=DELETE&atomicMode=NONE` with a
        minimal `{resource_type: [{"id": uid}, ...]}` bundle. Returns the
        `WebMessageResponse` envelope — `.import_count().deleted` reports the
        total rows deleted; `.conflicts()` lists anything DHIS2 refused
        (foreign-key constraints, soft-delete protection, etc.).

        `atomicMode=NONE` lets partial failures through: some UIDs deleted,
        some held back with a conflict. Switch to `delete_bulk_multi` with
        atomic semantics when every row must delete or none should.
        Empty `uids` short-circuits with a no-op envelope (no HTTP call).
        """
        return await self.delete_bulk_multi({resource_type: list(uids)})

    async def delete_bulk_multi(
        self,
        by_resource: Mapping[str, Sequence[str]],
        *,
        atomic_mode: str = "NONE",
    ) -> WebMessageResponse:
        """Delete across multiple resource types in one `/api/metadata` call.

        `by_resource` maps each resource type (e.g. `"dataElements"`,
        `"indicators"`) to the UIDs to delete for that type. Entries with
        empty UID lists are skipped. `atomic_mode` controls DHIS2's
        partial-failure behaviour: `"NONE"` (default) lets individual
        conflicts through, `"ALL"` rolls the entire bundle back on any
        conflict.
        """
        bundle: dict[str, list[dict[str, str]]] = {
            resource: [{"id": uid} for uid in uids] for resource, uids in by_resource.items() if uids
        }
        if not bundle:
            return WebMessageResponse(status=Status.OK, httpStatus="OK", httpStatusCode=200, message="no uids supplied")
        raw = await self._client.post_raw(
            "/api/metadata",
            body=bundle,
            params={"importStrategy": "DELETE", "atomicMode": atomic_mode},
        )
        return WebMessageResponse.model_validate(raw)

    async def dry_run(
        self,
        by_resource: Mapping[str, Sequence[BaseModel | dict[str, Any]]],
        *,
        import_strategy: str = "CREATE_AND_UPDATE",
    ) -> WebMessageResponse:
        """Validate a cross-resource bundle without committing (`importMode=VALIDATE`).

        `by_resource` maps each resource type (e.g. `"dataElements"`,
        `"indicators"`) to the objects that would be imported. Objects can be
        typed pydantic models (auto-dumped via `by_alias + exclude_none`) or
        raw dicts (pass-through). Empty resource entries are skipped.

        Returns the `WebMessageResponse` DHIS2 would have returned on a real
        import — `.import_report().stats` carries the per-type
        created/updated counts; `.conflicts()` lists everything DHIS2 would
        have rejected. Useful as a safety gate in a CI pipeline before a
        real bulk write, or before `delete_bulk` on resources with
        foreign-key dependencies.
        """
        bundle = _bundle_from_by_resource(by_resource)
        if not bundle:
            return WebMessageResponse(
                status=Status.OK, httpStatus="OK", httpStatusCode=200, message="no items supplied"
            )
        raw = await self._client.post_raw(
            "/api/metadata",
            body=bundle,
            params={"importStrategy": import_strategy, "importMode": "VALIDATE"},
        )
        return WebMessageResponse.model_validate(raw)


# Non-metadata keys DHIS2 always includes on an `/api/metadata` response.
# Skip them when enumerating resource sections.
_NON_RESOURCE_KEYS: frozenset[str] = frozenset({"system", "date"})


def _merge_search_results(query: str, per_field: Sequence[SearchResults]) -> SearchResults:
    """OR-merge per-field `SearchResults`, deduplicating by (resource, uid)."""
    merged: dict[str, dict[str, SearchHit]] = {}
    for field_result in per_field:
        for resource, rows in field_result.hits.items():
            slot = merged.setdefault(resource, {})
            for hit in rows:
                slot.setdefault(hit.uid, hit)
    ordered: dict[str, list[SearchHit]] = {
        resource: list(uid_map.values()) for resource, uid_map in sorted(merged.items()) if uid_map
    }
    return SearchResults(query=query, hits=ordered)


def _search_results_from_bundle(query: str, bundle: dict[str, Any]) -> SearchResults:
    """Convert a `/api/metadata` bundle response into a typed `SearchResults`."""
    hits: dict[str, list[SearchHit]] = {}
    for resource, rows in bundle.items():
        if resource in _NON_RESOURCE_KEYS or not isinstance(rows, list):
            continue
        resource_hits: list[SearchHit] = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            uid = row.get("id")
            if not isinstance(uid, str):
                continue
            resource_hits.append(
                SearchHit(
                    uid=uid,
                    name=str(row.get("name") or row.get("displayName") or uid),
                    code=row.get("code") if isinstance(row.get("code"), str) else None,
                    resource=resource,
                    href=row.get("href") if isinstance(row.get("href"), str) else None,
                ),
            )
        if resource_hits:
            hits[resource] = resource_hits
    return SearchResults(query=query, hits=hits)


def _bundle_from_by_resource(
    by_resource: Mapping[str, Sequence[BaseModel | dict[str, Any]]],
) -> dict[str, list[dict[str, Any]]]:
    """Normalise a `{resource: [models|dicts]}` map to DHIS2's wire bundle shape."""
    return {
        resource: [
            item.model_dump(by_alias=True, exclude_none=True, mode="json")
            if isinstance(item, BaseModel)
            else dict(item)
            for item in items
        ]
        for resource, items in by_resource.items()
        if items
    }


__all__ = ["MetadataAccessor", "SearchHit", "SearchResults"]
