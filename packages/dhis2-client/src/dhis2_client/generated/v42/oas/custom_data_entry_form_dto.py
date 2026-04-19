"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DisplayDensity


class CustomDataEntryFormDto(_BaseModel):
    """OpenAPI schema `CustomDataEntryFormDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dataSetId: str | None = None
    displayDensity: DisplayDensity
    form: str | None = None
    id: str | None = None
    version: int | None = None
