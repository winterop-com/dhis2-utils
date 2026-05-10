"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class TargetRequest(_BaseModel):
    """OpenAPI schema `TargetRequest`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    categoryOptionComboIdScheme: str | None = None
    dataElementIdScheme: str | None = None
    dryRun: bool | None = None
    idScheme: str | None = None
    importStrategy: str | None = None
    orgUnitIdScheme: str | None = None
    skipAudit: bool | None = None
