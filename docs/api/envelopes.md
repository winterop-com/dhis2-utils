# Envelopes + responses

The `WebMessageResponse` envelope and its inner shapes (`ObjectReport`, `ImportReport`, `ImportCount`, `Conflict`, `ErrorReport`, `Stats`, `TypeReport`). Every DHIS2 write endpoint — `POST /api/metadata`, `POST /api/dataValueSets`, `POST /api/tracker`, the per-resource write endpoints, etc. — returns one of these shapes.

## When to reach for it

You don't usually instantiate envelopes; you parse them from a write response and branch on the typed fields. The accessor surface returns them already-parsed:

```python
# A bulk metadata import; envelope is a fully-typed model.
envelope = await client.metadata.import_bundle(payload)
assert isinstance(envelope, WebMessageResponse)
```

What you read off it:

- `envelope.status` — `"OK"` / `"WARNING"` / `"ERROR"` / `"SUCCESS"`. Always check this before declaring victory.
- `envelope.message` — a one-line human description (often duplicates `httpStatusCode`'s reason phrase).
- `envelope.import_count()` — convenience accessor on `WebMessageResponse` that walks the typed response into a `ImportCount` (imported / updated / ignored / deleted) without dict navigation.
- `envelope.response.conflicts` — list of `Conflict`s with per-row error messages. Empty on `status="OK"`.
- `envelope.response.typeReports` — per-resource breakdown (e.g. how many DataElements vs DataSets vs OrgUnits landed in a metadata bundle).

## Worked example — write + branch on envelope

```python
from dhis2w_client import DataValue, WebMessageResponse
from dhis2w_core.client_context import open_client
from dhis2w_core.profile import profile_from_env

async with open_client(profile_from_env()) as client:
    values = [
        DataValue(
            dataElement="fbfJHSPpUQD",
            period="202604",
            orgUnit="ImspTQPwCqd",
            categoryOptionCombo="HllvX50cXC0",
            attributeOptionCombo="HllvX50cXC0",
            value="42",
        ),
    ]
    envelope: WebMessageResponse = await client.data_values.import_(values)

    count = envelope.import_count()
    if envelope.status == "OK" and count.ignored == 0:
        print(f"imported={count.imported}  updated={count.updated}")
    else:
        # Conflict shape: row index + per-field message. Read first 5.
        for conflict in (envelope.response.conflicts or [])[:5]:
            print(f"  row {conflict.object} -> {conflict.value}")
        raise RuntimeError(f"import failed: status={envelope.status} message={envelope.message}")
```

## Error-side shape

Failed writes raise `Dhis2ApiError` whose `.envelope` field carries the parsed `WebMessageResponse` (when DHIS2 returned one). Same fields available — the typed `conflicts` list is the actionable bit.

```python
from dhis2w_client import Dhis2ApiError

try:
    await client.metadata.import_bundle(bad_payload)
except Dhis2ApiError as exc:
    if exc.envelope is not None:
        for c in exc.envelope.response.conflicts or []:
            print(f"  {c.object}: {c.value}")
```

## Related examples

- [`examples/v42/client/error_handling.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v42/client/error_handling.py) — `Dhis2ApiError` + WebMessage conflict shape.
- [`examples/v42/client/metadata_bulk_import.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v42/client/metadata_bulk_import.py) — typed dry-run + real import branching on the envelope.

::: dhis2w_client.v42.envelopes
