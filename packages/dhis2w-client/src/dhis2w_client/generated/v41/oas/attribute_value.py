"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class AttributeValueAttribute(_BaseModel):
    """A UID reference to a Attribute  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class AttributeValue(_BaseModel):
    """OpenAPI schema `AttributeValue`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attribute: AttributeValueAttribute | None = _Field(default=None, description="A UID reference to a Attribute  ")
    value: str | None = None
