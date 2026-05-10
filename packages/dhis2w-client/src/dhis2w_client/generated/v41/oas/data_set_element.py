"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class DataSetElementCategoryCombo(_BaseModel):
    """A UID reference to a CategoryCombo  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSetElementDataElement(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSetElementDataSet(_BaseModel):
    """A UID reference to a DataSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSetElement(_BaseModel):
    """OpenAPI schema `DataSetElement`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    categoryCombo: DataSetElementCategoryCombo | None = _Field(
        default=None, description="A UID reference to a CategoryCombo  "
    )
    dataElement: DataSetElementDataElement | None = _Field(
        default=None, description="A UID reference to a DataElement  "
    )
    dataSet: DataSetElementDataSet | None = _Field(default=None, description="A UID reference to a DataSet  ")
