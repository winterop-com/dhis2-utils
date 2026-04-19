"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .data_element_params import DataElementParams
    from .tracked_entity_attribute_params import TrackedEntityAttributeParams


class SMSCodeParamsOptionId(_BaseModel):
    """OpenAPI schema `SMSCodeParamsOptionId`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class SMSCodeParams(_BaseModel):
    """OpenAPI schema `SMSCodeParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    code: str | None = None
    compulsory: bool | None = None
    dataElement: DataElementParams | None = None
    formula: str | None = None
    optionId: SMSCodeParamsOptionId | None = None
    trackedEntityAttribute: TrackedEntityAttributeParams | None = None
