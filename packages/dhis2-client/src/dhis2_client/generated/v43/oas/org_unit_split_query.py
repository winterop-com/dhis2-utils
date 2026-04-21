"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class OrgUnitSplitQuery(_BaseModel):
    """OpenAPI schema `OrgUnitSplitQuery`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    deleteSource: bool | None = None
    primaryTarget: str | None = None
    source: str | None = None
    targets: list[str] | None = None
