"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class FollowupParams(_BaseModel):
    """OpenAPI schema `FollowupParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeOptionComboId: int | None = None
    categoryOptionComboId: int | None = None
    dataElementId: int | None = None
    followup: bool | None = None
    organisationUnitId: int | None = None
    periodId: int | None = None
