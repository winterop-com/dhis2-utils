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
`ProgramStage`, `ProgramStageDataElement` from
`dhis2_client.generated.v42.schemas`. No hand-rolled dicts crossing
the function boundary; we dump at the wire edge via
`model_dump(by_alias=True, exclude_none=True)` before POSTing.

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

_SHARING = Sharing(public=ACCESS_READ_WRITE_DATA, external=False, users={}, userGroups={})


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


def _supervision_program() -> Program:
    """Typed `Program` for the supervision-visit event program."""
    return Program(
        id=PROGRAM_UID,
        name="Supervision visit",
        shortName="Supervision",
        programType=ProgramType.WITHOUT_REGISTRATION,
        categoryCombo=Reference(id=_CC_DEFAULT),
        organisationUnits=[{"id": _SL_ROOT}],
        programStages=[{"id": STAGE_UID}],
        accessLevel=AccessLevel.OPEN,
        sharing=_SHARING,
    )


async def build_event_program(client: Dhis2Client) -> str:
    """Create / update the Supervision-visit event program via /api/metadata.

    Idempotent — uses fixed UIDs, so re-runs update in place instead of
    creating duplicates. Dumps every typed model through `by_alias +
    exclude_none` so the wire payload matches DHIS2's JSON contract.
    Returns the program UID for caller reference.
    """
    program = _supervision_program()
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
