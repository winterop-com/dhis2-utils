"""Fetch /api/system/info and /api/schemas to build a SchemasManifest."""

from __future__ import annotations

import re
from typing import Any

from dhis2_client import AuthProvider
from dhis2_client.client import Dhis2Client
from pydantic import BaseModel, Field

_VERSION_RE = re.compile(r"^(\d+)\.(\d+)")

# DHIS2 /api/schemas exposes per-property metadata we want in the generated
# models as docstrings + pydantic Field constraints:
# - `owner`      who owns the relationship. A DataElement has `dataElementGroups`
#                but owner=false there — DataElementGroup.dataElements is the
#                writable side. Without this, generated models look symmetric
#                when the API isn't.
# - `required`   drives whether the field is Optional.
# - `readable`/`writable`/`persisted` — signals for clients building forms
#                or round-tripping updates.
# - `unique`     worth flagging in the docstring (uid, code, name typically).
# - `min`/`max`  length bounds for strings / value bounds for numerics.
# - `itemKlass`/`itemPropertyType` — element type for collections.
_SCHEMAS_FIELDS = (
    "fields=name,plural,singular,displayName,apiEndpoint,metadata,klass,persisted,"
    "properties[name,fieldName,propertyType,klass,itemKlass,itemPropertyType,"
    "collection,simple,constants,owner,required,readable,writable,persisted,"
    "unique,min,max]"
)


class SchemaProperty(BaseModel):
    """One property declaration inside a DHIS2 schema."""

    name: str | None = None
    fieldName: str | None = None
    propertyType: str | None = None
    klass: str | None = None
    itemKlass: str | None = None
    itemPropertyType: str | None = None
    collection: bool = False
    simple: bool = True
    constants: list[str] | None = None
    # Relationship / persistence metadata — used for docstrings and to flag
    # non-writable inverse sides of many-to-many relationships.
    owner: bool = False
    required: bool = False
    readable: bool = True
    writable: bool = True
    persisted: bool = True
    unique: bool = False
    min: float | None = None
    max: float | None = None


class Schema(BaseModel):
    """A single metadata type exposed by /api/schemas."""

    name: str
    plural: str | None = None
    singular: str | None = None
    displayName: str | None = None
    apiEndpoint: str | None = None
    metadata: bool = False
    persisted: bool = True
    klass: str | None = None
    properties: list[SchemaProperty] = Field(default_factory=list)


class SchemasManifest(BaseModel):
    """Captured /api/system/info + /api/schemas at a point in time."""

    raw_version: str
    version_key: str
    schemas: list[Schema]


async def discover(url: str, auth: AuthProvider) -> SchemasManifest:
    """Fetch system info and schemas from a live DHIS2 instance."""
    client = Dhis2Client(base_url=url, auth=auth, allow_version_fallback=True)
    try:
        info = await _system_info_without_version_gate(client)
        raw_version = str(info.get("version", ""))
        version_key = _version_key(raw_version)
        schemas_response = await client.get_raw(f"/api/schemas?{_SCHEMAS_FIELDS}")
        schemas = [Schema.model_validate(item) for item in schemas_response.get("schemas", [])]
    finally:
        await client.close()
    return SchemasManifest(raw_version=raw_version, version_key=version_key, schemas=schemas)


async def _system_info_without_version_gate(client: Dhis2Client) -> dict[str, Any]:
    """Open the HTTP pool and fetch /api/system/info, bypassing version dispatch."""
    if client._http is None:  # noqa: SLF001 — intentional reach into client internals for codegen
        import httpx

        client._http = httpx.AsyncClient(base_url=client.base_url, timeout=httpx.Timeout(30.0, connect=60.0))  # noqa: SLF001
    return await client.get_raw("/api/system/info")


def _version_key(raw_version: str) -> str:
    match = _VERSION_RE.match(raw_version)
    if not match:
        raise ValueError(f"could not parse DHIS2 version from {raw_version!r}")
    return f"v{int(match.group(2))}"
