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
- **Dashboard visibility**: DHIS2's dashboardItems don't support a
  program-launcher kind (valid types are VISUALIZATION / MAP / TEXT /
  USERS / etc.). The program shows up in the Capture app's program
  list; for dashboard-level visibility a follow-up should author an
  EventVisualization that aggregates supervision events and attach it
  as a VISUALIZATION-kind tile via the existing dashboard builder.

Fixed UIDs so callers can reference the program + stage across rebuilds
without looking them up:

- program  : `EVTsupVis01`  (Supervision visit — event program)
- stage    : `EVTsupVS001`  (Supervision visit stage)
- DE refs  : `s46m5MS0hxu` (BCG doses given), `YtbsuPPo010` (Measles doses given)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from dhis2_client.generated.v42.common import Reference
from dhis2_client.generated.v42.enums import AccessLevel, ProgramType
from dhis2_client.generated.v42.oas import Sharing
from dhis2_client.generated.v42.schemas import Program, ProgramStage, ProgramStageDataElement
from dhis2_client.sharing import ACCESS_READ_WRITE_DATA

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client

PROGRAM_UID = "EVTsupVis01"
STAGE_UID = "EVTsupVS001"

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


async def build_event_program(client: Dhis2Client) -> str:
    """Create / update the Supervision-visit event program via /api/metadata.

    Idempotent — uses fixed UIDs, so re-runs update in place instead of
    creating duplicates. Fetches the current facility-level OUs on each
    call so the program's assignment tracks the OU tree.
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
    return PROGRAM_UID
