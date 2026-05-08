"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import FailurePolicy


class TestJobParameters(_BaseModel):
    """OpenAPI schema `TestJobParameters`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    failAtItem: int | None = None
    failAtStage: int | None = None
    failWithException: bool | None = None
    failWithMessage: str | None = None
    failWithPolicy: FailurePolicy | None = None
    failWithPostCondition: bool | None = None
    itemDuration: int | None = None
    items: int | None = None
    runStagesParallel: bool | None = None
    stages: int | None = None
    waitMillis: int | None = None
