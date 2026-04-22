"""Programmatic event-only (`WITHOUT_REGISTRATION`) program for the seed.

The Sierra Leone play42 snapshot ships two `WITH_REGISTRATION` programs
(Child Programme, Antenatal care). Event programs — community surveys,
case investigations, supervision visits — aren't in the snapshot.

This module synthesises a minimal event program + one stage that
references two existing Sierra Leone DEs (BCG doses given + Measles
doses given) so the tracker workflow examples + tests have a concrete
target for `add_event` calls that omit `enrollment`. Called from
`seed_play` after the core metadata pass (DEs + OUs already exist by
then).

Every object on the wire is a generated pydantic model — `Program`,
`ProgramStage`, `ProgramStageDataElement`, `Sharing` from
`dhis2_client.generated.v42`. No hand-rolled dicts cross the function
boundary; we dump at the wire edge via
`model_dump(by_alias=True, exclude_none=True)` before POSTing.

Design notes:

- **Icon**: program carries `style.icon = "clinical_a_outline"` so the
  DHIS2 Capture app surfaces it with a recognisable tile.
- **OU scope**: the program is assigned to every level-4 facility OU
  (~1100 on the Sierra Leone tree), not just the country root. Event
  programs are typically run at the facility, and DHIS2 rejects event
  writes at OUs the program isn't assigned to (error E1029). Scoping
  to level-4 matches where immunization supervision actually happens.
- **Dashboard visibility**: an `EventVisualization` (COLUMN chart of
  BCG + Measles supervision values across 2024) is created alongside
  the program and attached to the Immunization data dashboard via
  `client.dashboards.add_item(kind="eventVisualization")`.
  DHIS2's plain dashboardItems don't support a program-launcher kind —
  EventVisualization is the standard way to surface an event program
  on a dashboard.
- **Sample events**: one supervision event per month across 2024 is
  logged at a rotating set of facility OUs so the event viz has real
  rows to chart. Without these the tile renders as "No data available"
  and the dashboard looks broken.

Fixed UIDs so callers can reference the program + stage across rebuilds
without looking them up:

- program  : `EVTsupVis01`  (Supervision visit — event program)
- stage    : `EVTsupVS001`  (Supervision visit stage)
- DE refs  : `s46m5MS0hxu` (BCG doses given), `YtbsuPPo010` (Measles doses given)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from dhis2_client.generated.v42.common import Reference
from dhis2_client.generated.v42.enums import (
    AccessLevel,
    EventOutputType,
    EventVisualizationType,
    ProgramType,
)
from dhis2_client.generated.v42.oas import Sharing
from dhis2_client.generated.v42.schemas import (
    EventVisualization,
    Program,
    ProgramStage,
    ProgramStageDataElement,
    TrackedEntityDataElementDimension,
)
from dhis2_client.sharing import ACCESS_READ_WRITE_DATA

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client

PROGRAM_UID = "EVTsupVis01"
STAGE_UID = "EVTsupVS001"
EVENT_VIZ_UID = "EVTsupViz01"

_DASHBOARD_UID = "L1BtjXgpUpd"  # "Immunization data" dashboard — hosts the event-viz tile.

_SL_ROOT = "ImspTQPwCqd"
_CC_DEFAULT = "bjDvmb4bfuf"  # DHIS2's built-in "default" CategoryCombo (present on every install).
_DE_BCG = "s46m5MS0hxu"
_DE_MEASLES = "YtbsuPPo010"
_ICON_KEY = "clinical_a_outline"  # Ships with DHIS2 core icon set.

_SHARING = Sharing(public=ACCESS_READ_WRITE_DATA, external=False, users={}, userGroups={})


async def _level_four_org_units(client: Dhis2Client) -> list[dict[str, str]]:
    """Return every level-4 (facility) org unit UID as `{id: ...}` refs.

    Event programs are typically run at facility level. Assigning the
    program to every level-4 OU means supervision events can be logged
    anywhere DHIS2 has a registered facility, not only at the country
    root. DHIS2 otherwise rejects event writes at unassigned OUs (E1029).
    """
    raw = await client.get_raw(
        "/api/organisationUnits",
        params={"filter": "level:eq:4", "fields": "id", "paging": "false"},
    )
    ous = raw.get("organisationUnits") or []
    return [{"id": str(entry["id"])} for entry in ous if isinstance(entry, dict) and entry.get("id")]


def _supervision_stage() -> ProgramStage:
    """Typed `ProgramStage` for the supervision-visit program's single stage."""
    return ProgramStage(
        id=STAGE_UID,
        name="Supervision visit stage",
        shortName="Supervision stage",
        program=Reference(id=PROGRAM_UID),
        repeatable=True,
        autoGenerateEvent=True,
        openAfterEnrollment=False,
        generatedByEnrollmentDate=False,
        sortOrder=1,
        programStageDataElements=[
            ProgramStageDataElement(
                dataElement=Reference(id=_DE_BCG),
                compulsory=False,
                allowProvidedElsewhere=False,
                displayInReports=True,
                sortOrder=0,
            ),
            ProgramStageDataElement(
                dataElement=Reference(id=_DE_MEASLES),
                compulsory=False,
                allowProvidedElsewhere=False,
                displayInReports=True,
                sortOrder=1,
            ),
        ],
        sharing=_SHARING,
    )


def _supervision_program(org_units: list[dict[str, str]]) -> Program:
    """Typed `Program` for the supervision-visit event program.

    Assigned to every facility-level OU passed in so events can be
    logged anywhere there's a registered facility. Icon surfaces on the
    Capture app tile.
    """
    return Program(
        id=PROGRAM_UID,
        name="Supervision visit",
        shortName="Supervision",
        programType=ProgramType.WITHOUT_REGISTRATION,
        categoryCombo=Reference(id=_CC_DEFAULT),
        organisationUnits=[*org_units, {"id": _SL_ROOT}],
        programStages=[{"id": STAGE_UID}],
        accessLevel=AccessLevel.OPEN,
        style={"icon": _ICON_KEY},
        sharing=_SHARING,
    )


def _supervision_event_viz() -> EventVisualization:
    """Typed `EventVisualization` — BCG + Measles values across 2024 monthly.

    Event visualizations on a dashboard are how DHIS2 surfaces event
    programs — plain dashboardItems don't support a program-launcher
    kind. This COLUMN chart aggregates event-stage data values across
    the year so supervisors see a month-by-month trend.

    DHIS2 binds event-program data elements to the viz via
    `dataElementDimensions` (each entry = `{dataElement, programStage}`)
    rather than the aggregate-style `dataDimensionItems` used on plain
    `Visualization`. Period on rows, org unit on columns, DE on filter.
    `outputType=EVENT` — the query aggregates over event rows rather
    than enrollments or tracked entities.
    """
    return EventVisualization(
        id=EVENT_VIZ_UID,
        name="Supervision visit 2024",
        shortName="Supervision 2024",
        type=EventVisualizationType.COLUMN,
        outputType=EventOutputType.EVENT,
        program=Reference(id=PROGRAM_UID),
        programStage=Reference(id=STAGE_UID),
        dataElementDimensions=[
            TrackedEntityDataElementDimension(
                dataElement=Reference(id=_DE_BCG),
                programStage=Reference(id=STAGE_UID),
            ),
            TrackedEntityDataElementDimension(
                dataElement=Reference(id=_DE_MEASLES),
                programStage=Reference(id=STAGE_UID),
            ),
        ],
        periods=[{"id": f"2024{month:02d}"} for month in range(1, 13)],
        organisationUnits=[{"id": _SL_ROOT}],
        rowDimensions=["pe"],
        columnDimensions=["ou"],
        filterDimensions=["dx"],
        sharing=_SHARING,
    )


async def _seed_sample_events(client: Dhis2Client, org_units: list[dict[str, str]]) -> int:
    """Log one supervision event per month of 2024 to give the event viz data.

    Rotates through the first 12 facility OUs so the chart has a spread
    across sites too. Uses `client.tracker.add_event` with no enrollment —
    standalone events, DHIS2 accepts them directly against the event
    program. Returns the number of events logged.
    """
    # Slice to the first 12 facilities (or fewer if the tree has fewer OUs).
    facilities = [ou["id"] for ou in org_units[:12]] or [_SL_ROOT]
    count = 0
    for month in range(1, 13):
        # Rotate OU each month so the distribution isn't all on one site.
        ou_id = facilities[(month - 1) % len(facilities)]
        # Values scale up over the year so the chart shows a visible trend.
        bcg_value = str(5 + month * 2)
        measles_value = str(3 + month * 2)
        await client.tracker.add_event(
            program=PROGRAM_UID,
            program_stage=STAGE_UID,
            org_unit=ou_id,
            data_values={_DE_BCG: bcg_value, _DE_MEASLES: measles_value},
            occurred_at=f"2024-{month:02d}-15",
        )
        count += 1
    return count


async def _attach_event_viz_to_dashboard(client: Dhis2Client) -> None:
    """Add the supervision EventVisualization to the Immunization data dashboard.

    Idempotent — scans the current dashboard items first and bails if
    the tile is already attached. Uses `client.dashboards.add_item`'s
    `kind="eventVisualization"` path so DHIS2 sets the right
    `type=EVENT_VISUALIZATION` on the new dashboard item.

    Note: `Dashboard.dashboardItems` is typed `list[Any]` in the
    generated model (DHIS2's schema loses the item's polymorphic type
    at the typed-list edge). Items come back as dicts even when the
    Dashboard itself is a pydantic model — hence the `.get()` scan
    below rather than attribute access.
    """
    current = await client.dashboards.get(_DASHBOARD_UID)
    for item in current.dashboardItems or []:
        if not isinstance(item, dict):
            continue
        ref = item.get("eventVisualization")
        if isinstance(ref, dict) and ref.get("id") == EVENT_VIZ_UID:
            return
    await client.dashboards.add_item(_DASHBOARD_UID, EVENT_VIZ_UID, kind="eventVisualization")


async def build_event_program(client: Dhis2Client) -> str:
    """Create / update the Supervision-visit event program + dashboard viz tile.

    Idempotent — uses fixed UIDs everywhere, so re-runs update in place
    instead of creating duplicates. Fetches the current facility-level
    OUs on each call so the program's assignment tracks the OU tree.

    After the program + stage land, creates the supervision
    EventVisualization and attaches it to the Immunization data
    dashboard (again, both steps idempotent).
    """
    org_units = await _level_four_org_units(client)
    program = _supervision_program(org_units)
    stage = _supervision_stage()
    payload = {
        "programs": [program.model_dump(by_alias=True, exclude_none=True, mode="json")],
        "programStages": [stage.model_dump(by_alias=True, exclude_none=True, mode="json")],
    }
    await client.post_raw(
        "/api/metadata",
        body=payload,
        params={"importStrategy": "CREATE_AND_UPDATE", "atomicMode": "OBJECT"},
    )
    # The event viz ships in a second call because it references the program
    # and stage — DHIS2 resolves those the moment they're on disk, but
    # splitting keeps the import order explicit.
    viz = _supervision_event_viz()
    await client.post_raw(
        "/api/metadata",
        body={"eventVisualizations": [viz.model_dump(by_alias=True, exclude_none=True, mode="json")]},
        params={"importStrategy": "CREATE_AND_UPDATE", "atomicMode": "OBJECT"},
    )
    await _seed_sample_events(client, org_units)
    await _attach_event_viz_to_dashboard(client)
    return PROGRAM_UID
