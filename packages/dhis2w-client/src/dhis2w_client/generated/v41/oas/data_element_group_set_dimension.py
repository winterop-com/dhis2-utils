"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class DataElementGroupSetDimensionDataElementGroupSet(_BaseModel):
    """A UID reference to a DataElementGroupSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementGroupSetDimensionDataElementGroups(_BaseModel):
    """A UID reference to a DataElementGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementGroupSetDimension(_BaseModel):
    """OpenAPI schema `DataElementGroupSetDimension`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dataElementGroupSet: DataElementGroupSetDimensionDataElementGroupSet | None = _Field(
        default=None, description="A UID reference to a DataElementGroupSet  "
    )
    dataElementGroups: list[DataElementGroupSetDimensionDataElementGroups] | None = None
