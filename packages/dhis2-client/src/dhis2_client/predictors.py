"""Predictor authoring + run — `Dhis2Client.predictors`.

Predictors generate data values from expressions over historical data
(e.g. "3-month rolling average of X" → emit a synthetic DataElement
row). The accessor covers both authoring (create / update / delete) and
the run endpoints DHIS2 exposes:

- `POST /api/predictors/run?startDate=…&endDate=…` — run every
  predictor on the instance.
- `POST /api/predictors/{uid}/run?startDate=…&endDate=…` — run one.
- `POST /api/predictorGroups/{uid}/run?startDate=…&endDate=…` — run
  a named group of predictors in one pass (exposed from
  `PredictorsAccessor.run_group` for backward compatibility + also
  from `PredictorGroupsAccessor.run`).

All three run shapes return a `WebMessageResponse` with a summary of
predictions written / ignored / failed; none of them kick a background
job, so there's no task to watch.

Authoring surface: `Predictor.generator` is an `Expression` sub-object
typed as `Any` on the generated schema. `create(...)` assembles the
minimal wrapper here so callers pass the expression string +
description, not the nested payload.

No `*Spec` builder — continues the spec-audit data point.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from dhis2_client.envelopes import WebMessageResponse
from dhis2_client.generated.v42.enums import MissingValueStrategy, OrganisationUnitDescendants
from dhis2_client.generated.v42.schemas import Predictor
from dhis2_client.periods import PeriodType

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


_PREDICTOR_FIELDS: str = (
    "id,name,shortName,code,description,"
    "periodType,sequentialSampleCount,annualSampleCount,sequentialSkipCount,"
    "organisationUnitDescendants,organisationUnitLevels[id,name,level],"
    "output[id,name,code],outputCombo[id,name],"
    "generator[expression,description,missingValueStrategy,slidingWindow],"
    "predictorGroups[id,name]"
)


class PredictorsAccessor:
    """`Dhis2Client.predictors` — CRUD + run helpers over `/api/predictors`."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    # ---- CRUD -----------------------------------------------------------

    async def list_all(
        self,
        *,
        period_type: PeriodType | str | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> list[Predictor]:
        """Page through Predictors, optionally filtered by periodType."""
        filters: list[str] | None = None
        if period_type is not None:
            value = period_type.value if isinstance(period_type, PeriodType) else period_type
            filters = [f"periodType:eq:{value}"]
        return cast(
            list[Predictor],
            await self._client.resources.predictors.list(
                fields=_PREDICTOR_FIELDS,
                filters=filters,
                page=page,
                page_size=page_size,
            ),
        )

    async def get(self, uid: str) -> Predictor:
        """Fetch one Predictor with generator, output, OU scope resolved inline."""
        return await self._client.get(f"/api/predictors/{uid}", model=Predictor, params={"fields": _PREDICTOR_FIELDS})

    async def create(
        self,
        *,
        name: str,
        short_name: str,
        expression: str,
        output_data_element_uid: str,
        period_type: PeriodType | str = PeriodType.MONTHLY,
        sequential_sample_count: int = 3,
        annual_sample_count: int = 0,
        sequential_skip_count: int = 0,
        organisation_unit_descendants: OrganisationUnitDescendants | str = OrganisationUnitDescendants.SELECTED,
        organisation_unit_level_uids: list[str] | None = None,
        output_combo_uid: str | None = None,
        missing_value_strategy: MissingValueStrategy | str = MissingValueStrategy.SKIP_IF_ALL_VALUES_MISSING,
        generator_description: str | None = None,
        description: str | None = None,
        code: str | None = None,
        uid: str | None = None,
    ) -> Predictor:
        """Create a Predictor.

        `expression` uses DHIS2's aggregate expression syntax; the
        accessor wraps it in the `generator` Expression sub-object.
        `output_data_element_uid` is the target DE the prediction writes
        to — needs a `TRACKER` or `AGGREGATE` domain and a numeric
        valueType.

        `sequential_sample_count` + `annual_sample_count` control the
        look-back window: `3` monthly samples with the default period
        type averages the three prior months.

        `organisation_unit_level_uids` scopes the run — pass the UIDs of
        the `OrganisationUnitLevel` rows the predictor should cover
        (typically the facility level for data-entry predictors).
        """
        payload: dict[str, Any] = {
            "name": name,
            "shortName": short_name,
            "periodType": period_type.value if isinstance(period_type, PeriodType) else period_type,
            "sequentialSampleCount": sequential_sample_count,
            "annualSampleCount": annual_sample_count,
            "sequentialSkipCount": sequential_skip_count,
            "organisationUnitDescendants": (
                organisation_unit_descendants.value
                if isinstance(organisation_unit_descendants, OrganisationUnitDescendants)
                else organisation_unit_descendants
            ),
            "output": {"id": output_data_element_uid},
            "generator": {
                "expression": expression,
                "missingValueStrategy": (
                    missing_value_strategy.value
                    if isinstance(missing_value_strategy, MissingValueStrategy)
                    else missing_value_strategy
                ),
                "slidingWindow": False,
            },
        }
        if generator_description:
            payload["generator"]["description"] = generator_description
        if output_combo_uid:
            payload["outputCombo"] = {"id": output_combo_uid}
        if organisation_unit_level_uids:
            payload["organisationUnitLevels"] = [{"id": level_uid} for level_uid in organisation_unit_level_uids]
        if uid:
            payload["id"] = uid
        if code:
            payload["code"] = code
        if description:
            payload["description"] = description
        envelope = await self._client.post("/api/predictors", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("predictor create did not return a uid")
        return await self.get(created_uid)

    async def update(self, predictor: Predictor) -> Predictor:
        """PUT an edited Predictor back. `predictor.id` must be set."""
        if not predictor.id:
            raise ValueError("update requires predictor.id to be set")
        body = predictor.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/predictors/{predictor.id}", body=body)
        return await self.get(predictor.id)

    async def rename(
        self,
        uid: str,
        *,
        name: str | None = None,
        short_name: str | None = None,
        description: str | None = None,
    ) -> Predictor:
        """Partial-update shortcut — read, mutate the label fields, PUT."""
        if name is None and short_name is None and description is None:
            raise ValueError("rename requires at least one of name / short_name / description")
        current = await self.get(uid)
        if name is not None:
            current.name = name
        if short_name is not None:
            current.shortName = short_name
        if description is not None:
            current.description = description
        return await self.update(current)

    async def delete(self, uid: str) -> None:
        """Delete a Predictor. DHIS2 keeps any data values it already wrote."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.predictors.delete(uid)

    # ---- Run ------------------------------------------------------------

    async def run_all(self, *, start_date: str, end_date: str) -> WebMessageResponse:
        """Run every predictor on the instance for the given date range.

        Returns the summary envelope — `.import_count()` gives
        `imported / updated / ignored / deleted` counts for the emitted
        data values.
        """
        return await self._run("/api/predictors/run", start_date=start_date, end_date=end_date)

    async def run_one(self, predictor_uid: str, *, start_date: str, end_date: str) -> WebMessageResponse:
        """Run a single predictor by UID over the given date range."""
        return await self._run(
            f"/api/predictors/{predictor_uid}/run",
            start_date=start_date,
            end_date=end_date,
        )

    async def run_group(self, group_uid: str, *, start_date: str, end_date: str) -> WebMessageResponse:
        """Run every predictor in a `PredictorGroup` over the given date range."""
        return await self._run(
            f"/api/predictorGroups/{group_uid}/run",
            start_date=start_date,
            end_date=end_date,
        )

    async def _run(self, path: str, *, start_date: str, end_date: str) -> WebMessageResponse:
        """Dispatch a predictor-run POST + return the typed envelope."""
        params: dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        raw = await self._client.post_raw(path, params=params)
        return WebMessageResponse.model_validate(raw)


__all__ = ["Predictor", "PredictorsAccessor"]
