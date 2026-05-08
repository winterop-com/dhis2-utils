"""DataElement authoring — `Dhis2Client.data_elements`.

DHIS2 `DataElement`s are the atoms of aggregate + tracker data
capture; every cell of a `DataValueSet` and every `eventDataValue` on
tracker events points at one. Generic CRUD lives on the generated
accessor (`client.resources.data_elements`); this module adds the
authoring primitives integration + admin flows need:

- `create(...)` — named kwargs covering the minimal required subset
  (`name`, `short_name`, `value_type`, `domain_type`, `aggregation_type`)
  plus the optional references (`category_combo`, `option_set`,
  `legend_set`) most real DEs carry, so callers don't hand-craft the
  reference payload shape.
- `update(de)` — PUT with an existing typed `DataElement` model.
- `rename(uid, ...)` — partial-update shortcut for the common case
  of "fix the label / short name / description" without round-tripping
  every field.
- `delete(uid)` — DHIS2 rejects deletes on DEs with saved values.

No `*Spec` builder — continues the spec-audit data point from the
organisation-unit accessors. Callers hand the accessor keyword args;
the accessor dumps a plain dict at the HTTP boundary.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from dhis2w_client.generated.v42.common import Reference
from dhis2w_client.generated.v42.enums import AggregationType, DataElementDomain, ValueType
from dhis2w_client.generated.v42.schemas import DataElement

if TYPE_CHECKING:
    from dhis2w_client.client import Dhis2Client
from dhis2w_client.envelopes import WebMessageResponse

_DE_FIELDS: str = (
    "id,name,shortName,code,formName,description,valueType,domainType,aggregationType,"
    "categoryCombo[id,name],optionSet[id,name,code],legendSets[id,name],"
    "zeroIsSignificant,dataElementGroups[id,name]"
)


class DataElementsAccessor:
    """`Dhis2Client.data_elements` — CRUD + renaming helpers over `/api/dataElements`."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(
        self,
        *,
        domain_type: DataElementDomain | str | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> list[DataElement]:
        """Page through DataElements, optionally filtered to one domain.

        `domain_type=DataElementDomain.AGGREGATE` narrows to aggregate
        DEs; `TRACKER` for tracker-only. Server-side paged — loop `page`
        until the returned list is shorter than `page_size` for the full
        catalog.
        """
        filters: list[str] | None = None
        if domain_type is not None:
            value = domain_type.value if isinstance(domain_type, DataElementDomain) else domain_type
            filters = [f"domainType:eq:{value}"]
        return cast(
            list[DataElement],
            await self._client.resources.data_elements.list(
                fields=_DE_FIELDS,
                filters=filters,
                page=page,
                page_size=page_size,
            ),
        )

    async def get(self, uid: str) -> DataElement:
        """Fetch one DataElement by UID with its references resolved inline."""
        return await self._client.get(f"/api/dataElements/{uid}", model=DataElement, params={"fields": _DE_FIELDS})

    async def create(
        self,
        *,
        name: str,
        short_name: str,
        value_type: ValueType | str,
        domain_type: DataElementDomain | str = DataElementDomain.AGGREGATE,
        aggregation_type: AggregationType | str = AggregationType.SUM,
        category_combo_uid: str | None = None,
        option_set_uid: str | None = None,
        legend_set_uids: list[str] | None = None,
        code: str | None = None,
        form_name: str | None = None,
        description: str | None = None,
        uid: str | None = None,
        zero_is_significant: bool = False,
    ) -> DataElement:
        """Create an aggregate or tracker DataElement.

        DHIS2 rejects DEs without a `categoryCombo` — omit
        `category_combo_uid` to fall back to the default combo
        (`client.system.default_category_combo_uid()`). `legend_set_uids`
        wires colour-legend sets for rendering in the Data Visualizer.
        `aggregation_type` defaults to `SUM`; pass `AVERAGE_SUM_ORG_UNIT`
        / etc. via the `AggregationType` StrEnum for other modes.
        """
        default_combo = category_combo_uid or await self._client.system.default_category_combo_uid()
        payload: dict[str, Any] = {
            "name": name,
            "shortName": short_name,
            "valueType": value_type.value if isinstance(value_type, ValueType) else value_type,
            "domainType": domain_type.value if isinstance(domain_type, DataElementDomain) else domain_type,
            "aggregationType": (
                aggregation_type.value if isinstance(aggregation_type, AggregationType) else aggregation_type
            ),
            "zeroIsSignificant": zero_is_significant,
            "categoryCombo": {"id": default_combo},
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
        envelope = await self._client.post("/api/dataElements", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("data-element create did not return a uid")
        return await self.get(created_uid)

    async def update(self, data_element: DataElement) -> DataElement:
        """PUT an edited DataElement back. `data_element.id` must be set."""
        if not data_element.id:
            raise ValueError("update requires data_element.id to be set")
        body = data_element.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/dataElements/{data_element.id}", body=body)
        return await self.get(data_element.id)

    async def rename(
        self,
        uid: str,
        *,
        name: str | None = None,
        short_name: str | None = None,
        form_name: str | None = None,
        description: str | None = None,
    ) -> DataElement:
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

    async def set_legend_sets(self, uid: str, *, legend_set_uids: list[str]) -> DataElement:
        """Replace the legend-set refs on a DE — used to roll out threshold colouring."""
        current = await self.get(uid)
        current.legendSets = [Reference(id=ref).model_dump(by_alias=True, exclude_none=True) for ref in legend_set_uids]
        return await self.update(current)

    async def delete(self, uid: str) -> None:
        """Delete a DataElement — DHIS2 rejects deletes on DEs with saved values."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.data_elements.delete(uid)


__all__ = [
    "DataElement",
    "DataElementsAccessor",
]
