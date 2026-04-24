# Tracker schema

The authoring flip side of `dhis2 tracker register / enroll / add-event`. DHIS2's tracker writes need a *schema* on the instance: the `TrackedEntityType` that names the kind of subject, and the `TrackedEntityAttribute`s that describe the fields captured per enrolled TEI. Two accessors cover the leaf half of tracker-schema CRUD:

| Accessor | API path | Purpose |
| --- | --- | --- |
| `client.tracked_entity_attributes` | `/api/trackedEntityAttributes` | Atomic fields on a TEI (National ID, Given Name, DOB, …). CRUD + rename + common toggles (`unique`, `generated`, `confidential`, `inherit`, `pattern`). |
| `client.tracked_entity_types` | `/api/trackedEntityTypes` | The kind of TEI (Person, Case, Animal). CRUD + ordered attribute linkage through `trackedEntityTypeAttributes[]`. |

## Scope

This page covers the leaf tracker-schema resources. The middle layer (`Program` + `programTrackedEntityAttributes[]`) and the inner layer (`ProgramStage` + `programStageDataElements[]` + `programStageSections[]`) ship in follow-up PRs — tracker schema is a linked graph, not a single triple.

## TETA join table

Wiring a TEA onto a TET isn't a simple ref list — the link is a `trackedEntityTypeAttributes[]` entry that carries `mandatory`, `searchable`, and `displayInList` flags. The accessor's `add_attribute` / `remove_attribute` helpers round-trip the full TET, mutate the list, and PUT it back so those flags travel without a dedicated endpoint:

```python
async with Dhis2Client(...) as client:
    national_id = await client.tracked_entity_attributes.create(
        name="National ID",
        short_name="NatID",
        unique=True,
        generated=True,
        pattern="RANDOM(#######)",
    )
    person = await client.tracked_entity_types.create(
        name="Person",
        short_name="Person",
        allow_audit_log=True,
        feature_type="NONE",
    )
    await client.tracked_entity_types.add_attribute(
        person.id,
        national_id.id,
        mandatory=True,
        searchable=True,
    )
```

## Self-ref stripping

DHIS2's `/api/trackedEntityTypes/{uid}` read embeds `trackedEntityTypeAttributes[].trackedEntityType = {id: <parent>}` even though that field is the inverse side the importer rejects on PUT. The accessor strips it automatically before every update, mirroring the DataSet + DataSetElement workaround (BUGS tracker parity — same shape as `_strip_self_ref_from_dse`).

## `unique` + `generated` + `pattern`

DHIS2 supports auto-generated attribute values for registration:

- `unique=True` makes the value unique across the instance (National ID, passport number).
- `generated=True` + `pattern` together mean DHIS2 auto-fills the value when a new TEI is registered.
- Common patterns: `"RANDOM(#######)"` for a 7-digit random suffix, `"#(ORGUNIT)(RANDOM)"` to prefix the TEI's OU.

## No `*Spec` builder

Same call as every other authoring accessor — keyword args. Continues the spec-audit data point.

## CLI

```bash
# TrackedEntityAttribute
dhis2 metadata tracked-entity-attributes create \
    --name "National ID" --short-name NatID --value-type TEXT \
    --unique --generated --pattern "RANDOM(#######)"

# TrackedEntityType + attribute linkage
dhis2 metadata tracked-entity-types create \
    --name Person --short-name Person --allow-audit-log --feature-type NONE
dhis2 metadata tracked-entity-types add-attribute <TET_UID> <TEA_UID> --mandatory --searchable
```

Every `list` has an `ls` alias; every destructive verb accepts `--yes` / `-y`.

## MCP

12 tools: `metadata_tracked_entity_attribute_*` (list / show / create / rename / delete), `metadata_tracked_entity_type_*` (list / show / create / rename / add-attribute / remove-attribute / delete).

## Using them with tracker writes

The point of authoring these here is to make the tracker-write plugin usable end-to-end from CLI alone:

```bash
# 1. author the schema
dhis2 metadata tracked-entity-types create --name Person --short-name Person ...
# 2. use it
dhis2 tracker register --type <TET_UID> --ou <OU_UID> ...
```

See the [tracker plugin](../architecture/tracker.md) for the write-side reference.

::: dhis2_client.tracked_entity_attributes

::: dhis2_client.tracked_entity_types
