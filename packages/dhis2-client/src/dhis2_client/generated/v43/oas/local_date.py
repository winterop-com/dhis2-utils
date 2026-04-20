"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DayOfWeek, IsoEra, Month

if TYPE_CHECKING:
    from .iso_chronology import IsoChronology


class LocalDate(_BaseModel):
    """OpenAPI schema `LocalDate`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    chronology: IsoChronology | None = None
    dayOfMonth: int | None = None
    dayOfWeek: DayOfWeek | None = None
    dayOfYear: int | None = None
    era: IsoEra | None = None
    leapYear: bool | None = None
    month: Month | None = None
    monthValue: int | None = None
    year: int | None = None
