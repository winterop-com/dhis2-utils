# JSON Patch operations

RFC 6902 JSON Patch op types + a typed `JsonPatchOpAdapter` for round-tripping ops through DHIS2's `PATCH /api/{resource}/{uid}` endpoint. The discriminator on `op` (`add`, `remove`, `replace`, `move`, `copy`, `test`) routes to the matching `BaseModel` subclass.

```python
from dhis2w_client import JsonPatchOpAdapter

op = JsonPatchOpAdapter.validate_python({"op": "replace", "path": "/name", "value": "ANC 2024"})
# -> ReplaceOp(op='replace', path='/name', value='ANC 2024')

await client.resources.programs.patch(program_uid, [op])
```

The adapter accepts both Python dicts and JSON strings; outputs dump back via `.model_dump()` / `.model_dump_json()`. Property-based tests in `tests/test_parser_properties.py` cover the round-trip and discriminator dispatch for every variant.

## When to reach for this

- Bulk-patching one field across many resources where a full PUT round-trip is wasteful.
- Server-side conditional ops (`test` followed by `replace` in one batch).
- Custom patch generators (CSV-driven sweeps, drift-detection auto-fixes).

For the higher-level batch patcher see `client.metadata.patch_bulk` on [Metadata accessor](metadata-accessor.md).

::: dhis2w_client.v42.json_patch
