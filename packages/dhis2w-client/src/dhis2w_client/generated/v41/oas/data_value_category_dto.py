"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class DataValueCategoryDto(_BaseModel):
    """OpenAPI schema `DataValueCategoryDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    combo: str | None = _Field(default=None, description="A UID for an CategoryCombo object  ")
    options: list[str] | None = None
