"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .exchange_source import ExchangeSource
    from .exchange_target import ExchangeTarget
    from .sharing import Sharing
    from .translation import Translation


class AggregateDataExchangeParamsCreatedBy(_BaseModel):
    """OpenAPI schema `AggregateDataExchangeParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class AggregateDataExchangeParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `AggregateDataExchangeParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class AggregateDataExchangeParams(_BaseModel):
    """OpenAPI schema `AggregateDataExchangeParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: AggregateDataExchangeParamsCreatedBy | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: AggregateDataExchangeParamsLastUpdatedBy | None = None
    name: str | None = None
    sharing: Sharing | None = None
    source: ExchangeSource | None = None
    target: ExchangeTarget | None = None
    translations: list[Translation] | None = None
