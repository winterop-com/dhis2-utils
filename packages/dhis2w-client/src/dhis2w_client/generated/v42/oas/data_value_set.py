"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .data_value import DataValue


class DataValueSet(_BaseModel):
    """OpenAPI schema `DataValueSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeCategoryOptions: list[str] | None = None
    attributeOptionCombo: str | None = None
    categoryOptionComboIdScheme: str | None = None
    completeDate: str | None = None
    dataElementIdScheme: str | None = None
    dataSet: str | None = None
    dataSetIdScheme: str | None = None
    dataValues: list[DataValue] | None = None
    dryRun: bool | None = None
    idScheme: str | None = None
    orgUnit: str | None = None
    orgUnitIdScheme: str | None = None
    period: str | None = None
    strategy: str | None = None
