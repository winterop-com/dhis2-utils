"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .s_m_s_code import SMSCode
    from .s_m_s_special_character import SMSSpecialCharacter
    from .sharing import Sharing
    from .translation import Translation


class SMSCommandCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SMSCommandDataset(_BaseModel):
    """A UID reference to a DataSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SMSCommandLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SMSCommandProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SMSCommandProgramStage(_BaseModel):
    """A UID reference to a ProgramStage  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SMSCommandUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SMSCommandUserGroup(_BaseModel):
    """A UID reference to a UserGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SMSCommand(_BaseModel):
    """OpenAPI schema `SMSCommand`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    codeValueSeparator: str | None = None
    completenessMethod: Literal["ALL_DATAVALUE", "AT_LEAST_ONE_DATAVALUE", "DO_NOT_MARK_COMPLETE"] | None = None
    created: datetime | None = None
    createdBy: SMSCommandCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    currentPeriodUsedForReporting: bool | None = None
    dataset: SMSCommandDataset | None = _Field(default=None, description="A UID reference to a DataSet  ")
    defaultMessage: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: SMSCommandLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    moreThanOneOrgUnitMessage: str | None = None
    name: str | None = None
    noUserMessage: str | None = None
    parserType: (
        Literal[
            "KEY_VALUE_PARSER",
            "J2ME_PARSER",
            "ALERT_PARSER",
            "UNREGISTERED_PARSER",
            "TRACKED_ENTITY_REGISTRATION_PARSER",
            "PROGRAM_STAGE_DATAENTRY_PARSER",
            "EVENT_REGISTRATION_PARSER",
        ]
        | None
    ) = None
    program: SMSCommandProgram | None = _Field(default=None, description="A UID reference to a Program  ")
    programStage: SMSCommandProgramStage | None = _Field(
        default=None, description="A UID reference to a ProgramStage  "
    )
    receivedMessage: str | None = None
    separator: str | None = None
    sharing: Sharing | None = None
    smsCodes: list[SMSCode] | None = None
    specialCharacters: list[SMSSpecialCharacter] | None = None
    successMessage: str | None = None
    translations: list[Translation] | None = None
    user: SMSCommandUser | None = _Field(default=None, description="A UID reference to a User  ")
    userGroup: SMSCommandUserGroup | None = _Field(default=None, description="A UID reference to a UserGroup  ")
    wrongFormatMessage: str | None = None
