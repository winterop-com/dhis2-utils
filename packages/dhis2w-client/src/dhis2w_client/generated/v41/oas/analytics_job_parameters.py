"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class AnalyticsJobParameters(_BaseModel):
    """OpenAPI schema `AnalyticsJobParameters`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    lastYears: int | None = None
    skipOutliers: bool | None = None
    skipPrograms: list[str] | None = None
    skipResourceTables: bool | None = None
    skipTableTypes: (
        list[
            Literal[
                "DATA_VALUE",
                "COMPLETENESS",
                "COMPLETENESS_TARGET",
                "ORG_UNIT_TARGET",
                "VALIDATION_RESULT",
                "EVENT",
                "ENROLLMENT",
                "OWNERSHIP",
                "TRACKED_ENTITY_INSTANCE_EVENTS",
                "TRACKED_ENTITY_INSTANCE_ENROLLMENTS",
                "TRACKED_ENTITY_INSTANCE",
            ]
        ]
        | None
    ) = None
