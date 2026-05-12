# Categories

`client.categories` — CRUD over `/api/categories` (the second tier of DHIS2's disaggregation model). A `Category` is a named grouping of `CategoryOption`s along one axis (e.g. "Sex", "Age band"). One or more `Category` records get combined into a `CategoryCombo` for the cross-product disaggregation actually attached to data elements.

```python
async with Dhis2Client(...) as client:
    sex = await client.categories.create(
        name="Sex",
        short_name="Sex",
        data_dimension_type="DISAGGREGATION",
        category_option_uids=["male001UID0", "female01UID0"],
    )
    # `.add_option(category_uid, option_uid)` and `.remove_option(...)` are also available.
```

CRUD verbs mirror the standard pattern: `list_all` / `get` / `create` / `update` / `rename` / `delete`. The accessor wraps the typed `Category` model from `dhis2w_client.generated.v42.schemas.category`.

::: dhis2w_client.v42.categories
