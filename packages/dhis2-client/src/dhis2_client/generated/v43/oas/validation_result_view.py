"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class ValidationResultView(_BaseModel):
    """OpenAPI schema `ValidationResultView`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeOptionComboDisplayName: str | None = None
    attributeOptionComboId: str | None = None
    importance: str | None = None
    leftSideValue: float | None = None
    operator: str | None = None
    organisationUnitAncestorNames: str | None = None
    organisationUnitDisplayName: str | None = None
    organisationUnitId: str | None = None
    organisationUnitPath: str | None = None
    periodDisplayName: str | None = None
    periodId: str | None = None
    rightSideValue: float | None = None
    validationRuleDescription: str | None = None
    validationRuleId: str | None = None
