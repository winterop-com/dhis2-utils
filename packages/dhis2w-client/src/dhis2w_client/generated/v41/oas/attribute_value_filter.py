"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .date_filter_period import DateFilterPeriod


class AttributeValueFilter(_BaseModel):
    """OpenAPI schema `AttributeValueFilter`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attribute: str | None = None
    dateFilter: DateFilterPeriod | None = None
    eq: str | None = None
    ew: str | None = None
    ge: str | None = None
    gt: str | None = None
    in_: list[str] | None = _Field(default=None, alias="in")
    le: str | None = None
    like: str | None = None
    lt: str | None = None
    sw: str | None = None
