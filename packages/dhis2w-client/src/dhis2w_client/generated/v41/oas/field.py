"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class Field(_BaseModel):
    """OpenAPI schema `Field`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    categoryOptionCombo: str | None = None
    comment: str | None = None
    dataElement: str | None = None
    label: str | None = None
    optionSet: str | None = None
    type: str | None = None
    value: str | None = None
