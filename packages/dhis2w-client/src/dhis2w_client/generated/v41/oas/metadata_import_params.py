"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class MetadataImportParams(_BaseModel):
    """OpenAPI schema `MetadataImportParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    async_: bool | None = _Field(default=None, alias="async")
    atomicMode: Literal["ALL", "NONE"] | None = None
    flushMode: Literal["OBJECT", "AUTO"] | None = None
    identifier: Literal["UID", "CODE"] | None = None
    importMode: Literal["COMMIT", "VALIDATE"] | None = None
    importReportMode: Literal["FULL", "ERRORS", "ERRORS_NOT_OWNER", "DEBUG"] | None = None
    importStrategy: (
        Literal[
            "CREATE", "UPDATE", "CREATE_AND_UPDATE", "DELETE", "SYNC", "NEW_AND_UPDATES", "NEW", "UPDATES", "DELETES"
        ]
        | None
    ) = None
    metadataSyncImport: bool | None = None
    preheatMode: Literal["REFERENCE", "ALL", "NONE"] | None = None
    skipSharing: bool | None = None
    skipTranslation: bool | None = None
    skipValidation: bool | None = None
    user: str | None = _Field(default=None, description="A UID for an User object  ")
