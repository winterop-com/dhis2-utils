"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class OrgUnitMergeQuery(_BaseModel):
    """OpenAPI schema `OrgUnitMergeQuery`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dataApprovalMergeStrategy: str | None = None
    dataValueMergeStrategy: str | None = None
    deleteSources: bool | None = None
    sources: list[str] | None = None
    target: str | None = None
