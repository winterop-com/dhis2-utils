# Metadata accessor

`MetadataAccessor` bound to `Dhis2Client.metadata` — bulk operations over `/api/metadata` that don't fit the per-resource generated CRUD shape. Per-UID CRUD lives on `client.resources.<resource>`; this accessor is specifically for the multi-resource / multi-UID paths.

## What's here

| Method | Role |
| --- | --- |
| `search(query, ...)` | Cross-resource UID / code / name search. Fans out three concurrent filter calls per match axis and merges by UID. |
| `usage(uid)` | Reverse lookup: "what references this UID?" Resolves the owning resource + finds every object that points at it. |
| `delete_bulk` / `delete_bulk_multi` | Fast-delete via `POST /api/metadata?importStrategy=DELETE`. |
| `patch_bulk` / `patch_bulk_multi` | Apply RFC 6902 patches to many UIDs in parallel. Client-side fan-out over `PATCH /api/<resource>/<uid>`; per-UID failures land in `BulkPatchResult.failures` instead of raising. |
| `dry_run(by_resource)` | Validate a cross-resource bundle without committing (`importMode=VALIDATE`). |

## `patch_bulk` + `BulkPatchResult`

DHIS2 has no bulk-PATCH endpoint, so `patch_bulk` is client-side fan-out with a concurrency cap (default 8). Each `(uid, ops)` pair hits `PATCH /api/<resource>/<uid>` with the RFC 6902 JSON body. Per-UID failures are captured into `BulkPatchResult.failures` instead of raising — callers see a row-level report:

```python
from dhis2w_client import ReplaceOp

result = await client.metadata.patch_bulk(
    "dataElements",
    [
        (de_a_uid, [ReplaceOp(op="replace", path="/shortName", value="A2")]),
        (de_b_uid, [ReplaceOp(op="replace", path="/shortName", value="B2")]),
    ],
)
if not result.ok:
    for failure in result.failures:
        print(failure.uid, failure.status_code, failure.message)
```

Cross-resource variant for mixed types:

```python
result = await client.metadata.patch_bulk_multi(
    {
        "dataElements": [(de_uid, ops_a)],
        "indicators": [(ind_uid, ops_b)],
    },
    concurrency=16,
)
```

Typed `ReplaceOp` / `AddOp` / `RemoveOp` / `MoveOp` / `CopyOp` / `TestOp` models are available on the top-level package; raw dicts matching the RFC 6902 shape are also accepted.

::: dhis2w_client.v42.metadata
