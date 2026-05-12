# Category option combos

`client.category_option_combos` — read-only accessor over `/api/categoryOptionCombos`. A `CategoryOptionCombo` is one cell of a `CategoryCombo`'s materialised cross-product: a tuple of `CategoryOption` values (e.g. `(Male, <1y)`). The server generates the matrix automatically when a CategoryCombo is saved (with the [v43 manual-regen caveat](category-combos.md#v43-caveat-manual-coc-matrix-regeneration)).

```python
async with Dhis2Client(...) as client:
    cocs = await client.category_option_combos.list_for_combo(combo_uid)
    for coc in cocs:
        print(coc.name, coc.id, [o.id for o in coc.categoryOptions or []])
```

`CategoryOptionCombo` UIDs are the targets of every `DataValue.categoryOptionCombo` / `attributeOptionCombo` reference, so this accessor is the standard way to enumerate the disaggregation slots a data element expects. Writes go through CategoryCombo lifecycle, not directly.

::: dhis2w_client.v42.category_option_combos
