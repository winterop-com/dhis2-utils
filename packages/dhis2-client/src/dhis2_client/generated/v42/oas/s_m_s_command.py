"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import CompletenessMethod, ParserType

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .data_set import DataSet
    from .program import Program
    from .program_stage import ProgramStage
    from .s_m_s_code import SMSCode
    from .s_m_s_special_character import SMSSpecialCharacter
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto
    from .user_group import UserGroup


class SMSCommand(_BaseModel):
    """OpenAPI schema `SMSCommand`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    codeValueSeparator: str | None = None
    completenessMethod: CompletenessMethod | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    currentPeriodUsedForReporting: bool | None = None
    dataset: DataSet | None = None
    defaultMessage: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    moreThanOneOrgUnitMessage: str | None = None
    name: str | None = None
    noUserMessage: str | None = None
    parserType: ParserType | None = None
    program: Program | None = None
    programStage: ProgramStage | None = None
    receivedMessage: str | None = None
    separator: str | None = None
    sharing: Sharing | None = None
    smsCodes: list[SMSCode] | None = None
    specialCharacters: list[SMSSpecialCharacter] | None = None
    successMessage: str | None = None
    translations: list[Translation] | None = None
    userGroup: UserGroup | None = None
    wrongFormatMessage: str | None = None
