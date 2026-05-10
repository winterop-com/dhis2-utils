"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .date_filter_period import DateFilterPeriod


class EventDataFilter(_BaseModel):
    """OpenAPI schema `EventDataFilter`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dataItem: str | None = None
    dateFilter: DateFilterPeriod | None = None
    eq: str | None = None
    ge: str | None = None
    gt: str | None = None
    in_: list[str] | None = _Field(default=None, alias="in")
    le: str | None = None
    like: str | None = None
    lt: str | None = None
