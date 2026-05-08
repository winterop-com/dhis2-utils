"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .base_identifiable_object import BaseIdentifiableObject
    from .category_option_combo import CategoryOptionCombo


class SMSCode(_BaseModel):
    """OpenAPI schema `SMSCode`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    code: str | None = None
    compulsory: bool | None = None
    dataElement: BaseIdentifiableObject | None = None
    formula: str | None = None
    optionId: CategoryOptionCombo | None = None
    trackedEntityAttribute: BaseIdentifiableObject | None = None
