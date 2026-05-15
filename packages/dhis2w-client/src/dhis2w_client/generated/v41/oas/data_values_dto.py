"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .complete_status_dto import CompleteStatusDto
    from .data_value_dto import DataValueDto
    from .min_max_value_dto import MinMaxValueDto


class DataValuesDto(_BaseModel):
    """OpenAPI schema `DataValuesDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    completeStatus: CompleteStatusDto | None = None
    dataValues: list[DataValueDto] | None = None
    lockStatus: Literal["LOCKED", "APPROVED", "OPEN"] | None = None
    minMaxValues: list[MinMaxValueDto] | None = None
