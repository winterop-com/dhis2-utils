"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .data_value_follow_up_request import DataValueFollowUpRequest


class DataValuesFollowUpRequest(_BaseModel):
    """OpenAPI schema `DataValuesFollowUpRequest`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    values: list[DataValueFollowUpRequest] | None = None
