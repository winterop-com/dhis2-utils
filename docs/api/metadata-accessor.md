# Metadata accessor

`MetadataAccessor` bound to `Dhis2Client.metadata` — bulk operations over `/api/metadata` that don't fit the per-resource generated CRUD shape. Per-UID CRUD lives on `client.resources.<resource>`; this accessor is specifically for the multi-resource / multi-UID paths.

::: dhis2_client.metadata
