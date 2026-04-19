"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import CompletenessMethod, ParserType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .s_m_s_code_params import SMSCodeParams
    from .s_m_s_special_character import SMSSpecialCharacter
    from .sharing import Sharing
    from .translation import Translation


class SMSCommandParamsCreatedBy(_BaseModel):
    """OpenAPI schema `SMSCommandParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class SMSCommandParamsDataset(_BaseModel):
    """OpenAPI schema `SMSCommandParamsDataset`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class SMSCommandParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `SMSCommandParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class SMSCommandParamsProgram(_BaseModel):
    """OpenAPI schema `SMSCommandParamsProgram`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class SMSCommandParamsProgramStage(_BaseModel):
    """OpenAPI schema `SMSCommandParamsProgramStage`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class SMSCommandParamsUserGroup(_BaseModel):
    """OpenAPI schema `SMSCommandParamsUserGroup`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class SMSCommandParams(_BaseModel):
    """OpenAPI schema `SMSCommandParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    codeValueSeparator: str | None = None
    completenessMethod: CompletenessMethod
    created: datetime | None = None
    createdBy: SMSCommandParamsCreatedBy | None = None
    currentPeriodUsedForReporting: bool | None = None
    dataset: SMSCommandParamsDataset | None = None
    defaultMessage: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: SMSCommandParamsLastUpdatedBy | None = None
    moreThanOneOrgUnitMessage: str
    name: str | None = None
    noUserMessage: str
    parserType: ParserType
    program: SMSCommandParamsProgram | None = None
    programStage: SMSCommandParamsProgramStage | None = None
    receivedMessage: str | None = None
    separator: str | None = None
    sharing: Sharing | None = None
    smsCodes: list[SMSCodeParams] | None = None
    specialCharacters: list[SMSSpecialCharacter] | None = None
    successMessage: str
    translations: list[Translation] | None = None
    userGroup: SMSCommandParamsUserGroup | None = None
    wrongFormatMessage: str | None = None
