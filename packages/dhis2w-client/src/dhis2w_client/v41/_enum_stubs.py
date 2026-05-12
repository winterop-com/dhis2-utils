"""Local v41 stubs for enums DHIS2 v41's emitted OAS doesn't surface.

DHIS2 v41's `/api/openapi.json` doesn't include these six enums even
though the runtime accepts the same string values that v42 / v43 do
for `/api/metadata` import parameters. v41's codegen output is
faithful to the spec, so the generated tree at
`dhis2w_client.generated.v41.oas` doesn't carry them either.

Until v41's upstream OAS gains these schemas (it likely won't — v41
is in maintenance mode), this hand-written stub gives the v41 plugin
tree a local home for the values without reaching into
`dhis2w_client.generated.v42.oas` cross-version. Wire-identical to v42.

If v41's OAS ever starts emitting these, retarget
`dhis2w_core.v41.plugins.metadata.service` to
`dhis2w_client.generated.v41.oas` and delete this file.
"""

from __future__ import annotations

from enum import StrEnum


class AtomicMode(StrEnum):
    """v41 local stub — `/api/metadata?atomicMode=`."""

    ALL = "ALL"
    NONE = "NONE"


class FlushMode(StrEnum):
    """v41 local stub — `/api/metadata?flushMode=`."""

    OBJECT = "OBJECT"
    AUTO = "AUTO"


class ImportStrategy(StrEnum):
    """v41 local stub — `/api/metadata?importStrategy=`."""

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    CREATE_AND_UPDATE = "CREATE_AND_UPDATE"
    DELETE = "DELETE"
    SYNC = "SYNC"
    NEW_AND_UPDATES = "NEW_AND_UPDATES"
    NEW = "NEW"
    UPDATES = "UPDATES"
    DELETES = "DELETES"


class MergeMode(StrEnum):
    """v41 local stub — `/api/metadata?mergeMode=`."""

    REPLACE = "REPLACE"


class PreheatIdentifier(StrEnum):
    """v41 local stub — `/api/metadata?preheatIdentifier=`."""

    UID = "UID"
    CODE = "CODE"


class PreheatMode(StrEnum):
    """v41 local stub — `/api/metadata?preheatMode=`."""

    REFERENCE = "REFERENCE"
    ALL = "ALL"
    NONE = "NONE"


__all__ = [
    "AtomicMode",
    "FlushMode",
    "ImportStrategy",
    "MergeMode",
    "PreheatIdentifier",
    "PreheatMode",
]
