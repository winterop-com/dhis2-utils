"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class SMSCodeDataElement(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SMSCodeOptionId(_BaseModel):
    """A UID reference to a CategoryOptionCombo  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SMSCodeTrackedEntityAttribute(_BaseModel):
    """A UID reference to a TrackedEntityAttribute  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SMSCode(_BaseModel):
    """OpenAPI schema `SMSCode`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    code: str | None = None
    compulsory: bool | None = None
    dataElement: SMSCodeDataElement | None = _Field(default=None, description="A UID reference to a DataElement  ")
    formula: str | None = None
    optionId: SMSCodeOptionId | None = _Field(default=None, description="A UID reference to a CategoryOptionCombo  ")
    trackedEntityAttribute: SMSCodeTrackedEntityAttribute | None = _Field(
        default=None, description="A UID reference to a TrackedEntityAttribute  "
    )
