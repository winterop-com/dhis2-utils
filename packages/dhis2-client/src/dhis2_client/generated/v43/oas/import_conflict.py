"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class ImportConflict(_BaseModel):
    """OpenAPI schema `ImportConflict`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    errorCode: str | None = None
    indexes: list[int] | None = None
    object: str | None = None
    objects: dict[str, str] | None = None
    property: str | None = None
    value: str | None = None
