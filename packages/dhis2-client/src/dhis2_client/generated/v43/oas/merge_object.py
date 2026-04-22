"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class MergeObject(_BaseModel):
    """OpenAPI schema `MergeObject`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    enrollments: list[str] | None = None
    relationships: list[str] | None = None
    trackedEntityAttributes: list[str] | None = None
