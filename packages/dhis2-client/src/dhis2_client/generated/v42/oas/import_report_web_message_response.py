"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import Status

if TYPE_CHECKING:
    from .stats import Stats
    from .type_report import TypeReport


class ImportReportWebMessageResponse(_BaseModel):
    """OpenAPI schema `ImportReportWebMessageResponse`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    responseType: str | None = None
    stats: Stats | None = None
    status: Status | None = None
    typeReports: list[TypeReport] | None = None
