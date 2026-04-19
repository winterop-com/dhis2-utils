"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class PredictorGroupParamsCreatedBy(_BaseModel):
    """OpenAPI schema `PredictorGroupParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PredictorGroupParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `PredictorGroupParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PredictorGroupParamsPredictors(_BaseModel):
    """OpenAPI schema `PredictorGroupParamsPredictors`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PredictorGroupParams(_BaseModel):
    """OpenAPI schema `PredictorGroupParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: PredictorGroupParamsCreatedBy | None = None
    description: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: PredictorGroupParamsLastUpdatedBy | None = None
    name: str | None = None
    predictors: list[PredictorGroupParamsPredictors] | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
