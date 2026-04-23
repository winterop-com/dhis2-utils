# Data elements

Three accessors on `Dhis2Client` for the DataElement triple, matching the canonical DHIS2 resource names:

| Accessor | API path | Purpose |
| --- | --- | --- |
| `client.data_elements` | `/api/dataElements` | Atoms of aggregate + tracker data capture. CRUD + rename + legend-set edits. |
| `client.data_element_groups` | `/api/dataElementGroups` | Thematic groupings of DEs (vaccines, ANC indicators, HIV indicators). Per-item membership add/remove. |
| `client.data_element_group_sets` | `/api/dataElementGroupSets` | Analytics dimensions collecting groups ("Vaccine stock", "HIV programme axis"). |

Generic CRUD is still available on the generated accessors (`client.resources.data_elements` + friends). The hand-written accessors layer the keyword-arg creation shapes, partial-update renames, and per-item membership shortcuts that production flows reach for every day.

## No `*Spec` builder

Same design decision as the organisation-unit surface: keyword args on the accessor rather than a spec-over-model hop. `client.data_elements.create(name=..., value_type=..., ...)` dumps a plain dict at the HTTP boundary. This continues to feed the open spec-class audit in [`roadmap.md`](../roadmap.md).

## Worked example

```python
from dhis2_client.generated.v42.enums import DataElementDomain, ValueType

async with Dhis2Client(...) as client:
    de = await client.data_elements.create(
        name="BCG doses given (<1y)",
        short_name="BCG <1y",
        value_type=ValueType.NUMBER,
        domain_type=DataElementDomain.AGGREGATE,
        legend_set_uids=["LsDoseBand1"],
    )

    group = await client.data_element_groups.create(
        name="Immunization indicators",
        short_name="Immun Ind",
    )
    await client.data_element_groups.add_members(group.id, data_element_uids=[de.id])

    dimension = await client.data_element_group_sets.create(
        name="Programme area",
        short_name="Prog Area",
    )
    await client.data_element_group_sets.add_groups(dimension.id, group_uids=[group.id])
```

`create` defaults the `categoryCombo` to the instance default (`client.system.default_category_combo_uid()`); override via `category_combo_uid=` when you have a disaggregation.

## CLI

```bash
dhis2 metadata data-elements list --domain-type AGGREGATE
dhis2 metadata data-elements create --name "BCG doses" --short-name "BCG" --value-type NUMBER --legend-set LsDoseBand1
dhis2 metadata data-element-groups create --name "Vaccines" --short-name "Vacc"
dhis2 metadata data-element-groups add-members <GROUP_UID> --data-element <DE_UID>
dhis2 metadata data-element-group-sets create --name "Programme area" --short-name "ProgArea"
dhis2 metadata data-element-group-sets add-groups <SET_UID> --group <GROUP_UID>
```

Every `list` has an `ls` alias; every destructive verb accepts `--yes` / `-y`.

## MCP

Eighteen tools: `metadata_data_element_{list,show,create,rename,set_legend_sets,delete}`, `metadata_data_element_group_{list,show,members,create,add_members,remove_members,delete}`, `metadata_data_element_group_set_{list,show,create,add_groups,remove_groups,delete}`.

::: dhis2_client.data_elements

::: dhis2_client.data_element_groups

::: dhis2_client.data_element_group_sets
