"""Workspace-local fixtures the play42 snapshot doesn't ship.

The Sierra Leone play42 snapshot covers the immunization-domain data
model well (OUs, DEs, programs, dashboards) but is thin on:

- OptionSets with meaningful codes (none shaped like `VACCINE_TYPE`).
- Custom `Attribute` definitions — the cross-resource interop mapping
  story (SNOMED / ICD-10 / external IDs attached via `attributeValues`).
- SqlViews — DHIS2's saved-query mechanism, useful for analyst-friendly
  SQL over the DHIS2 data model without opening a Postgres connection.

Workflow examples for each of the three surfaces were parked on
`verify_examples.py`'s skip-list for lack of a concrete target. This
module synthesises the minimum fixture that unskips every one:

1. **Attribute `SNOMED_CODE`** (`AtrSNOMED01`) — TEXT, optionAttribute
   only. The integration-killer hook examples lean on: "given a
   SNOMED code, find the DHIS2 Option it maps to".
2. **OptionSet `VACCINE_TYPE`** (`OsVaccType1`) + 5 Options with fixed
   UIDs so examples can reference them by UID across rebuilds:
   - `OptVacBCG01` / BCG / SNOMED 77656005
   - `OptVacMes01` / MEASLES / SNOMED 386661006
   - `OptVacPlo01` / POLIO
   - `OptVacDPT01` / DPT
   - `OptVacHpB01` / HEPB
3. **Three SqlViews**, one of each type, so `sql-view list / execute /
   refresh / adhoc` all have a target:
   - `SqvOuLvl001` — VIEW, OU count per level
   - `SqvDeByNm01` — QUERY with `${pattern}` substitution, DE name search
   - `SqvDeVtMV01` — MATERIALIZED_VIEW, DE count per valueType

Everything is typed: `Attribute`, `OptionSet`, `Option`, `SqlView`,
`Sharing` from `dhis2_client.generated.v42` — no hand-rolled dicts cross
the function boundary. Seed runs after the core metadata pass (DEs +
OUs already exist), idempotent via fixed UIDs + CREATE_AND_UPDATE.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2_client.generated.v42.common import Reference
from dhis2_client.generated.v42.enums import SqlViewType, ValueType
from dhis2_client.generated.v42.oas import Sharing
from dhis2_client.generated.v42.schemas import Attribute, Option, OptionSet, SqlView
from dhis2_client.sharing import ACCESS_READ_WRITE_DATA

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client

# Fixed UIDs so examples reference them across rebuilds.
ATTRIBUTE_SNOMED_UID = "AtrSNOMED01"
OPTION_SET_VACCINE_UID = "OsVaccType1"
OPTION_BCG_UID = "OptVacBCG01"
OPTION_MEASLES_UID = "OptVacMes01"
OPTION_POLIO_UID = "OptVacPlo01"
OPTION_DPT_UID = "OptVacDPT01"
OPTION_HEPB_UID = "OptVacHpB01"

SQLVIEW_OU_LEVEL_UID = "SqvOuLvl001"
SQLVIEW_DE_BY_NAME_UID = "SqvDeByNm01"
SQLVIEW_DE_VALUETYPE_UID = "SqvDeVtMV01"

_SHARING = Sharing(public=ACCESS_READ_WRITE_DATA, external=False, users={}, userGroups={})


def _snomed_attribute() -> Attribute:
    """Typed `Attribute` — SNOMED_CODE, TEXT, only applicable to Options."""
    return Attribute(
        id=ATTRIBUTE_SNOMED_UID,
        name="SNOMED code",
        shortName="SNOMED",
        code="SNOMED_CODE",
        valueType=ValueType.TEXT,
        optionAttribute=True,
        unique=False,
        mandatory=False,
        sharing=_SHARING,
    )


def _vaccine_option(
    uid: str,
    code: str,
    name: str,
    sort_order: int,
) -> Option:
    """Typed `Option` for the VACCINE_TYPE set — fixed UID so examples can lookup."""
    return Option(
        id=uid,
        code=code,
        name=name,
        shortName=name[:50],
        optionSet=Reference(id=OPTION_SET_VACCINE_UID),
        sortOrder=sort_order,
    )


def _vaccine_option_set() -> OptionSet:
    """Typed `OptionSet` wrapping the 5 vaccine-type options via references."""
    return OptionSet(
        id=OPTION_SET_VACCINE_UID,
        name="Vaccine type",
        code="VACCINE_TYPE",
        valueType=ValueType.TEXT,
        options=[
            Reference(id=OPTION_BCG_UID),
            Reference(id=OPTION_MEASLES_UID),
            Reference(id=OPTION_POLIO_UID),
            Reference(id=OPTION_DPT_UID),
            Reference(id=OPTION_HEPB_UID),
        ],
        sharing=_SHARING,
    )


def _sqlview_ou_level() -> SqlView:
    """VIEW — row per OU level with count + max depth markers."""
    return SqlView(
        id=SQLVIEW_OU_LEVEL_UID,
        name="Org units per level",
        description="Count of organisation units at each hierarchy level.",
        type=SqlViewType.VIEW,
        sqlQuery=(
            "SELECT hierarchylevel AS level, COUNT(*) AS count "
            "FROM organisationunit GROUP BY hierarchylevel ORDER BY hierarchylevel"
        ),
        sharing=_SHARING,
    )


def _sqlview_de_by_name() -> SqlView:
    """QUERY with `${pattern}` variable — DE name substring search."""
    return SqlView(
        id=SQLVIEW_DE_BY_NAME_UID,
        name="Data elements by name pattern",
        description="Search DataElements by a name pattern. Use `vars=pattern:<term>` in the execute call.",
        type=SqlViewType.QUERY,
        sqlQuery="SELECT uid, name, shortname FROM dataelement WHERE name ILIKE '%${pattern}%' ORDER BY name LIMIT 50",
        sharing=_SHARING,
    )


def _sqlview_de_valuetype() -> SqlView:
    """MATERIALIZED_VIEW — DataElement count per valueType. Refreshable on demand."""
    return SqlView(
        id=SQLVIEW_DE_VALUETYPE_UID,
        name="Data elements per value type",
        description="Aggregate count of DataElements grouped by valueType.",
        type=SqlViewType.MATERIALIZED_VIEW,
        sqlQuery="SELECT valuetype, COUNT(*) AS count FROM dataelement GROUP BY valuetype ORDER BY valuetype",
        sharing=_SHARING,
    )


async def build_workspace_fixtures(client: Dhis2Client) -> int:
    """Post the attribute + option-set/options + sql-views bundle via /api/metadata.

    Idempotent — fixed UIDs + CREATE_AND_UPDATE, so re-running updates
    in place rather than creating duplicates. Then sets the two seeded
    SNOMED attribute values on BCG + Measles via the AttributeValues
    accessor (read-merge-write). Returns the total object count that
    landed (7 = 1 attribute + 1 option set + 5 options + 3 sql views +
    2 attribute values, minus the attribute values since they're not
    counted on the metadata POST side).
    """
    metadata_bundle: dict[str, list[dict[str, Any]]] = {
        "attributes": [
            _snomed_attribute().model_dump(by_alias=True, exclude_none=True, mode="json"),
        ],
        "optionSets": [
            _vaccine_option_set().model_dump(by_alias=True, exclude_none=True, mode="json"),
        ],
        "options": [
            _vaccine_option(OPTION_BCG_UID, "BCG", "BCG", 1).model_dump(by_alias=True, exclude_none=True, mode="json"),
            _vaccine_option(OPTION_MEASLES_UID, "MEASLES", "Measles", 2).model_dump(
                by_alias=True, exclude_none=True, mode="json"
            ),
            _vaccine_option(OPTION_POLIO_UID, "POLIO", "Polio", 3).model_dump(
                by_alias=True, exclude_none=True, mode="json"
            ),
            _vaccine_option(OPTION_DPT_UID, "DPT", "DPT", 4).model_dump(by_alias=True, exclude_none=True, mode="json"),
            _vaccine_option(OPTION_HEPB_UID, "HEPB", "Hepatitis B", 5).model_dump(
                by_alias=True, exclude_none=True, mode="json"
            ),
        ],
        "sqlViews": [
            _sqlview_ou_level().model_dump(by_alias=True, exclude_none=True, mode="json"),
            _sqlview_de_by_name().model_dump(by_alias=True, exclude_none=True, mode="json"),
            _sqlview_de_valuetype().model_dump(by_alias=True, exclude_none=True, mode="json"),
        ],
    }
    await client.post_raw(
        "/api/metadata",
        body=metadata_bundle,
        params={"importStrategy": "CREATE_AND_UPDATE", "atomicMode": "OBJECT"},
    )
    # Attach SNOMED codes — read-merge-write via the typed accessor.
    await client.attribute_values.set_value("options", OPTION_BCG_UID, ATTRIBUTE_SNOMED_UID, "77656005")
    await client.attribute_values.set_value("options", OPTION_MEASLES_UID, ATTRIBUTE_SNOMED_UID, "386661006")
    return 1 + 1 + 5 + 3
