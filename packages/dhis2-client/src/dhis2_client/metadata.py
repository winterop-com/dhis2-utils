"""`Dhis2Client.metadata` — bulk operations over `/api/metadata`.

One accessor for bulk-write paths that don't have a typed generated CRUD
entry (generated resources cover the per-UID `GET / POST / PUT / PATCH /
DELETE` surface per resource type). Covers:

- `delete_bulk` / `delete_bulk_multi` — fast-delete via `importStrategy=DELETE`.
- `dry_run` — validate a cross-resource bundle without committing
  (`importMode=VALIDATE`).

For typed bulk writes scoped to a single resource, reach for the generated
per-resource accessor's `save_bulk` method
(`client.resources.data_elements.save_bulk([DataElement(...), ...])`) —
IDE autocomplete gives you model-typed input on that path.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

from dhis2_client.envelopes import WebMessageResponse
from dhis2_client.generated.v42.oas import Status

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


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


__all__ = ["MetadataAccessor"]
