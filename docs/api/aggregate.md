# Aggregate data values

`DataValue` and `DataValueSet` — the typed wire shapes for DHIS2's aggregate-data path (`/api/dataValueSets` GET / POST and the per-value `/api/dataValues` endpoint). Pairs with [Data values (streaming)](data-values.md), which exposes the same shape via `client.data_values.stream(...)` for very large imports.

## When to reach for it

- Pushing a small or medium batch of aggregate values from a script (CSV-to-DHIS2 sync, ETL pipeline, integration test fixture).
- Reading values back to verify a write landed or to drive an analytics-side check.
- Building the typed payload the streaming accessor and the bulk-grouped helper both consume.

## Worked example — typed write, then read-back

```python
from dhis2w_client import DataValue, DataValueSet
from dhis2w_core.client_context import open_client
from dhis2w_core.profile import profile_from_env

async with open_client(profile_from_env()) as client:
    # Push two values. `import_grouped_by_dataset` is the cross-version
    # write path (required on v43 BUGS #35, accepted on v41 + v42). The
    # typed `DataValue`s are validated by pydantic before they hit the wire.
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
    envelope = await client.data_values.import_grouped_by_dataset(values)
    count = envelope.import_count()
    print(f"status={envelope.status}  imported={count.imported if count else '?'}")

    # Read back. `/api/dataValueSets` returns the typed DataValueSet shape;
    # validate the raw dict through the pydantic model.
    raw = await client.get_raw(
        "/api/dataValueSets",
        params={"dataSet": "lyLU2wR22tC", "period": "202604", "orgUnit": "ImspTQPwCqd"},
    )
    dvs = DataValueSet.model_validate(raw)
    for v in dvs.dataValues or []:
        print(f"  DE={v.dataElement}  pe={v.period}  ou={v.orgUnit}  value={v.value}")
```

## When to use which write path

`import_grouped_by_dataset(values)` is the safe cross-version default. It pre-fetches each `DataElement`'s `DataSet` membership and POSTs one `{"dataSet": …, "dataValues": [...]}` envelope per group — required on DHIS2 v43 for any DE that belongs to multiple DataSets (BUGS #35: v43 rejects mixed batches with `409 E8002`). v41 + v42 accept the same envelope shape, so the call is portable.

`client.data_values.stream(values, ...)` is the streaming alternative for very large imports — wraps the values as an async-byte stream so httpx doesn't have to materialise the full payload in memory.

## Related examples

- [`examples/v42/client/push_data_value.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v42/client/push_data_value.py) — minimal single-value push.
- [`examples/v42/client/stream_data_values.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v42/client/stream_data_values.py) — streaming reads, four shapes (bytes, sync generator, Path/CSV, 1000-row file with timing).
- [`examples/v42/client/aggregate_bulk_grouped.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v42/client/aggregate_bulk_grouped.py) — the grouped bulk path.

::: dhis2w_client.v42.aggregate
