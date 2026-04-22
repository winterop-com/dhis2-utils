"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import ImportStrategy


class TargetRequest(_BaseModel):
    """OpenAPI schema `TargetRequest`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    categoryOptionComboIdScheme: str | None = None
    dataElementIdScheme: str | None = None
    dryRun: bool | None = None
    idScheme: str | None = None
    importStrategy: ImportStrategy | None = None
    orgUnitIdScheme: str | None = None
    skipAudit: bool | None = None
