"""TrackedEntityAttribute authoring — `Dhis2Client.tracked_entity_attributes`.

`TrackedEntityAttribute`s are the atomic fields on a tracked entity
(National ID, Given Name, Date of Birth, …). They get wired into a
TrackedEntityType (via `trackedEntityTypeAttributes[]`) and/or into
programs (via `programTrackedEntityAttributes[]`).

This module adds the CRUD primitives — the run / write side lives on
`Dhis2Client.tracker` (the existing tracker write plugin).

- `create(...)` — named kwargs over the minimal required subset
  (`name`, `short_name`, `value_type`, `aggregation_type`) plus the
  optional references (`option_set_uid`, `legend_set_uids`) and the
  common toggles (`unique`, `generated`, `confidential`, `inherit`,
  `display_in_list_no_program`, `pattern`).
- `update(tea)` / `rename(uid, ...)` — standard edit pathways.
- `delete(uid)` — DHIS2 rejects deletes on TEAs in use.

No `*Spec` builder — continues the spec-audit data point.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from dhis2w_client.generated.v43.enums import AggregationType, ValueType
from dhis2w_client.generated.v43.schemas import TrackedEntityAttribute

if TYPE_CHECKING:
    from dhis2w_client.v43.client import Dhis2Client
from dhis2w_client.v43.envelopes import WebMessageResponse

_TEA_FIELDS: str = (
    "id,name,shortName,code,formName,description,valueType,aggregationType,"
    "optionSet[id,name,code],legendSets[id,name],"
    "unique,generated,confidential,inherit,"
    "displayInListNoProgram,orgunitScope,pattern,fieldMask"
)


class TrackedEntityAttributesAccessor:
    """`Dhis2Client.tracked_entity_attributes` — CRUD over `/api/trackedEntityAttributes`."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(
        self,
        *,
        value_type: ValueType | str | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> list[TrackedEntityAttribute]:
        """Page through TrackedEntityAttributes, optionally filtered by valueType."""
        filters: list[str] | None = None
        if value_type is not None:
            value = value_type.value if isinstance(value_type, ValueType) else value_type
            filters = [f"valueType:eq:{value}"]
        return cast(
            list[TrackedEntityAttribute],
            await self._client.resources.tracked_entity_attributes.list(
                fields=_TEA_FIELDS,
                filters=filters,
                page=page,
                page_size=page_size,
            ),
        )

    async def get(self, uid: str) -> TrackedEntityAttribute:
        """Fetch one TrackedEntityAttribute with its optionSet + legendSet refs inline."""
        return await self._client.get(
            f"/api/trackedEntityAttributes/{uid}", model=TrackedEntityAttribute, params={"fields": _TEA_FIELDS}
        )

    async def create(
        self,
        *,
        name: str,
        short_name: str,
        value_type: ValueType | str = ValueType.TEXT,
        aggregation_type: AggregationType | str = AggregationType.NONE,
        option_set_uid: str | None = None,
        legend_set_uids: list[str] | None = None,
        unique: bool = False,
        generated: bool = False,
        confidential: bool = False,
        inherit: bool = False,
        display_in_list_no_program: bool = False,
        orgunit_scope: bool = False,
        pattern: str | None = None,
        field_mask: str | None = None,
        code: str | None = None,
        form_name: str | None = None,
        description: str | None = None,
        uid: str | None = None,
    ) -> TrackedEntityAttribute:
        """Create a TrackedEntityAttribute.

        `value_type` defaults to `TEXT`; switch to `NUMBER`, `DATE`,
        `PHONE_NUMBER`, etc. via the `ValueType` StrEnum. `unique=True`
        makes the value unique across the instance (National ID,
        passport number). `generated=True` + `pattern` lets DHIS2
        auto-generate the value when a TEI is registered (common for
        case IDs). `option_set_uid` constrains to an option-set
        picklist. `confidential=True` tags the attribute as sensitive
        for audit + sharing policies.
        """
        payload: dict[str, Any] = {
            "name": name,
            "shortName": short_name,
            "valueType": value_type.value if isinstance(value_type, ValueType) else value_type,
            "aggregationType": (
                aggregation_type.value if isinstance(aggregation_type, AggregationType) else aggregation_type
            ),
            "unique": unique,
            "generated": generated,
            "confidential": confidential,
            "inherit": inherit,
            "displayInListNoProgram": display_in_list_no_program,
            "orgunitScope": orgunit_scope,
        }
        if option_set_uid:
            payload["optionSet"] = {"id": option_set_uid}
        if legend_set_uids:
            payload["legendSets"] = [{"id": uid_} for uid_ in legend_set_uids]
        if uid:
            payload["id"] = uid
        if code:
            payload["code"] = code
        if form_name:
            payload["formName"] = form_name
        if description:
            payload["description"] = description
        if pattern:
            payload["pattern"] = pattern
        if field_mask:
            payload["fieldMask"] = field_mask
        envelope = await self._client.post("/api/trackedEntityAttributes", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("tracked-entity-attribute create did not return a uid")
        return await self.get(created_uid)

    async def update(self, attribute: TrackedEntityAttribute) -> TrackedEntityAttribute:
        """PUT an edited TrackedEntityAttribute back. `attribute.id` must be set."""
        if not attribute.id:
            raise ValueError("update requires attribute.id to be set")
        body = attribute.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/trackedEntityAttributes/{attribute.id}", body=body)
        return await self.get(attribute.id)

    async def rename(
        self,
        uid: str,
        *,
        name: str | None = None,
        short_name: str | None = None,
        form_name: str | None = None,
        description: str | None = None,
    ) -> TrackedEntityAttribute:
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

    async def delete(self, uid: str) -> None:
        """Delete a TrackedEntityAttribute — DHIS2 rejects deletes on TEAs wired into a TET or program."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.tracked_entity_attributes.delete(uid)


__all__ = [
    "TrackedEntityAttribute",
    "TrackedEntityAttributesAccessor",
]
