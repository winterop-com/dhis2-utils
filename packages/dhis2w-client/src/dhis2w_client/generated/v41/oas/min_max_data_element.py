"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class MinMaxDataElementDataElement(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MinMaxDataElementOptionCombo(_BaseModel):
    """A UID reference to a CategoryOptionCombo  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MinMaxDataElementSource(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MinMaxDataElement(_BaseModel):
    """OpenAPI schema `MinMaxDataElement`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dataElement: MinMaxDataElementDataElement | None = _Field(
        default=None, description="A UID reference to a DataElement  "
    )
    generated: bool | None = None
    max: int | None = None
    min: int | None = None
    optionCombo: MinMaxDataElementOptionCombo | None = _Field(
        default=None, description="A UID reference to a CategoryOptionCombo  "
    )
    source: MinMaxDataElementSource | None = _Field(default=None, description="A UID reference to a OrganisationUnit  ")
