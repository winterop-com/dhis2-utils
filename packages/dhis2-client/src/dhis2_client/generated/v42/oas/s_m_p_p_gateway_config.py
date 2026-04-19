"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import BindType, NumberingPlanIndicator, TypeOfNumber


class SMPPGatewayConfig(_BaseModel):
    """OpenAPI schema `SMPPGatewayConfig`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    bindType: BindType
    compressed: bool | None = None
    host: str | None = None
    id: str | None = None
    isDefault: bool | None = None
    maxSmsLength: str | None = None
    name: str | None = None
    numberPlanIndicator: NumberingPlanIndicator
    password: str | None = None
    port: int
    sendUrlParameters: bool | None = None
    systemId: str | None = None
    systemType: str | None = None
    typeOfNumber: TypeOfNumber
    uid: str | None = None
    urlTemplate: str | None = None
    username: str | None = None
