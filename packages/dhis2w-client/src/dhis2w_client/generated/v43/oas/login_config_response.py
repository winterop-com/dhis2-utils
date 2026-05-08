"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .login_oidc_provider import LoginOidcProvider


class LoginConfigResponse(_BaseModel):
    """OpenAPI schema `LoginConfigResponse`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    allowAccountRecovery: bool | None = None
    apiVersion: str | None = None
    applicationDescription: str | None = None
    applicationLeftSideFooter: str | None = None
    applicationNotification: str | None = None
    applicationRightSideFooter: str | None = None
    applicationTitle: str | None = None
    countryFlag: str | None = None
    emailConfigured: bool | None = None
    loginPageLayout: str | None = None
    loginPageLogo: str | None = None
    loginPageTemplate: str | None = None
    loginPopup: str | None = None
    maxPasswordLength: str | None = None
    minPasswordLength: str | None = None
    oidcProviders: list[LoginOidcProvider] | None = None
    recaptchaSite: str | None = None
    selfRegistrationEnabled: bool | None = None
    selfRegistrationNoRecaptcha: bool | None = None
    uiLocale: str | None = None
    useCustomLogoFront: bool | None = None
