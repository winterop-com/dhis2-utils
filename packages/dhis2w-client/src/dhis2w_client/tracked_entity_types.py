"""TrackedEntityType authoring — `Dhis2Client.tracked_entity_types`.

A `TrackedEntityType` is the kind of subject a tracker program enrols
(Person, Case, Animal). Each TET carries its own set of attributes
via `trackedEntityTypeAttributes[]` — a join table that flags which
TEAs are mandatory, searchable, and visible in the enrollment UI.

- `create(...)` — named kwargs over the minimal required subset
  (`name`, `short_name`) plus common knobs (`description`,
  `allow_audit_log`, `feature_type`,
  `min_attributes_required_to_search`).
- `add_attribute(tet_uid, tea_uid, *, mandatory=False,
  searchable=False, display_in_list=True)` — wire a TEA onto the TET
  by round-tripping the full TET, mutating
  `trackedEntityTypeAttributes[]`, and PUTing back. Mirrors DataSet +
  DataSetElement.
- `remove_attribute(tet_uid, tea_uid)` — drops the TEA ref from the TET.
- `rename(uid, ...)` / `delete(uid)` — standard edit pathways.

No `*Spec` builder — continues the spec-audit data point.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2w_client.generated.v42.schemas import TrackedEntityType

if TYPE_CHECKING:
    from dhis2w_client.client import Dhis2Client
from dhis2w_client.envelopes import WebMessageResponse

_TET_FIELDS: str = (
    "id,name,shortName,code,formName,description,"
    "allowAuditLog,featureType,maxTeiCountToReturn,minAttributesRequiredToSearch,"
    "trackedEntityTypeAttributes["
    "trackedEntityAttribute[id,name,valueType],mandatory,searchable,displayInList"
    "]"
)


class TrackedEntityTypesAccessor:
    """`Dhis2Client.tracked_entity_types` — CRUD + attribute-linkage helpers."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> list[TrackedEntityType]:
        """Page through TrackedEntityTypes."""
        raw = await self._client.get_raw(
            "/api/trackedEntityTypes",
            params={
                "fields": _TET_FIELDS,
                "page": str(page),
                "pageSize": str(page_size),
            },
        )
        rows = raw.get("trackedEntityTypes") or []
        return [TrackedEntityType.model_validate(row) for row in rows if isinstance(row, dict)]

    async def get(self, uid: str) -> TrackedEntityType:
        """Fetch one TrackedEntityType with its TEA link table resolved inline."""
        return await self._client.get(
            f"/api/trackedEntityTypes/{uid}", model=TrackedEntityType, params={"fields": _TET_FIELDS}
        )

    async def create(
        self,
        *,
        name: str,
        short_name: str,
        description: str | None = None,
        code: str | None = None,
        form_name: str | None = None,
        allow_audit_log: bool | None = None,
        feature_type: str | None = None,
        min_attributes_required_to_search: int | None = None,
        max_tei_count_to_return: int | None = None,
        uid: str | None = None,
    ) -> TrackedEntityType:
        """Create a TrackedEntityType.

        `allow_audit_log` enables the per-TEI audit trail (required for
        compliance workflows). `feature_type` governs the geometry
        attached to each TEI (`NONE` / `POINT` / `POLYGON`).
        `min_attributes_required_to_search` sets the enrollment-search
        minimum attribute count; higher values reduce accidental
        full-table scans.
        """
        payload: dict[str, Any] = {"name": name, "shortName": short_name}
        if description:
            payload["description"] = description
        if code:
            payload["code"] = code
        if form_name:
            payload["formName"] = form_name
        if allow_audit_log is not None:
            payload["allowAuditLog"] = allow_audit_log
        if feature_type:
            payload["featureType"] = feature_type
        if min_attributes_required_to_search is not None:
            payload["minAttributesRequiredToSearch"] = min_attributes_required_to_search
        if max_tei_count_to_return is not None:
            payload["maxTeiCountToReturn"] = max_tei_count_to_return
        if uid:
            payload["id"] = uid
        envelope = await self._client.post("/api/trackedEntityTypes", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("tracked-entity-type create did not return a uid")
        return await self.get(created_uid)

    async def update(self, tet: TrackedEntityType) -> TrackedEntityType:
        """PUT an edited TrackedEntityType back. `tet.id` must be set."""
        if not tet.id:
            raise ValueError("update requires tet.id to be set")
        body = tet.model_dump(by_alias=True, exclude_none=True, mode="json")
        _strip_self_ref_from_teta(body)
        await self._client.put_raw(f"/api/trackedEntityTypes/{tet.id}", body=body)
        return await self.get(tet.id)

    async def rename(
        self,
        uid: str,
        *,
        name: str | None = None,
        short_name: str | None = None,
        form_name: str | None = None,
        description: str | None = None,
    ) -> TrackedEntityType:
        """Partial-update shortcut — read, mutate the label fields, PUT."""
        if name is None and short_name is None and form_name is None and description is None:
            raise ValueError("rename requires at least one of name / short_name / form_name / description")
        current = await self.get(uid)
        if name is not None:
            current.name = name
        if short_name is not None:
            current.shortName = short_name
        if form_name is not None:
            current.formName = form_name
        if description is not None:
            current.description = description
        return await self.update(current)

    async def add_attribute(
        self,
        tet_uid: str,
        attribute_uid: str,
        *,
        mandatory: bool = False,
        searchable: bool = False,
        display_in_list: bool = True,
    ) -> TrackedEntityType:
        """Wire a TrackedEntityAttribute onto the TET.

        DHIS2 stores the link in `trackedEntityTypeAttributes[]` as a
        nested join object — the accessor round-trips the full TET,
        appends a new entry, and PUTs it back.
        """
        current = await self.get(tet_uid)
        raw = current.model_dump(by_alias=True, exclude_none=True, mode="json")
        _strip_self_ref_from_teta(raw)
        existing = raw.get("trackedEntityTypeAttributes") or []
        if any(
            (entry.get("trackedEntityAttribute") or {}).get("id") == attribute_uid
            for entry in existing
            if isinstance(entry, dict)
        ):
            return current
        existing.append(
            {
                "trackedEntityAttribute": {"id": attribute_uid},
                "mandatory": mandatory,
                "searchable": searchable,
                "displayInList": display_in_list,
            },
        )
        raw["trackedEntityTypeAttributes"] = existing
        await self._client.put_raw(f"/api/trackedEntityTypes/{tet_uid}", body=raw)
        return await self.get(tet_uid)

    async def remove_attribute(self, tet_uid: str, attribute_uid: str) -> TrackedEntityType:
        """Drop a TrackedEntityAttribute from the TET's link table."""
        current = await self.get(tet_uid)
        raw = current.model_dump(by_alias=True, exclude_none=True, mode="json")
        _strip_self_ref_from_teta(raw)
        existing = raw.get("trackedEntityTypeAttributes") or []
        filtered = [
            entry
            for entry in existing
            if isinstance(entry, dict) and (entry.get("trackedEntityAttribute") or {}).get("id") != attribute_uid
        ]
        if len(filtered) == len(existing):
            return current
        raw["trackedEntityTypeAttributes"] = filtered
        await self._client.put_raw(f"/api/trackedEntityTypes/{tet_uid}", body=raw)
        return await self.get(tet_uid)

    async def delete(self, uid: str) -> None:
        """Delete a TrackedEntityType — DHIS2 rejects deletes on TETs in use by enrolled TEIs."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.tracked_entity_types.delete(uid)


def _strip_self_ref_from_teta(payload: dict[str, Any]) -> None:
    """Drop the self-referencing `trackedEntityType` field from each TETA entry.

    DHIS2's `/api/trackedEntityTypes/{uid}` read embeds
    `trackedEntityTypeAttributes[].trackedEntityType = {id: <parent>}`;
    its importer rejects the PUT with a self-reference conflict. Mirrors
    the DataSetElement self-ref workaround.
    """
    entries = payload.get("trackedEntityTypeAttributes")
    if not isinstance(entries, list):
        return
    cleaned: list[dict[str, Any]] = []
    for entry in entries:
        if isinstance(entry, dict):
            cleaned.append({k: v for k, v in entry.items() if k != "trackedEntityType"})
    payload["trackedEntityTypeAttributes"] = cleaned


__all__ = [
    "TrackedEntityType",
    "TrackedEntityTypesAccessor",
]
