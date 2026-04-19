"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import (
    AtomicMode,
    FlushMode,
    ImportReportMode,
    ImportStrategy,
    ObjectBundleMode,
    PreheatIdentifier,
    PreheatMode,
)


class MetadataImportParams(_BaseModel):
    """OpenAPI schema `MetadataImportParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    async_: bool | None = _Field(default=None, alias="async")
    atomicMode: AtomicMode
    flushMode: FlushMode
    identifier: PreheatIdentifier
    importMode: ObjectBundleMode
    importReportMode: ImportReportMode
    importStrategy: ImportStrategy
    metadataSyncImport: bool | None = None
    preheatMode: PreheatMode
    skipSharing: bool | None = None
    skipTranslation: bool | None = None
    skipValidation: bool | None = None
    user: str | None = None
