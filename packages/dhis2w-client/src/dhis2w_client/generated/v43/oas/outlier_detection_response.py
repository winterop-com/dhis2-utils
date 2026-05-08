"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .outlier_detection_metadata import OutlierDetectionMetadata
    from .outlier_value import OutlierValue


class OutlierDetectionResponse(_BaseModel):
    """OpenAPI schema `OutlierDetectionResponse`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    metadata: OutlierDetectionMetadata | None = None
    outlierValues: list[OutlierValue] | None = None
