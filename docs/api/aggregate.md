# Aggregate data values

`DataValue` and `DataValueSet` — the typed wire shapes for DHIS2's aggregate-data path (`/api/dataValueSets` GET / POST and the per-value `/api/dataValues` endpoint). Pairs with [Data values (streaming)](data-values.md), which exposes the same shape via `client.data_values.stream(...)` for very large imports.

## When to reach for it

- Pushing a small or medium batch of aggregate values from a script (CSV-to-DHIS2 sync, ETL pipeline, integration test fixture).
- Reading values back to verify a write landed or to drive an analytics-side check.
- Building the typed payload the streaming accessor and the bulk-grouped helper both consume.

## Worked example — typed write, then read-back

```python
from dhis2w_client import DataValue
from dhis2w_core.client_context import open_client
from dhis2w_core.profile import profile_from_env

async with open_client(profile_from_env()) as client:
    # Push two values via the streaming accessor. The typed `DataValue`s
    # are validated by pydantic before they hit the wire.
    values = [
        DataValue(
            dataElement="fbfJHSPpUQD",
            period="202604",
            orgUnit="ImspTQPwCqd",
            categoryOptionCombo="HllvX50cXC0",
            attributeOptionCombo="HllvX50cXC0",
            value="42",
        ),
        DataValue(
            dataElement="fbfJHSPpUQD",
            period="202605",
            orgUnit="ImspTQPwCqd",
            categoryOptionCombo="HllvX50cXC0",
            attributeOptionCombo="HllvX50cXC0",
            value="43",
        ),
    ]
    envelope = await client.data_values.import_(values)
    print(f"imported={envelope.import_count().imported}  status={envelope.status}")

    # Read back via the typed DataValueSet shape.
    raw = await client.get_raw(
        "/api/dataValueSets",
        params={"dataSet": "lyLU2wR22tC", "period": "202604", "orgUnit": "ImspTQPwCqd"},
    )
    dvs = client.data_values.parse_value_set(raw)
    for v in dvs.dataValues or []:
        print(f"  DE={v.dataElement}  pe={v.period}  ou={v.orgUnit}  value={v.value}")
```

## When to use the grouped helper

`client.data_values.import_grouped_by_dataset(values)` is required on DHIS2 v43 for any `DataElement` that belongs to multiple `DataSet`s (BUGS #35 — v43 rejects the mixed batch with `409 E8002` otherwise). v41 + v42 accept the same envelope shape, so the call works unchanged across the support matrix. See [`examples/v43/client/aggregate_bulk_grouped.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v43/client/aggregate_bulk_grouped.py).

## Related examples

- [`examples/v42/client/push_data_value.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v42/client/push_data_value.py) — minimal single-value push.
- [`examples/v42/client/stream_data_values.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v42/client/stream_data_values.py) — streaming reads, four shapes (bytes, sync generator, Path/CSV, 1000-row file with timing).
- [`examples/v42/client/aggregate_bulk_grouped.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v42/client/aggregate_bulk_grouped.py) — the grouped bulk path.

::: dhis2w_client.v42.aggregate
