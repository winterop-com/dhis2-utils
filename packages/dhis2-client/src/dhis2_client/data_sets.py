"""DataSet authoring — `Dhis2Client.data_sets`.

A DHIS2 `DataSet` is the collection of `DataElement`s captured together
for one period (monthly immunisation tally, weekly commodity stock,
etc.). Generic CRUD lives on the generated accessor
(`client.resources.data_sets`); this module adds the authoring
primitives integration + admin flows need:

- `create(...)` — named kwargs covering the minimal required subset
  (`name`, `short_name`, `period_type`) plus the optional references
  (`category_combo`, `code`, `description`) and the knobs most real
  DataSets carry (`open_future_periods`, `expiry_days`, `timely_days`).
- `add_element(ds_uid, de_uid, *, category_combo_uid=None)` —
  append a DataElement to the DataSet, with optional per-set
  CategoryCombo override. DataSetElements are the join table, not a
  simple ref list; the accessor round-trips the full DataSet, mutates
  `dataSetElements`, and PUTs it back so the `categoryCombo` override
  can be carried without a dedicated endpoint.
- `remove_element(ds_uid, de_uid)` — same round-trip, filtered.
- `rename(uid, ...)` — partial-update shortcut for label fields.
- `delete(uid)` — DHIS2 rejects deletes on DataSets with saved values
  or a section tree.

No `*Spec` builder — continues the spec-audit data point from the
organisation-unit accessors.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2_client.envelopes import WebMessageResponse
from dhis2_client.generated.v42.schemas import DataSet
from dhis2_client.periods import PeriodType

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


_DS_FIELDS: str = (
    "id,name,shortName,code,formName,description,periodType,"
    "categoryCombo[id,name],expiryDays,openFuturePeriods,timelyDays,"
    "mobile,fieldCombinationRequired,validCompleteOnly,noValueRequiresComment,"
    "dataSetElements[dataElement[id,name,code],categoryCombo[id,name]],"
    "sections[id,name,sortOrder],"
    "organisationUnits[id,name]"
)


class DataSetsAccessor:
    """`Dhis2Client.data_sets` — CRUD + membership helpers over `/api/dataSets`."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(
        self,
        *,
        period_type: PeriodType | str | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> list[DataSet]:
        """Page through DataSets, optionally filtered by periodType.

        `period_type=PeriodType.MONTHLY` narrows to monthly DataSets.
        Server-side paged — loop `page` until the returned list is
        shorter than `page_size` for the full catalog.
        """
        params: dict[str, Any] = {
            "fields": _DS_FIELDS,
            "page": str(page),
            "pageSize": str(page_size),
        }
        if period_type is not None:
            value = period_type.value if isinstance(period_type, PeriodType) else period_type
            params["filter"] = f"periodType:eq:{value}"
        raw = await self._client.get_raw("/api/dataSets", params=params)
        rows = raw.get("dataSets") or []
        return [DataSet.model_validate(row) for row in rows if isinstance(row, dict)]

    async def get(self, uid: str) -> DataSet:
        """Fetch one DataSet by UID with its DSEs + sections + OUs resolved inline."""
        return await self._client.get(f"/api/dataSets/{uid}", model=DataSet, params={"fields": _DS_FIELDS})

    async def create(
        self,
        *,
        name: str,
        short_name: str,
        period_type: PeriodType | str,
        category_combo_uid: str | None = None,
        code: str | None = None,
        form_name: str | None = None,
        description: str | None = None,
        open_future_periods: int | None = None,
        expiry_days: int | None = None,
        timely_days: int | None = None,
        uid: str | None = None,
    ) -> DataSet:
        """Create a DataSet.

        DHIS2 rejects DataSets without a `categoryCombo` — omit
        `category_combo_uid` to fall back to the default combo
        (`client.system.default_category_combo_uid()`). `period_type` is
        required (`Monthly`, `Weekly`, `Daily`, `Yearly`, …). Use the
        `PeriodType` StrEnum for typed access; a plain string is
        accepted for the rare frequency not yet in the enum.
        """
        default_combo = category_combo_uid or await self._client.system.default_category_combo_uid()
        payload: dict[str, Any] = {
            "name": name,
            "shortName": short_name,
            "periodType": period_type.value if isinstance(period_type, PeriodType) else period_type,
            "categoryCombo": {"id": default_combo},
        }
        if uid:
            payload["id"] = uid
        if code:
            payload["code"] = code
        if form_name:
            payload["formName"] = form_name
        if description:
            payload["description"] = description
        if open_future_periods is not None:
            payload["openFuturePeriods"] = open_future_periods
        if expiry_days is not None:
            payload["expiryDays"] = expiry_days
        if timely_days is not None:
            payload["timelyDays"] = timely_days
        envelope = await self._client.post("/api/dataSets", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("data-set create did not return a uid")
        return await self.get(created_uid)

    async def update(self, data_set: DataSet) -> DataSet:
        """PUT an edited DataSet back. `data_set.id` must be set."""
        if not data_set.id:
            raise ValueError("update requires data_set.id to be set")
        body = data_set.model_dump(by_alias=True, exclude_none=True, mode="json")
        _strip_self_ref_from_dse(body)
        await self._client.put_raw(f"/api/dataSets/{data_set.id}", body=body)
        return await self.get(data_set.id)

    async def rename(
        self,
        uid: str,
        *,
        name: str | None = None,
        short_name: str | None = None,
        form_name: str | None = None,
        description: str | None = None,
    ) -> DataSet:
        """Partial-update shortcut — read, mutate label fields, PUT."""
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

    async def add_element(
        self,
        data_set_uid: str,
        data_element_uid: str,
        *,
        category_combo_uid: str | None = None,
    ) -> DataSet:
        """Append a DataElement to the DataSet.

        Pass `category_combo_uid` to override the DE's own CategoryCombo
        for this DataSet only (a common pattern when one DE is captured
        under different disaggregations per set).
        """
        current = await self.get(data_set_uid)
        raw = current.model_dump(by_alias=True, exclude_none=True, mode="json")
        _strip_self_ref_from_dse(raw)
        existing = raw.get("dataSetElements") or []
        if any((entry.get("dataElement") or {}).get("id") == data_element_uid for entry in existing):
            return current
        new_entry: dict[str, Any] = {"dataElement": {"id": data_element_uid}}
        if category_combo_uid:
            new_entry["categoryCombo"] = {"id": category_combo_uid}
        existing.append(new_entry)
        raw["dataSetElements"] = existing
        await self._client.put_raw(f"/api/dataSets/{data_set_uid}", body=raw)
        return await self.get(data_set_uid)

    async def remove_element(self, data_set_uid: str, data_element_uid: str) -> DataSet:
        """Remove a DataElement from the DataSet."""
        current = await self.get(data_set_uid)
        raw = current.model_dump(by_alias=True, exclude_none=True, mode="json")
        _strip_self_ref_from_dse(raw)
        existing = raw.get("dataSetElements") or []
        filtered = [entry for entry in existing if (entry.get("dataElement") or {}).get("id") != data_element_uid]
        if len(filtered) == len(existing):
            return current
        raw["dataSetElements"] = filtered
        await self._client.put_raw(f"/api/dataSets/{data_set_uid}", body=raw)
        return await self.get(data_set_uid)

    async def delete(self, uid: str) -> None:
        """Delete a DataSet — DHIS2 rejects deletes on DataSets with saved values."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.data_sets.delete(uid)


def _strip_self_ref_from_dse(payload: dict[str, Any]) -> None:
    """Drop the self-referencing `dataSet` field from each DataSetElement.

    DHIS2's `/api/dataSets/{uid}` embeds `dataSetElements[].dataSet =
    {id: <parent>}`; the importer treats that as an authoring directive
    on the child DSE and rejects the PUT with a "self-reference not
    allowed" conflict. Strip it before every PUT that carries DSEs.
    """
    dse = payload.get("dataSetElements")
    if not isinstance(dse, list):
        return
    cleaned: list[dict[str, Any]] = []
    for entry in dse:
        if isinstance(entry, dict):
            cleaned.append({k: v for k, v in entry.items() if k != "dataSet"})
    payload["dataSetElements"] = cleaned


__all__ = [
    "DataSet",
    "DataSetsAccessor",
]
