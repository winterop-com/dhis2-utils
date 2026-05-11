"""ProgramStage authoring — `Dhis2Client.program_stages`.

The inner layer of tracker schema authoring. A `ProgramStage` is
a stage/visit inside a `Program` — ANC 1st visit, ANC 2nd visit,
vaccination schedule entry, etc. Each stage owns an ordered list of
`programStageDataElements[]` (a join table: which DEs the stage
captures, in what order, with per-DE `compulsory` / `displayInReports`
/ `allowFutureDate` / `allowProvidedElsewhere` flags).

Ships step 3 of the tracker-schema stretch:

- Step 1 (#188) — `TrackedEntityAttribute` + `TrackedEntityType`.
- Step 2 (#189) — `Program` + PTEA + OU scope.
- Step 3 (this) — `ProgramStage` + `programStageDataElements[]`.

Surface:

- `create(...)` — kwargs over the minimal required subset (`name`,
  `program_uid`) plus common knobs (`repeatable`,
  `auto_generate_event`, `min_days_from_start`, `sort_order`,
  `validation_strategy`, `feature_type`).
- `add_element(stage_uid, de_uid, *, compulsory, allow_future_date,
  display_in_reports, allow_provided_elsewhere, render_options_as_radio)`
  — wire a DE into the stage's data-entry form via the PSDE join
  table. Round-trips the full stage + PUTs with `mergeMode=REPLACE`
  (matches the Program PUT quirk).
- `remove_element` / `reorder(stage_uid, [de_uids])`.
- `rename(uid, ...)` / `delete(uid)` — standard edit pathways.

No `*Spec` builder — continues the spec-audit data point.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from dhis2w_client.generated.v41.schemas import ProgramStage
from dhis2w_client.v41.envelopes import WebMessageResponse
from dhis2w_client.v41.periods import PeriodType

if TYPE_CHECKING:
    from dhis2w_client.v41.client import Dhis2Client


_STAGE_FIELDS: str = (
    "id,name,shortName,code,formName,description,"
    "program[id,name],sortOrder,"
    "repeatable,autoGenerateEvent,displayGenerateEventBox,"
    "generatedByEnrollmentDate,openAfterEnrollment,blockEntryForm,"
    "featureType,periodType,validationStrategy,"
    "dueDateLabel,executionDateLabel,eventLabel,"
    "minDaysFromStart,standardInterval,"
    "remindCompleted,enableUserAssignment,preGenerateUID,"
    "programStageDataElements["
    "dataElement[id,name,valueType],compulsory,displayInReports,"
    "allowFutureDate,allowProvidedElsewhere,renderOptionsAsRadio,"
    "skipSynchronization,skipAnalytics,sortOrder"
    "]"
)


class ProgramStagesAccessor:
    """`Dhis2Client.program_stages` — CRUD + PSDE ordering helpers."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(
        self,
        *,
        program_uid: str | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> list[ProgramStage]:
        """Page through ProgramStages, optionally filtered to one parent Program."""
        filters: list[str] | None = None
        if program_uid:
            filters = [f"program.id:eq:{program_uid}"]
        return cast(
            list[ProgramStage],
            await self._client.resources.program_stages.list(
                fields=_STAGE_FIELDS,
                filters=filters,
                page=page,
                page_size=page_size,
            ),
        )

    async def list_for(self, program_uid: str) -> list[ProgramStage]:
        """Return ProgramStages belonging to one Program, sorted by `sortOrder`."""
        return cast(
            list[ProgramStage],
            await self._client.resources.program_stages.list(
                fields=_STAGE_FIELDS,
                filters=[f"program.id:eq:{program_uid}"],
                order=["sortOrder:asc"],
                paging=False,
            ),
        )

    async def get(self, uid: str) -> ProgramStage:
        """Fetch one ProgramStage with its PSDE list resolved inline."""
        return await self._client.get(
            f"/api/programStages/{uid}",
            model=ProgramStage,
            params={"fields": _STAGE_FIELDS},
        )

    async def create(
        self,
        *,
        name: str,
        program_uid: str,
        short_name: str | None = None,
        description: str | None = None,
        code: str | None = None,
        form_name: str | None = None,
        sort_order: int | None = None,
        repeatable: bool | None = None,
        auto_generate_event: bool | None = None,
        generated_by_enrollment_date: bool | None = None,
        open_after_enrollment: bool | None = None,
        block_entry_form: bool | None = None,
        feature_type: str | None = None,
        period_type: PeriodType | str | None = None,
        validation_strategy: str | None = None,
        min_days_from_start: int | None = None,
        standard_interval: int | None = None,
        enable_user_assignment: bool | None = None,
        pre_generate_uid: bool | None = None,
        due_date_label: str | None = None,
        execution_date_label: str | None = None,
        event_label: str | None = None,
        uid: str | None = None,
    ) -> ProgramStage:
        """Create a ProgramStage under `program_uid`.

        `repeatable=True` makes the stage reusable within one enrollment
        (follow-up ANC visits, chronic-care check-ins).
        `auto_generate_event=True` + `generated_by_enrollment_date=True`
        tells DHIS2 to schedule an event when the enrollment is
        created. `min_days_from_start` + `standard_interval` tune the
        default due-date math.
        """
        payload: dict[str, Any] = {
            "name": name,
            "program": {"id": program_uid},
        }
        if short_name:
            payload["shortName"] = short_name
        if description:
            payload["description"] = description
        if code:
            payload["code"] = code
        if form_name:
            payload["formName"] = form_name
        if sort_order is not None:
            payload["sortOrder"] = sort_order
        if repeatable is not None:
            payload["repeatable"] = repeatable
        if auto_generate_event is not None:
            payload["autoGenerateEvent"] = auto_generate_event
        if generated_by_enrollment_date is not None:
            payload["generatedByEnrollmentDate"] = generated_by_enrollment_date
        if open_after_enrollment is not None:
            payload["openAfterEnrollment"] = open_after_enrollment
        if block_entry_form is not None:
            payload["blockEntryForm"] = block_entry_form
        if feature_type:
            payload["featureType"] = feature_type
        if period_type is not None:
            payload["periodType"] = period_type.value if isinstance(period_type, PeriodType) else period_type
        if validation_strategy:
            payload["validationStrategy"] = validation_strategy
        if min_days_from_start is not None:
            payload["minDaysFromStart"] = min_days_from_start
        if standard_interval is not None:
            payload["standardInterval"] = standard_interval
        if enable_user_assignment is not None:
            payload["enableUserAssignment"] = enable_user_assignment
        if pre_generate_uid is not None:
            payload["preGenerateUID"] = pre_generate_uid
        if due_date_label:
            payload["dueDateLabel"] = due_date_label
        if execution_date_label:
            payload["executionDateLabel"] = execution_date_label
        if event_label:
            payload["eventLabel"] = event_label
        if uid:
            payload["id"] = uid
        envelope = await self._client.post("/api/programStages", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("program-stage create did not return a uid")
        return await self.get(created_uid)

    async def update(self, stage: ProgramStage) -> ProgramStage:
        """PUT an edited ProgramStage back. `stage.id` must be set.

        Matches the Program PUT quirk: `mergeMode=REPLACE` forces
        nested-list replacement so `programStageDataElements[]` items
        omitted from the payload actually get removed instead of
        silently retained.
        """
        if not stage.id:
            raise ValueError("update requires stage.id to be set")
        body = stage.model_dump(by_alias=True, exclude_none=True, mode="json")
        _strip_self_ref_from_psde(body)
        await self._client.put_raw(f"/api/programStages/{stage.id}", body=body, params={"mergeMode": "REPLACE"})
        return await self.get(stage.id)

    async def rename(
        self,
        uid: str,
        *,
        name: str | None = None,
        short_name: str | None = None,
        form_name: str | None = None,
        description: str | None = None,
    ) -> ProgramStage:
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
        stage_uid: str,
        data_element_uid: str,
        *,
        compulsory: bool = False,
        allow_future_date: bool = False,
        display_in_reports: bool = True,
        allow_provided_elsewhere: bool = False,
        render_options_as_radio: bool = False,
        skip_synchronization: bool = False,
        skip_analytics: bool = False,
        sort_order: int | None = None,
    ) -> ProgramStage:
        """Wire a DataElement into the ProgramStage via the PSDE join table.

        Round-trips the full stage, appends a new PSDE entry, PUTs with
        `mergeMode=REPLACE`. Idempotent — returns early when the DE is
        already attached.
        """
        current = await self.get(stage_uid)
        raw = current.model_dump(by_alias=True, exclude_none=True, mode="json")
        _strip_self_ref_from_psde(raw)
        existing = raw.get("programStageDataElements") or []
        if any(
            (entry.get("dataElement") or {}).get("id") == data_element_uid
            for entry in existing
            if isinstance(entry, dict)
        ):
            return current
        new_entry: dict[str, Any] = {
            "dataElement": {"id": data_element_uid},
            "compulsory": compulsory,
            "allowFutureDate": allow_future_date,
            "displayInReports": display_in_reports,
            "allowProvidedElsewhere": allow_provided_elsewhere,
            "renderOptionsAsRadio": render_options_as_radio,
            "skipSynchronization": skip_synchronization,
            "skipAnalytics": skip_analytics,
        }
        if sort_order is not None:
            new_entry["sortOrder"] = sort_order
        existing.append(new_entry)
        raw["programStageDataElements"] = existing
        await self._client.put_raw(f"/api/programStages/{stage_uid}", body=raw, params={"mergeMode": "REPLACE"})
        return await self.get(stage_uid)

    async def remove_element(self, stage_uid: str, data_element_uid: str) -> ProgramStage:
        """Drop a DataElement from the ProgramStage's PSDE list."""
        current = await self.get(stage_uid)
        raw = current.model_dump(by_alias=True, exclude_none=True, mode="json")
        _strip_self_ref_from_psde(raw)
        existing = raw.get("programStageDataElements") or []
        filtered = [
            entry
            for entry in existing
            if isinstance(entry, dict) and (entry.get("dataElement") or {}).get("id") != data_element_uid
        ]
        if len(filtered) == len(existing):
            return current
        raw["programStageDataElements"] = filtered
        await self._client.put_raw(f"/api/programStages/{stage_uid}", body=raw, params={"mergeMode": "REPLACE"})
        return await self.get(stage_uid)

    async def reorder(self, stage_uid: str, data_element_uids: list[str]) -> ProgramStage:
        """Replace the ordered `programStageDataElements` with exactly the given DE UIDs.

        Any PSDE flags (`compulsory`, `display_in_reports`, etc.) on
        dropped entries are lost. Use `add_element` + `remove_element`
        for fine-grained edits; reach for `reorder` when the set of
        attached DEs is known.
        """
        current = await self.get(stage_uid)
        raw = current.model_dump(by_alias=True, exclude_none=True, mode="json")
        _strip_self_ref_from_psde(raw)
        # Preserve PSDE flags for DEs that stay in the list.
        existing = {
            (entry.get("dataElement") or {}).get("id"): entry
            for entry in (raw.get("programStageDataElements") or [])
            if isinstance(entry, dict)
        }
        new_entries: list[dict[str, Any]] = []
        for index, de_uid in enumerate(data_element_uids):
            entry = existing.get(de_uid) or {"dataElement": {"id": de_uid}}
            entry["sortOrder"] = index
            new_entries.append(entry)
        raw["programStageDataElements"] = new_entries
        await self._client.put_raw(f"/api/programStages/{stage_uid}", body=raw, params={"mergeMode": "REPLACE"})
        return await self.get(stage_uid)

    async def delete(self, uid: str) -> None:
        """Delete a ProgramStage — DHIS2 rejects deletes on stages with recorded events."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.program_stages.delete(uid)


def _strip_self_ref_from_psde(payload: dict[str, Any]) -> None:
    """Drop the self-referencing `programStage` field from each PSDE entry.

    DHIS2's `/api/programStages/{uid}` read embeds
    `programStageDataElements[].programStage = {id: <parent>}` as an
    inverse ref the importer rejects on PUT. Mirrors the DataSet+DSE /
    TET+TETA / Program+PTEA workarounds.
    """
    entries = payload.get("programStageDataElements")
    if not isinstance(entries, list):
        return
    cleaned: list[dict[str, Any]] = []
    for entry in entries:
        if isinstance(entry, dict):
            cleaned.append({k: v for k, v in entry.items() if k != "programStage"})
    payload["programStageDataElements"] = cleaned


__all__ = [
    "ProgramStage",
    "ProgramStagesAccessor",
]
