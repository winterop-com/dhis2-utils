"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import LockStatus

if TYPE_CHECKING:
    from .complete_status_dto import CompleteStatusDto
    from .data_value_post_params import DataValuePostParams
    from .min_max_value import MinMaxValue


class DataValuesDto(_BaseModel):
    """OpenAPI schema `DataValuesDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    completeStatus: CompleteStatusDto | None = None
    dataValues: list[DataValuePostParams] | None = None
    lockStatus: LockStatus | None = None
    minMaxValues: list[MinMaxValue] | None = None
