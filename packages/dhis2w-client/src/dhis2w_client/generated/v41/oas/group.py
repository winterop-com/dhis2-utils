"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .field import Field


class Group(_BaseModel):
    """OpenAPI schema `Group`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dataElementCount: int | None = None
    description: str | None = None
    fields: list[Field] | None = None
    label: str | None = None
    metaData: dict[str, dict[str, Any]] | None = _Field(default=None, description="keys are class java.lang.Object")
