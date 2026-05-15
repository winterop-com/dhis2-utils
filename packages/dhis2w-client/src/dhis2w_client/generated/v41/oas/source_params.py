"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class SourceParams(_BaseModel):
    """OpenAPI schema `SourceParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    periodTypes: (
        list[
            Literal[
                "BI_MONTHLY",
                "BI_WEEKLY",
                "DAILY",
                "FINANCIAL_APRIL",
                "FINANCIAL_JULY",
                "FINANCIAL_NOV",
                "FINANCIAL_OCT",
                "MONTHLY",
                "QUARTERLY",
                "QUARTERLY_NOV",
                "SIX_MONTHLY_APRIL",
                "SIX_MONTHLY_NOV",
                "SIX_MONTHLY",
                "TWO_YEARLY",
                "WEEKLY",
                "WEEKLY_SATURDAY",
                "WEEKLY_SUNDAY",
                "WEEKLY_THURSDAY",
                "WEEKLY_WEDNESDAY",
                "YEARLY",
            ]
        ]
        | None
    ) = None
