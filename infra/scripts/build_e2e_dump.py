"""Build the committed e2e DHIS2 dump against a fresh-bootstrapped instance.

Usage (from repo root): `make dhis2-build-e2e-dump` — brings up an empty DHIS2,
runs this script to populate metadata + monthly data 2015-2025 + the standard
OAuth2 client + admin openId mapping, triggers analytics, and pg_dump's the
result into `infra/dhis-v{DHIS2_VERSION}.sql.gz`.

Deterministic everywhere that matters: UIDs, org unit structure, data-element
codes, OAuth2 client id/secret. The only per-run randomness is the data values
themselves (seeded RNG, so they're also reproducible) and BCrypt's salt on the
client secret (same plaintext verifies regardless).

Produces a dump small enough (~1–3 MB gzipped) to commit next to the compose
file, so `make dhis2-up` on a fresh clone gives you a ready-to-login DHIS2
with realistic analytics data.
"""

from __future__ import annotations

import argparse
import asyncio
import gzip
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from datetime import datetime  # noqa: E402

# Cross-version models + client — stable across DHIS2 2.42+. Hand-written
# because `/api/schemas` doesn't describe the tracker / dataValueSet /
# analytics instance shapes; they're defined only in OpenAPI. PeriodType
# is also hand-written since upstream `PeriodType` is a class hierarchy
# rather than a Java enum.
from dhis2_client import (  # noqa: E402 — path-prepend intentional
    BasicAuth,
    DataValue,
    DataValueSet,
    Dhis2Client,
    LoginCustomization,
    PeriodType,
    WebMessageResponse,
    generate_uid,
)

# Version-specific generated models — emitted from DHIS2 v42's /api/schemas.
# The committed e2e dump targets v42 so this script pins to the v42 generated
# module explicitly.
from dhis2_client.generated.v42.common import Reference  # noqa: E402
from dhis2_client.generated.v42.enums import (  # noqa: E402
    AggregationType,
    DataElementDomain,
    Importance,
    MissingValueStrategy,
    Operator,
    ProgramType,
    ValueType,
)

# `/api/schemas`-derived UserRole mis-pluralises `authorities` → `authoritys`
# (the emitter appends 's' naively). Use the OAS-derived UserRole here; its
# field names match the real wire format.
from dhis2_client.generated.v42.oas import UserRole  # noqa: E402
from dhis2_client.generated.v42.schemas import (  # noqa: E402
    DataElement,
    DataSet,
    DataSetElement,
    Expression,
    OrganisationUnit,
    Program,
    ProgramStage,
    ProgramStageDataElement,
    ProgramTrackedEntityAttribute,
    TrackedEntityAttribute,
    TrackedEntityType,
    TrackedEntityTypeAttribute,
    UserGroup,
    ValidationRule,
    ValidationRuleGroup,
)
from dhis2_client.generated.v42.tracker import (  # noqa: E402
    EnrollmentStatus,
    EventStatus,
    TrackerBundle,
    TrackerEnrollment,
    TrackerEvent,
    TrackerTrackedEntity,
)
from pydantic import BaseModel, ConfigDict  # noqa: E402
from seed_auth import ensure_user_openid_mapping, upsert_oauth2_client, wait_for_ready  # noqa: E402

# ---------------------------------------------------------------------------
# Deterministic identifiers
# ---------------------------------------------------------------------------


class OrgUnitSpec(BaseModel):
    """Deterministic identifiers for a seeded org unit."""

    model_config = ConfigDict(frozen=True)

    uid: str
    code: str
    name: str


class DataElementSpec(BaseModel):
    """Deterministic identifiers for a seeded data element."""

    model_config = ConfigDict(frozen=True)

    uid: str
    code: str
    name: str


# DHIS2 UIDs are 11 chars, [A-Za-z][A-Za-z0-9]{10}. Human-readable so it's
# obvious in the UI / logs what these refer to. Org-unit hierarchy is:
#
#   Norway
#   ├── Oslo
#   ├── Vestland
#   ├── Trøndelag
#   └── Nordland
#
# A small, real-world tree gives the analytics dashboards something
# recognisable to aggregate — better for manual smoke-testing than a
# synthetic "District 1/2/3" setup.
OU_ROOT_UID = "NORNorway01"

# One spec per fylke. UIDs stay ASCII; names can carry Norwegian chars.
PROVINCES: list[OrgUnitSpec] = [
    OrgUnitSpec(uid="NOROsloProv", code="NOR_OSLO", name="Oslo"),
    OrgUnitSpec(uid="NORVestland", code="NOR_VESTLAND", name="Vestland"),
    OrgUnitSpec(uid="NORTrondlag", code="NOR_TRONDELAG", name="Trøndelag"),
    OrgUnitSpec(uid="NORNordland", code="NOR_NORDLAND", name="Nordland"),
]
OU_PROVINCE_UIDS = [p.uid for p in PROVINCES]

DS_UID = "NORMonthDS1"


# 7 data elements — the maternal/child health set gives realistic seasonal
# variation when the analytics tables render. DHIS2 UIDs must match
# `[A-Za-z][A-Za-z0-9]{10}` — 11 chars, no underscores, no hyphens.
# (Learned the hard way: `DE_ANC01vst` fails with E4014 Invalid UID.)
DATA_ELEMENTS: list[DataElementSpec] = [
    DataElementSpec(uid="DEancVisit1", code="ANC1ST", name="ANC 1st visit"),
    DataElementSpec(uid="DEancVisit4", code="ANC4TH", name="ANC 4th visit"),
    DataElementSpec(uid="DEdelFacilt", code="DELFAC", name="Deliveries in facility"),
    DataElementSpec(uid="DEliveBirth", code="BIRTH", name="Live births"),
    DataElementSpec(uid="DEbcgVaccin", code="VACBCG", name="Child vaccinations (BCG)"),
    DataElementSpec(uid="DEmesVaccin", code="VACMES", name="Child vaccinations (measles)"),
    DataElementSpec(uid="DEopdConsul", code="OPD", name="OPD consultations (total)"),
]

START_YEAR = 2015
END_YEAR = 2025  # inclusive

# ---------------------------------------------------------------------------
# Tracker + event programs
#
# DHIS2 has two flavours of program:
#   - WITH_REGISTRATION     (tracker program; each row is a TrackedEntity with
#                            one or more enrollments, each carrying events)
#   - WITHOUT_REGISTRATION  (event program;   each row is a single standalone
#                            event, no TEI, no enrollment)
# The seed ships one of each so `dhis2 data tracker`, `dhis2 analytics events`,
# and `dhis2 analytics enrollments` all have something to read against.
# ---------------------------------------------------------------------------

# Minted once via `dhis2_client.generate_uid()` so every UID is guaranteed to
# match DHIS2's `^[A-Za-z][A-Za-z0-9]{10}$` regex without risk of a typo in
# hand-written 11-char strings. Pasted here as constants so the committed
# dump stays byte-reproducible across rebuilds.
TET_PERSON_UID = "FsgEX4d3Fc5"
TEA_FIRST_NAME_UID = "gskc6FLk1pQ"
TEA_LAST_NAME_UID = "aIeQSP9rwIu"
TEA_DOB_UID = "swGQg8tteit"

# Tracker program — maternal care, with two stages (ANC visit + delivery).
# Reuses DEancVisit1 / DEdelFacilt created above so analytics dimensions
# overlap between the aggregate dataset and the tracker program.
PROG_MATERNAL_UID = "eke95YJi9VS"
STAGE_ANC_UID = "b1rFlQyZFPX"
STAGE_DELIVERY_UID = "iPwB0u9Tufl"

# Event program — standalone malaria case reporting. One stage, one DE.
PROG_MALARIA_UID = "kNYyyzd0DLp"
STAGE_MALARIA_UID = "hqHu9bJaAaH"
DE_MALARIA_CASE_UID = "G26HLwsgfQn"

# ---------------------------------------------------------------------------
# User groups + user roles
#
# Gives callers something to filter/mutate from the `dhis2 user-group` +
# `dhis2 user-role` plugins against a freshly seeded instance. Three groups:
# data-entry, analysts, admin. One extra role: data-entry (the seeded
# Superuser role covers admin). No sharing grants yet — keep the default
# seeded admin as owner/public-read.
# ---------------------------------------------------------------------------

USER_GROUP_DATA_ENTRY_UID = "ZnZB3PZR3Qq"
USER_GROUP_ANALYSTS_UID = "YqirA6gkMLG"
USER_GROUP_ADMINS_UID = "fKCkReZEyUN"
USER_ROLE_DATA_ENTRY_UID = "YHt5Wbp4YFV"

# ---------------------------------------------------------------------------
# Validation rules
#
# Three realistic data-quality rules wired up so `dhis2 maintenance
# validation run` has something to evaluate out of the box. Because the
# seeded data values are random, most runs produce a mix of passes +
# violations — good for exercising the full response path.
#
# The rules reference seeded DE UIDs directly; `periodType=Monthly`
# matches the seeded dataset so DHIS2 evaluates them over every month
# that has data.
# ---------------------------------------------------------------------------

VR_ANC_CONSISTENCY_UID = "WQ9mjcYCFJE"
VR_MEASLES_LE_BCG_UID = "xBLQGAYWeU3"
VR_OPD_NONZERO_UID = "Kc9mdXbAFRY"
VR_GROUP_CORE_UID = "KOIDLPkzBvS"


def default_dump_path(dhis2_version: str) -> Path:
    """Gzipped dump path for a given DHIS2 major version (e.g. '42' -> infra/dhis-v42.sql.gz)."""
    return Path(__file__).resolve().parents[1] / f"dhis-v{dhis2_version}.sql.gz"


# Matches the compose project's auto-generated postgres container name.
POSTGRES_CONTAINER_DEFAULT = "dhis2-docker-postgresql-1"

# Committed branding assets applied to every fresh fixture. `infra/login-customization/`
# holds the logo PNGs + preset.json; the seed uploads them via the same `Dhis2Client.customize`
# surface that `dhis2 dev customize apply` uses from the CLI.
LOGIN_CUSTOMIZATION_DIR = Path(__file__).resolve().parents[1] / "login-customization"


# ---------------------------------------------------------------------------
# Metadata + data population
# ---------------------------------------------------------------------------


async def resolve_default_category_combo(client: Dhis2Client) -> str:
    """Return the UID of DHIS2's built-in `default` category combo.

    DHIS2's Flyway migrations always seed a category combo named `default`;
    every aggregate data element and dataset must reference it when no
    disaggregation is needed.
    """
    return await client.system.default_category_combo_uid()


def _dump(models: list[Any]) -> list[dict[str, Any]]:
    """Serialise a list of typed dhis2-client models into the /api/metadata bundle shape."""
    return [m.model_dump(by_alias=True, exclude_none=True, mode="json") for m in models]


async def create_org_units(client: Dhis2Client) -> None:
    """Create the 2-level org unit tree: Norway ; 4 fylker (Oslo, Vestland, Trøndelag, Nordland)."""
    root = OrganisationUnit(
        id=OU_ROOT_UID,
        code="NOR",
        name="Norway",
        shortName="Norway",
        openingDate=datetime(2000, 1, 1),
    )
    children = [
        OrganisationUnit(
            id=spec.uid,
            code=spec.code,
            name=spec.name,
            shortName=spec.name,
            openingDate=datetime(2000, 1, 1),
            parent=Reference(id=OU_ROOT_UID),
        )
        for spec in PROVINCES
    ]
    units = [root, *children]
    await client.resources.organisation_units.save_bulk(units)
    print(f"    created {len(units)} org units (Norway + {len(PROVINCES)} fylker)")


async def create_data_elements(client: Dhis2Client, category_combo_uid: str) -> None:
    """Create the 7 monthly aggregate data elements."""
    data_elements = [
        DataElement(
            id=spec.uid,
            code=spec.code,
            name=spec.name,
            shortName=spec.code,
            domainType=DataElementDomain.AGGREGATE,
            valueType=ValueType.INTEGER_ZERO_OR_POSITIVE,
            aggregationType=AggregationType.SUM,
            categoryCombo=Reference(id=category_combo_uid),
        )
        for spec in DATA_ELEMENTS
    ]
    await client.resources.data_elements.save_bulk(data_elements)
    print(f"    created {len(data_elements)} data elements")


async def create_dataset(client: Dhis2Client, category_combo_uid: str) -> None:
    """Create a Monthly dataset holding all data elements and assigned to all districts."""
    data_set = DataSet(
        id=DS_UID,
        code="NOR_MONTHLY_DS",
        name="Norway Monthly Indicators",
        shortName="Norway Monthly",
        periodType=PeriodType.MONTHLY,
        categoryCombo=Reference(id=category_combo_uid),
        dataSetElements=[
            DataSetElement(dataElement=Reference(id=spec.uid), dataSet=Reference(id=DS_UID)) for spec in DATA_ELEMENTS
        ],
        organisationUnits=[Reference(id=uid) for uid in OU_PROVINCE_UIDS],
        openFuturePeriods=0,
        timelyDays=15,
    )
    await client.resources.data_sets.save_bulk([data_set])
    print(f"    created dataset {DS_UID}")


async def assign_admin_capture_scope(client: Dhis2Client) -> None:
    """Attach the 3 districts to admin's organisationUnits so admin has capture scope."""
    me = await client.system.me()
    admin_uid = me.id
    await client.patch_raw(
        f"/api/users/{admin_uid}",
        [
            {
                "op": "add",
                "path": "/organisationUnits",
                "value": [{"id": uid} for uid in OU_PROVINCE_UIDS],
            }
        ],
    )
    print(f"    assigned {len(OU_PROVINCE_UIDS)} fylker to admin capture scope")


async def create_validation_rules(client: Dhis2Client) -> None:
    """Seed three realistic validation rules + a ValidationRuleGroup.

    All three reference seeded DEs + use `periodType=Monthly` so DHIS2
    evaluates them against every month in the seeded random-data window.
    Because the values are random, a typical `dhis2 maintenance validation
    run NORNorway01 --start-date 2020-01-01 --end-date 2025-12-31` catches
    a handful of real violations per rule — perfect for exercising the
    plugin end-to-end on a freshly-seeded instance.
    """
    rules: list[ValidationRule] = [
        ValidationRule(
            id=VR_ANC_CONSISTENCY_UID,
            name="ANC 1st >= ANC 4th",
            shortName="ANC 1st >= 4th",
            description="Women starting antenatal care should outnumber those completing 4 visits.",
            operator=Operator.GREATER_THAN_OR_EQUAL_TO,
            importance=Importance.HIGH,
            periodType=PeriodType.MONTHLY,
            leftSide=Expression(
                expression="#{DEancVisit1}",
                description="ANC 1st visits",
                missingValueStrategy=MissingValueStrategy.SKIP_IF_ANY_VALUE_MISSING,
            ),
            rightSide=Expression(
                expression="#{DEancVisit4}",
                description="ANC 4th visits",
                missingValueStrategy=MissingValueStrategy.SKIP_IF_ANY_VALUE_MISSING,
            ),
        ),
        ValidationRule(
            id=VR_MEASLES_LE_BCG_UID,
            name="Measles vaccinations <= BCG vaccinations",
            shortName="Measles <= BCG",
            description=(
                "Measles doses should not exceed BCG doses (BCG is given at birth, "
                "measles later — any child with measles must have BCG first)."
            ),
            operator=Operator.LESS_THAN_OR_EQUAL_TO,
            importance=Importance.MEDIUM,
            periodType=PeriodType.MONTHLY,
            leftSide=Expression(
                expression="#{DEmesVaccin}",
                description="Measles vaccinations",
                missingValueStrategy=MissingValueStrategy.SKIP_IF_ANY_VALUE_MISSING,
            ),
            rightSide=Expression(
                expression="#{DEbcgVaccin}",
                description="BCG vaccinations",
                missingValueStrategy=MissingValueStrategy.SKIP_IF_ANY_VALUE_MISSING,
            ),
        ),
        ValidationRule(
            id=VR_OPD_NONZERO_UID,
            name="OPD consultations should be positive",
            shortName="OPD > 0",
            description="Zero OPD consultations for a month at a facility is typically a data-capture gap.",
            operator=Operator.GREATER_THAN,
            importance=Importance.LOW,
            periodType=PeriodType.MONTHLY,
            leftSide=Expression(
                expression="#{DEopdConsul}",
                description="OPD consultations",
                missingValueStrategy=MissingValueStrategy.SKIP_IF_ALL_VALUES_MISSING,
            ),
            rightSide=Expression(
                expression="0",
                description="Zero",
                missingValueStrategy=MissingValueStrategy.NEVER_SKIP,
            ),
        ),
    ]
    group = ValidationRuleGroup(
        id=VR_GROUP_CORE_UID,
        name="Core data-quality checks",
        code="VRG_CORE",
        description="Sensible baseline VRs seeded for fresh e2e dumps.",
        validationRules=[Reference(id=rule.id) for rule in rules if rule.id is not None],
    )
    raw = await client.post_raw(
        "/api/metadata",
        {
            "validationRules": _dump(rules),
            "validationRuleGroups": _dump([group]),
        },
        params={"importStrategy": "CREATE_AND_UPDATE"},
    )
    WebMessageResponse.model_validate(raw)  # validate shape; ignore value
    print(f"    created {len(rules)} validation rules + 1 ValidationRuleGroup")


async def create_user_groups_and_roles(client: Dhis2Client) -> None:
    """Seed three user groups + one extra user role.

    Exercises the `dhis2 user-group` + `dhis2 user-role` plugins against the
    committed fixture: three groups (data-entry, analysts, admins) and a
    data-entry role carrying a narrow authority set. Groups are empty on
    creation — callers build membership workflows on top.
    """
    me = await client.system.me()
    admin_uid = me.id

    groups = [
        UserGroup(id=USER_GROUP_DATA_ENTRY_UID, name="Data Entry", code="GRP_DATA_ENTRY"),
        UserGroup(id=USER_GROUP_ANALYSTS_UID, name="Analysts", code="GRP_ANALYSTS"),
        UserGroup(id=USER_GROUP_ADMINS_UID, name="Administrators", code="GRP_ADMINS"),
    ]
    data_entry_role = UserRole(
        id=USER_ROLE_DATA_ENTRY_UID,
        name="Data entry clerk",
        code="ROLE_DATA_ENTRY",
        description="Capture + read access for aggregate data values. No metadata edits.",
        authorities=[
            "F_DATAVALUE_ADD",
            "F_DATAVALUE_DELETE",
            "M_dhis-web-dataentry",
            "F_ORGANISATIONUNIT_MOVE",
        ],
    )

    # Two resources in one bundle: `save_bulk` on each accessor is typed,
    # but DHIS2's single /api/metadata POST with both keys resolves
    # cross-resource dependencies in one pass, so stay on the raw-bundle
    # shape here. Wrap the result in a typed envelope for readability.
    raw = await client.post_raw(
        "/api/metadata",
        {
            "userGroups": [g.model_dump(by_alias=True, exclude_none=True, mode="json") for g in groups],
            "userRoles": [data_entry_role.model_dump(by_alias=True, exclude_none=True, mode="json")],
        },
        params={"importStrategy": "CREATE_AND_UPDATE"},
    )
    WebMessageResponse.model_validate(raw)  # validate shape; ignore value
    # Put admin in every seeded group so membership-related list calls and
    # sharing-get examples have something to show on a clean dump. The
    # membership endpoint is `/api/userGroups/<uid>/users/<userId>` in v42
    # (not `/members/` — DHIS2 names the collection `users` on UserGroup).
    for group in groups:
        await client.post_raw(f"/api/userGroups/{group.id}/users/{admin_uid}", {})
    print(f"    created {len(groups)} user groups + 1 extra user role")


def generate_data_values(seed: int = 42) -> list[DataValue]:
    """Produce deterministic monthly values for every (district × data-element × period).

    Numbers are randomised within realistic bounds so analytics aggregations
    produce varied charts — but seeded so rebuilds are byte-reproducible.
    """
    rng = random.Random(seed)
    periods = [f"{year}{month:02d}" for year in range(START_YEAR, END_YEAR + 1) for month in range(1, 13)]
    values: list[DataValue] = []
    for ou_uid in OU_PROVINCE_UIDS:
        for de_spec in DATA_ELEMENTS:
            base = rng.randint(50, 400)
            trend = rng.uniform(0.98, 1.03)
            level = float(base)
            for period in periods:
                noise = rng.randint(-25, 40)
                value = max(0, int(level + noise))
                values.append(
                    DataValue(
                        dataElement=de_spec.uid,
                        period=period,
                        orgUnit=ou_uid,
                        value=str(value),
                    ),
                )
                level *= trend
    return values


async def upload_data_values(client: Dhis2Client, values: list[DataValue], chunk_size: int = 2000) -> None:
    """POST data values in chunks so the payload stays small and errors are localised."""
    total = len(values)
    print(f"    uploading {total} data values in chunks of {chunk_size}")
    for start in range(0, total, chunk_size):
        chunk = DataValueSet(dataValues=values[start : start + chunk_size])
        response = await client.post_raw(
            "/api/dataValueSets",
            chunk.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        status = response.get("status")
        if status not in (None, "SUCCESS", "OK"):
            raise RuntimeError(f"dataValueSets import failed: {response}")
    print(f"    uploaded {total} values")


async def create_tracker_program(client: Dhis2Client, category_combo_uid: str) -> None:
    """Seed a TrackedEntityType, tracker program (WITH_REGISTRATION), and event program.

    Uses typed `Program`, `ProgramStage`, `TrackedEntityType`,
    `TrackedEntityAttribute` models from dhis2-client — same surface end
    users get. Eats our own dogfood.
    """
    attrs = [
        TrackedEntityAttribute(
            id=TEA_FIRST_NAME_UID,
            code="TEA_FIRST_NAME",
            name="First name",
            shortName="First name",
            valueType=ValueType.TEXT,
            aggregationType=AggregationType.NONE,
        ),
        TrackedEntityAttribute(
            id=TEA_LAST_NAME_UID,
            code="TEA_LAST_NAME",
            name="Last name",
            shortName="Last name",
            valueType=ValueType.TEXT,
            aggregationType=AggregationType.NONE,
        ),
        TrackedEntityAttribute(
            id=TEA_DOB_UID,
            code="TEA_DOB",
            name="Date of birth",
            shortName="DOB",
            valueType=ValueType.DATE,
            aggregationType=AggregationType.NONE,
        ),
    ]

    person_tet = TrackedEntityType(
        id=TET_PERSON_UID,
        code="TET_PERSON",
        name="Person",
        shortName="Person",
        trackedEntityTypeAttributes=[
            TrackedEntityTypeAttribute(trackedEntityAttribute=Reference(id=TEA_FIRST_NAME_UID), displayInList=True),
            TrackedEntityTypeAttribute(trackedEntityAttribute=Reference(id=TEA_LAST_NAME_UID), displayInList=True),
            TrackedEntityTypeAttribute(trackedEntityAttribute=Reference(id=TEA_DOB_UID), displayInList=False),
        ],
    )

    malaria_de = DataElement(
        id=DE_MALARIA_CASE_UID,
        code="DE_MALARIA_CASE",
        name="Malaria case reported",
        shortName="MalariaCase",
        domainType=DataElementDomain.TRACKER,
        valueType=ValueType.BOOLEAN,
        aggregationType=AggregationType.COUNT,
        categoryCombo=Reference(id=category_combo_uid),
    )

    sharing_public = {"public": "rwrw----", "external": False, "users": {}, "userGroups": {}}

    maternal_program = Program(
        id=PROG_MATERNAL_UID,
        code="PROG_MATERNAL",
        name="Maternal Care",
        shortName="Maternal",
        programType=ProgramType.WITH_REGISTRATION,
        trackedEntityType=Reference(id=TET_PERSON_UID),
        categoryCombo=Reference(id=category_combo_uid),
        organisationUnits=[Reference(id=ou) for ou in OU_PROVINCE_UIDS],
        # Program must own its ProgramStages (the back-reference from the stage
        # isn't enough; DHIS2 drops events with "ProgramStage has no reference
        # to a Program" on the tracker POST unless the program lists them here).
        programStages=[Reference(id=STAGE_ANC_UID), Reference(id=STAGE_DELIVERY_UID)],
        # DHIS2's JSON uses `trackedEntityAttribute`; the codegen emits the
        # pydantic field as `attribute` because `/api/schemas` reports that
        # name. `model_validate` with the wire-name dict lets extras through.
        programTrackedEntityAttributes=[
            ProgramTrackedEntityAttribute.model_validate(
                {"trackedEntityAttribute": {"id": TEA_FIRST_NAME_UID}, "displayInList": True, "mandatory": True},
            ),
            ProgramTrackedEntityAttribute.model_validate(
                {"trackedEntityAttribute": {"id": TEA_LAST_NAME_UID}, "displayInList": True, "mandatory": True},
            ),
            ProgramTrackedEntityAttribute.model_validate(
                {"trackedEntityAttribute": {"id": TEA_DOB_UID}, "displayInList": False, "mandatory": False},
            ),
        ],
        sharing=sharing_public,
    )

    malaria_program = Program(
        id=PROG_MALARIA_UID,
        code="PROG_MALARIA",
        name="Malaria Cases",
        shortName="Malaria",
        programType=ProgramType.WITHOUT_REGISTRATION,
        categoryCombo=Reference(id=category_combo_uid),
        organisationUnits=[Reference(id=ou) for ou in OU_PROVINCE_UIDS],
        programStages=[Reference(id=STAGE_MALARIA_UID)],
        sharing=sharing_public,
    )

    stages = [
        ProgramStage(
            id=STAGE_ANC_UID,
            name="ANC visit",
            program=Reference(id=PROG_MATERNAL_UID),
            repeatable=True,
            sortOrder=1,
            programStageDataElements=[
                ProgramStageDataElement(dataElement=Reference(id="DEancVisit1"), compulsory=True, sortOrder=1),
            ],
        ),
        ProgramStage(
            id=STAGE_DELIVERY_UID,
            name="Delivery",
            program=Reference(id=PROG_MATERNAL_UID),
            repeatable=False,
            sortOrder=2,
            programStageDataElements=[
                ProgramStageDataElement(dataElement=Reference(id="DEdelFacilt"), compulsory=True, sortOrder=1),
            ],
        ),
        ProgramStage(
            id=STAGE_MALARIA_UID,
            name="Case reporting",
            program=Reference(id=PROG_MALARIA_UID),
            repeatable=False,
            sortOrder=1,
            programStageDataElements=[
                ProgramStageDataElement(dataElement=Reference(id=DE_MALARIA_CASE_UID), compulsory=True, sortOrder=1),
            ],
        ),
    ]

    payload: dict[str, list[dict[str, Any]]] = {
        "trackedEntityAttributes": _dump(attrs),
        "trackedEntityTypes": _dump([person_tet]),
        "dataElements": _dump([malaria_de]),
        "programs": _dump([maternal_program, malaria_program]),
        "programStages": _dump(stages),
    }
    await client.post_raw(
        "/api/metadata",
        payload,
        params={"importStrategy": "CREATE_AND_UPDATE", "atomicMode": "ALL"},
    )
    print("    created TET Person + tracker program + event program + 3 stages")


async def seed_tracker_instances(client: Dhis2Client, seed: int = 42) -> None:
    """Create a handful of tracked entities, enrollments, and events for analytics to aggregate.

    Uses the typed `TrackerBundle` / `TrackerTrackedEntity` / `TrackerEnrollment`
    / `TrackerEvent` models end-to-end. Deterministic UIDs + values (seeded
    RNG) so the committed dump reproduces byte-for-byte across rebuilds.
    """
    rng = random.Random(seed)
    first_names = ["Ada", "Ingrid", "Kari", "Liv", "Marte", "Solveig", "Astrid", "Sigrid"]
    last_names = ["Hansen", "Larsen", "Olsen", "Berg", "Dahl", "Lund"]
    today = datetime(2026, 1, 15)

    tracked_entities: list[TrackerTrackedEntity] = []
    events: list[TrackerEvent] = []

    # 8 Person tracked entities, each enrolled in maternal-care with one ANC event.
    for _ in range(8):
        te_uid = generate_uid()
        enr_uid = generate_uid()
        ou_uid = rng.choice(OU_PROVINCE_UIDS)
        tracked_entities.append(
            TrackerTrackedEntity.model_validate(
                {
                    "trackedEntity": te_uid,
                    "trackedEntityType": TET_PERSON_UID,
                    "orgUnit": ou_uid,
                    "attributes": [
                        {"attribute": TEA_FIRST_NAME_UID, "value": rng.choice(first_names)},
                        {"attribute": TEA_LAST_NAME_UID, "value": rng.choice(last_names)},
                        {"attribute": TEA_DOB_UID, "value": f"{rng.randint(1985, 2005)}-{rng.randint(1, 12):02d}-15"},
                    ],
                    "enrollments": [
                        TrackerEnrollment(
                            enrollment=enr_uid,
                            trackedEntity=te_uid,
                            program=PROG_MATERNAL_UID,
                            orgUnit=ou_uid,
                            enrolledAt=today,
                            occurredAt=today,
                            status=EnrollmentStatus.ACTIVE,
                            events=[
                                TrackerEvent.model_validate(
                                    {
                                        "event": generate_uid(),
                                        "program": PROG_MATERNAL_UID,
                                        "programStage": STAGE_ANC_UID,
                                        "enrollment": enr_uid,
                                        "trackedEntity": te_uid,
                                        "orgUnit": ou_uid,
                                        "status": EventStatus.COMPLETED,
                                        "occurredAt": today,
                                        "dataValues": [
                                            {"dataElement": "DEancVisit1", "value": str(rng.randint(1, 4))},
                                        ],
                                    }
                                ),
                            ],
                        ).model_dump(by_alias=True, exclude_none=True, mode="json"),
                    ],
                }
            ),
        )

    # 12 standalone malaria events across the fylker.
    for _ in range(12):
        events.append(
            TrackerEvent.model_validate(
                {
                    "event": generate_uid(),
                    "program": PROG_MALARIA_UID,
                    "programStage": STAGE_MALARIA_UID,
                    "orgUnit": rng.choice(OU_PROVINCE_UIDS),
                    "status": EventStatus.COMPLETED,
                    "occurredAt": today,
                    "dataValues": [{"dataElement": DE_MALARIA_CASE_UID, "value": "true"}],
                }
            ),
        )

    bundle = TrackerBundle(trackedEntities=tracked_entities, events=events)
    # async=false so the POST blocks until the import completes — otherwise
    # `pg_dump` captures a half-written state (or no tracker data at all,
    # since /api/tracker defaults to queueing a job).
    response = await client.post_raw(
        "/api/tracker",
        bundle.model_dump(by_alias=True, exclude_none=True, mode="json"),
        params={"importStrategy": "CREATE_AND_UPDATE", "atomicMode": "ALL", "async": "false"},
    )
    status = response.get("status")
    if status not in (None, "OK", "SUCCESS"):
        raise RuntimeError(f"tracker seed failed: {response}")
    stats = response.get("stats") or response.get("response", {}).get("stats") or {}
    print(
        f"    tracker import: created={stats.get('created', '?')} updated={stats.get('updated', '?')} "
        f"ignored={stats.get('ignored', '?')}"
    )


async def apply_login_customization(client: Dhis2Client) -> None:
    """Apply the committed login-page branding preset (`infra/login-customization/`)."""
    import json as _json

    preset = LoginCustomization()
    logo_front = LOGIN_CUSTOMIZATION_DIR / "logo_front.png"
    if logo_front.exists():
        preset.logo_front = logo_front.read_bytes()
    logo_banner = LOGIN_CUSTOMIZATION_DIR / "logo_banner.png"
    if logo_banner.exists():
        preset.logo_banner = logo_banner.read_bytes()
    style = LOGIN_CUSTOMIZATION_DIR / "style.css"
    if style.exists():
        preset.style_css = style.read_text(encoding="utf-8")
    settings_file = LOGIN_CUSTOMIZATION_DIR / "preset.json"
    if settings_file.exists():
        loaded = _json.loads(settings_file.read_text(encoding="utf-8"))
        preset.system_settings = {str(k): str(v) for k, v in loaded.items()}
    result = await client.customize.apply_preset(preset)
    print(
        f"    applied branding: logo_front={result.logo_front_uploaded} "
        f"logo_banner={result.logo_banner_uploaded} style={result.style_uploaded} "
        f"settings={len(result.settings_applied)}"
    )


def run_analytics(analytics_container: str = "analytics-trigger") -> None:
    """Trigger analytics by restarting the compose's `analytics-trigger` sidecar and waiting for it to exit.

    The sidecar already POSTs `/api/resourceTables/analytics` and polls the
    resulting task until it reports completion — reusing it means we don't
    re-implement the retry/poll logic (and we inherit the memory-aware
    waiting behaviour tuned for DHIS2). The sidecar runs once on stack-up
    against an empty DB (no-op), so we restart it explicitly after loading
    data and block until it exits.
    """
    print(f"    restarting {analytics_container} to populate analytics tables")
    subprocess.run(["docker", "restart", analytics_container], check=True, capture_output=True)
    print("    waiting for analytics task to finish (docker wait)...")
    result = subprocess.run(
        ["docker", "wait", analytics_container],
        check=True,
        capture_output=True,
        text=True,
    )
    exit_code = int(result.stdout.strip() or "1")
    if exit_code != 0:
        logs = subprocess.run(
            ["docker", "logs", "--tail", "50", analytics_container],
            capture_output=True,
            text=True,
            check=False,
        ).stdout
        raise RuntimeError(f"analytics-trigger exited with {exit_code}:\n{logs}")
    print("    analytics tables populated")


# ---------------------------------------------------------------------------
# DB dump
# ---------------------------------------------------------------------------


def pg_dump(container: str, output: Path, *, postgres_user: str, postgres_db: str) -> None:
    """Run `pg_dump | gzip` via `docker exec` and write the result to `output`.

    Skips the derived `analytics_*` and `_*` materialised-table families — they're
    regenerable from base metadata + data values by `analytics-trigger` on
    restore, and they roughly triple the compressed dump size for no benefit.
    """
    print(f">>> Dumping database to {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "docker",
        "exec",
        container,
        "pg_dump",
        "--no-owner",
        "--no-privileges",
        "--no-sync",  # skip fsync — we're dumping an already-durable state
        "--clean",
        "--if-exists",
        # Skip every family of derived/materialised table — they're all
        # regenerated by `analytics-trigger` on restore in a few seconds,
        # and they roughly triple the compressed dump size otherwise.
        "--exclude-table=analytics_*",
        "--exclude-table=aggregated_*",
        "--exclude-table=completeness_*",
        "--exclude-table=_*",  # DHIS2 resource/periodstructure caches etc.
        "-U",
        postgres_user,
        "-d",
        postgres_db,
    ]
    with output.open("wb") as gz_handle, gzip.GzipFile(fileobj=gz_handle, mode="wb", compresslevel=9) as gz:
        proc = subprocess.run(cmd, check=True, capture_output=True)
        gz.write(proc.stdout)
    size = output.stat().st_size
    print(f">>> Wrote {size:,} bytes to {output}")


def detect_postgres_container(default: str) -> str:
    """Return the running postgres container name, falling back to `default`."""
    if shutil.which("docker") is None:
        raise RuntimeError("`docker` CLI not found — need it for pg_dump")
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
        check=True,
    )
    names = [line.strip() for line in result.stdout.splitlines()]
    candidates = [n for n in names if "postgres" in n.lower()]
    if default in names:
        return default
    if len(candidates) == 1:
        return candidates[0]
    if candidates:
        print(f"!!! multiple postgres containers found: {candidates}; defaulting to {candidates[0]}")
        return candidates[0]
    raise RuntimeError(f"no running postgres container detected; expected {default!r}")


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


async def build(url: str, username: str, password: str, output: Path, container: str) -> None:
    """End-to-end: populate DHIS2 → seed auth → dump."""
    print(f">>> Waiting for DHIS2 at {url}")
    await wait_for_ready(url, username, password)
    async with Dhis2Client(url, BasicAuth(username=username, password=password)) as client:
        info = await client.system.info()
        print(f">>> Connected to DHIS2 {info.version} as {username}")

        print(">>> Resolving default category combo")
        cc_uid = await resolve_default_category_combo(client)

        print(">>> Creating metadata")
        await create_org_units(client)
        await create_data_elements(client, cc_uid)
        await create_dataset(client, cc_uid)
        await assign_admin_capture_scope(client)

        print(">>> Creating validation rules + rule group")
        await create_validation_rules(client)

        print(">>> Creating user groups + user role")
        await create_user_groups_and_roles(client)

        print(">>> Creating tracker + event programs")
        await create_tracker_program(client, cc_uid)

        print(">>> Generating data values")
        values = generate_data_values()

        print(">>> Uploading data values")
        await upload_data_values(client, values)

        print(">>> Seeding tracker instances + events")
        await seed_tracker_instances(client)

        print(">>> Running analytics")
        run_analytics()

        print(">>> Seeding OAuth2 client + admin openId mapping")
        await upsert_oauth2_client(client)
        await ensure_user_openid_mapping(client, username)

        print(">>> Applying login-page branding preset")
        await apply_login_customization(client)

    pg_dump(container, output, postgres_user="dhis", postgres_db="dhis")


def main() -> int:
    """Parse args and run the build."""
    default_version = os.environ.get("DHIS2_VERSION", "42")
    parser = argparse.ArgumentParser(
        description="Populate a fresh DHIS2 and dump it to infra/dhis-v{DHIS2_VERSION}.sql.gz.",
    )
    parser.add_argument("--url", default="http://localhost:8080")
    parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="district")
    parser.add_argument(
        "--dhis2-version",
        default=default_version,
        help="DHIS2 major version used to name the dump (default: env DHIS2_VERSION or '42')",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="where to write the gzipped dump (default: infra/dhis-v{dhis2-version}.sql.gz)",
    )
    parser.add_argument(
        "--container",
        default=POSTGRES_CONTAINER_DEFAULT,
        help="name of the running postgres container (auto-detected if not found)",
    )
    args = parser.parse_args()

    output_path = Path(args.output).resolve() if args.output else default_dump_path(args.dhis2_version)
    container = detect_postgres_container(args.container)

    try:
        asyncio.run(build(args.url, args.username, args.password, output_path, container))
    except Exception as exc:  # noqa: BLE001 — top-level runner
        print(f"!!! build failed: {exc}", file=sys.stderr)
        return 1
    print(">>> Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
