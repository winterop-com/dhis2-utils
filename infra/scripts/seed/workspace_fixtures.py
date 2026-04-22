"""Workspace-local fixtures the play42 snapshot doesn't ship.

The Sierra Leone play42 snapshot covers the immunization-domain data
model well (OUs, DEs, programs, dashboards) but is thin on:

- OptionSets with meaningful codes (none shaped like `VACCINE_TYPE`).
- Custom `Attribute` definitions — the cross-resource interop mapping
  story (SNOMED / ICD-10 / external IDs attached via `attributeValues`).
- SqlViews — DHIS2's saved-query mechanism, useful for analyst-friendly
  SQL over the DHIS2 data model without opening a Postgres connection.
- Predictors — DHIS2's forecast-from-history mechanism. Upstream ships
  the endpoints (`/api/predictors/run`, `/api/predictorGroups/{id}/run`)
  but no default predictor to run, so `dhis2 maintenance predictors run
  --group ...` had no concrete target on fresh dumps.
- Validation rules — DHIS2's data-integrity business-logic mechanism.
  Upstream ships the endpoints (`/api/validationRules`, `.../run`) but
  no default rule to run, so `dhis2 maintenance validation run` and the
  VR analysis commands had no concrete target on fresh dumps.

Workflow examples for each of these surfaces were parked on
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
4. **Two predictors + a PredictorGroup**, so `maintenance predictors run
   [--group]` has somewhere to write:
   - Output DEs `DePredBCG01` (avg) + `DePredSum01` (sum) — destinations
     for the predicted values.
   - `PrdAvgBCG01` / `PrdSumBCG01` — 3-month rolling average + sum of
     the seeded `s46m5MS0hxu` (BCG doses given) DE.
   - `PdGImmun001` — group wrapping both predictors.
5. **Two validation rules + a ValidationRuleGroup**, so `maintenance
   validation run [--group]` has concrete targets:
   - `VrBCGPos001` — "BCG <1y > 0". Guaranteed to find rows that
     violate (the seed has legitimate zero-dose months).
   - `VrBCGInf001` — "BCG <1y == BCG >1y". Violates on almost every
     cell since the two age buckets rarely have equal counts.
   - `VrGImmun001` — group wrapping both.

Everything is typed: `Attribute`, `OptionSet`, `Option`, `SqlView`,
`Predictor`, `PredictorGroup`, `DataElement`, `ValidationRule`,
`ValidationRuleGroup`, `Sharing` from `dhis2_client.generated.v42`
— no hand-rolled dicts cross the function boundary. Seed runs after
the core metadata pass (DEs + OUs already exist), idempotent via
fixed UIDs + CREATE_AND_UPDATE.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2_client.generated.v42.common import Reference
from dhis2_client.generated.v42.enums import (
    AggregationType,
    DataElementDomain,
    Importance,
    Operator,
    OrganisationUnitDescendants,
    PeriodType,
    SqlViewType,
    ValueType,
)
from dhis2_client.generated.v42.oas import Sharing
from dhis2_client.generated.v42.schemas import (
    Attribute,
    DataElement,
    Option,
    OptionSet,
    OrganisationUnitLevel,
    Predictor,
    PredictorGroup,
    SqlView,
    ValidationRule,
    ValidationRuleGroup,
)
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

# Predictor fixtures. Input DE `s46m5MS0hxu` = "BCG doses given" from the
# play42 Sierra Leone snapshot — INTEGER, SUM aggregation, populated by
# the seeded aggregate data values across 2024. The DE stores values on
# two age-bucket CategoryOptionCombos (Prlt0C1RF0s = "<1y", V6L425pT3A0
# = ">1y") — the predictor expression references the "<1y" combo
# directly because an unqualified `#{s46m5MS0hxu}` resolves to the
# default combo, which this DE doesn't use.
DE_PREDICTOR_BCG_INPUT_UID = "s46m5MS0hxu"
COC_BCG_UNDER_ONE_UID = "Prlt0C1RF0s"
DE_PREDICTOR_AVG_OUTPUT_UID = "DePredBCG01"
DE_PREDICTOR_SUM_OUTPUT_UID = "DePredSum01"
PREDICTOR_AVG_BCG_UID = "PrdAvgBCG01"
PREDICTOR_SUM_BCG_UID = "PrdSumBCG01"
PREDICTOR_GROUP_IMMUNIZATION_UID = "PdGImmun001"

# OrganisationUnitLevel records. DHIS2's predictor engine needs the target
# OU levels specified as references (not bare integers) or the `run`
# endpoint emits 0 predictions. Seed level-3 (district) and level-4
# (facility) so the predictors can point at facility and future examples
# can group analytics by district without a per-instance manual step.
OU_LEVEL_DISTRICT_UID = "OuLvlDistrc"
OU_LEVEL_FACILITY_UID = "OuLvlFacilt"

# Validation-rule fixtures — run over the same BCG doses DE the predictors
# target. `VrBCGPos001` asserts BCG <1y > 0 (finds legitimate zero-dose
# months); `VrBCGInf001` asserts BCG <1y == BCG >1y (almost always
# violates since the two age buckets rarely match). A `VrGImmun001`
# group wraps both for `dhis2 maintenance validation run --group`.
COC_BCG_OVER_ONE_UID = "V6L425pT3A0"
VALIDATION_RULE_BCG_POSITIVE_UID = "VrBCGPos001"
VALIDATION_RULE_BCG_INF_EQ_UID = "VrBCGInf001"
VALIDATION_RULE_GROUP_IMMUNIZATION_UID = "VrGImmun001"

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


def _ou_level(uid: str, level: int, name: str) -> OrganisationUnitLevel:
    """Typed `OrganisationUnitLevel` — binds a display name to a hierarchy level."""
    return OrganisationUnitLevel(
        id=uid,
        level=level,
        name=name,
    )


def _predictor_output_de(uid: str, name: str, short_name: str) -> DataElement:
    """Typed output `DataElement` for a predictor — plain numeric, uses default categoryCombo."""
    return DataElement(
        id=uid,
        name=name,
        shortName=short_name,
        valueType=ValueType.NUMBER,
        aggregationType=AggregationType.SUM,
        domainType=DataElementDomain.AGGREGATE,
        zeroIsSignificant=False,
        sharing=_SHARING,
    )


def _predictor(
    *,
    uid: str,
    name: str,
    short_name: str,
    output_uid: str,
    expression: str,
    description: str,
) -> Predictor:
    """Typed `Predictor` — MONTHLY periods, 3 sequential samples, default OU scope.

    DHIS2 `generator` is an `Expression` sub-object with at minimum an
    `expression` string (reusing the aggregate-data-element reference
    syntax `#{<DE_UID>}`). `sequentialSampleCount=3` + `periodType=Monthly`
    makes each run consume the three prior months of data; run windows
    land on the aggregated-data output DE passed in.
    """
    return Predictor(
        id=uid,
        name=name,
        shortName=short_name,
        code=uid,
        description=description,
        output=Reference(id=output_uid),
        generator={  # Expression sub-object — typed as `Any` on the Predictor model.
            "expression": expression,
            "description": description,
        },
        periodType=PeriodType.MONTHLY,
        sequentialSampleCount=3,
        annualSampleCount=0,
        sequentialSkipCount=0,
        organisationUnitDescendants=OrganisationUnitDescendants.SELECTED,
        organisationUnitLevels=[Reference(id=OU_LEVEL_FACILITY_UID)],
        sharing=_SHARING,
    )


def _validation_rule(
    *,
    uid: str,
    name: str,
    short_name: str,
    description: str,
    left_expression: str,
    operator: Operator,
    right_expression: str,
) -> ValidationRule:
    """Typed `ValidationRule` — MONTHLY period, HIGH importance, SKIP_IF_ALL_VALUES_MISSING strategy.

    `leftSide` / `rightSide` are `Expression` sub-objects (typed as `Any`
    on the generated model). Each carries the expression string plus a
    `missingValueStrategy` — `SKIP_IF_ALL_VALUES_MISSING` is the safe
    default so a row with no data doesn't count as a violation.
    """
    return ValidationRule(
        id=uid,
        name=name,
        shortName=short_name,
        code=uid,
        description=description,
        leftSide={
            "expression": left_expression,
            "description": f"leftSide: {description}",
            "missingValueStrategy": "SKIP_IF_ALL_VALUES_MISSING",
            "slidingWindow": False,
        },
        operator=operator,
        rightSide={
            "expression": right_expression,
            "description": f"rightSide: {description}",
            "missingValueStrategy": "SKIP_IF_ALL_VALUES_MISSING",
            "slidingWindow": False,
        },
        periodType=PeriodType.MONTHLY,
        importance=Importance.HIGH,
        organisationUnitLevels=[4],
        sharing=_SHARING,
    )


def _validation_rule_group() -> ValidationRuleGroup:
    """Typed `ValidationRuleGroup` wrapping both BCG validation rules."""
    return ValidationRuleGroup(
        id=VALIDATION_RULE_GROUP_IMMUNIZATION_UID,
        name="Immunization validation rules (BCG)",
        code="IMMUNIZATION_VALIDATION_RULES",
        validationRules=[
            Reference(id=VALIDATION_RULE_BCG_POSITIVE_UID),
            Reference(id=VALIDATION_RULE_BCG_INF_EQ_UID),
        ],
        sharing=_SHARING,
    )


def _predictor_group() -> PredictorGroup:
    """Typed `PredictorGroup` wrapping both BCG-dose predictors."""
    return PredictorGroup(
        id=PREDICTOR_GROUP_IMMUNIZATION_UID,
        name="Immunization predictors (BCG rolling)",
        code="IMMUNIZATION_PREDICTORS",
        predictors=[
            Reference(id=PREDICTOR_AVG_BCG_UID),
            Reference(id=PREDICTOR_SUM_BCG_UID),
        ],
        sharing=_SHARING,
    )


async def build_workspace_fixtures(client: Dhis2Client) -> int:
    """Post the metadata bundle (attributes + option-sets + sql-views + predictors) via /api/metadata.

    Idempotent — fixed UIDs + CREATE_AND_UPDATE, so re-running updates
    in place rather than creating duplicates. Attaches the two seeded
    SNOMED attribute values on BCG + Measles via the AttributeValues
    accessor (read-merge-write) after the bundle lands. Returns the
    total metadata-object count (18 = 2 OU levels + 1 attribute +
    1 option set + 5 options + 3 sql views + 2 data elements +
    2 predictors + 1 predictor group + 2 validation rules +
    1 validation rule group; attribute values aren't counted because
    they ride a separate endpoint).
    """
    metadata_bundle: dict[str, list[dict[str, Any]]] = {
        "organisationUnitLevels": [
            _ou_level(OU_LEVEL_DISTRICT_UID, 3, "District").model_dump(by_alias=True, exclude_none=True, mode="json"),
            _ou_level(OU_LEVEL_FACILITY_UID, 4, "Facility").model_dump(by_alias=True, exclude_none=True, mode="json"),
        ],
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
        "dataElements": [
            _predictor_output_de(
                DE_PREDICTOR_AVG_OUTPUT_UID,
                "BCG doses given (3-month rolling average)",
                "BCG avg 3m",
            ).model_dump(by_alias=True, exclude_none=True, mode="json"),
            _predictor_output_de(
                DE_PREDICTOR_SUM_OUTPUT_UID,
                "BCG doses given (3-month rolling sum)",
                "BCG sum 3m",
            ).model_dump(by_alias=True, exclude_none=True, mode="json"),
        ],
        "predictors": [
            _predictor(
                uid=PREDICTOR_AVG_BCG_UID,
                name="BCG doses given — 3-month rolling average",
                short_name="BCG avg 3m",
                output_uid=DE_PREDICTOR_AVG_OUTPUT_UID,
                expression=f"avg(#{{{DE_PREDICTOR_BCG_INPUT_UID}.{COC_BCG_UNDER_ONE_UID}}})",
                description="Predicted monthly average of BCG doses given over the prior 3 months.",
            ).model_dump(by_alias=True, exclude_none=True, mode="json"),
            _predictor(
                uid=PREDICTOR_SUM_BCG_UID,
                name="BCG doses given — 3-month rolling sum",
                short_name="BCG sum 3m",
                output_uid=DE_PREDICTOR_SUM_OUTPUT_UID,
                expression=f"sum(#{{{DE_PREDICTOR_BCG_INPUT_UID}.{COC_BCG_UNDER_ONE_UID}}})",
                description="Predicted monthly sum of BCG doses given over the prior 3 months.",
            ).model_dump(by_alias=True, exclude_none=True, mode="json"),
        ],
        "predictorGroups": [
            _predictor_group().model_dump(by_alias=True, exclude_none=True, mode="json"),
        ],
        "validationRules": [
            _validation_rule(
                uid=VALIDATION_RULE_BCG_POSITIVE_UID,
                name="BCG doses <1y must be positive",
                short_name="BCG <1y > 0",
                description="BCG first-dose count for <1y age bucket must be greater than zero.",
                left_expression=f"#{{{DE_PREDICTOR_BCG_INPUT_UID}.{COC_BCG_UNDER_ONE_UID}}}",
                operator=Operator.GREATER_THAN,
                right_expression="0",
            ).model_dump(by_alias=True, exclude_none=True, mode="json"),
            _validation_rule(
                uid=VALIDATION_RULE_BCG_INF_EQ_UID,
                name="BCG doses <1y must equal BCG doses >1y",
                short_name="BCG <1y == >1y",
                description=(
                    "Sentinel rule — BCG doses for the two age buckets should match "
                    "(almost never does, produces reliable violations for analysis demos)."
                ),
                left_expression=f"#{{{DE_PREDICTOR_BCG_INPUT_UID}.{COC_BCG_UNDER_ONE_UID}}}",
                operator=Operator.EQUAL_TO,
                right_expression=f"#{{{DE_PREDICTOR_BCG_INPUT_UID}.{COC_BCG_OVER_ONE_UID}}}",
            ).model_dump(by_alias=True, exclude_none=True, mode="json"),
        ],
        "validationRuleGroups": [
            _validation_rule_group().model_dump(by_alias=True, exclude_none=True, mode="json"),
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
    return 2 + 1 + 1 + 5 + 3 + 2 + 2 + 1 + 2 + 1
