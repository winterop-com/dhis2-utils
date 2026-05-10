"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class MetadataImportParams(_BaseModel):
    """OpenAPI schema `MetadataImportParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    async_: bool | None = _Field(default=None, alias="async")
    atomicMode: str | None = None
    flushMode: str | None = None
    identifier: str | None = None
    importMode: str | None = None
    importReportMode: str | None = None
    importStrategy: str | None = None
    metadataSyncImport: bool | None = None
    preheatMode: str | None = None
    skipSharing: bool | None = None
    skipTranslation: bool | None = None
    skipValidation: bool | None = None
    user: str | None = _Field(default=None, description="A UID for an User object  ")
