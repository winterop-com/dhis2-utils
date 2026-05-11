"""Branding + theming surface for a DHIS2 instance.

Scope: visual identity that shows up at DHIS2's brand-touchpoints — logos,
CSS theme, application title/footer/notification copy, login-page layout.
Covers the three DHIS2 endpoint families that collectively drive branding:

    POST /api/staticContent/{logo_front,logo_banner}   brand images
    POST /api/files/style                              custom CSS
    POST /api/systemSettings/{key}                     title/intro/footer/theme

The name "login" appears a lot because the login card is the most visible
canvas for restyling, but the CSS + banner + title are served on every page
— authenticated users see the theme too. This is NOT a general file-upload
surface: content attachments live under `/api/documents`, data-element
images live under `/api/fileResources`, and neither is touched here.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from dhis2w_client.generated.v42.oas import LoginConfigResponse

if TYPE_CHECKING:
    from dhis2w_client.v41.client import Dhis2Client


class LoginCustomization(BaseModel):
    """Declarative branding preset — logos + CSS + system settings in one call.

    Named `LoginCustomization` because the login card is the most visible
    canvas, but `logo_banner` + `style_css` + `applicationTitle` apply to the
    authenticated app as well.
    """

    model_config = ConfigDict(extra="forbid")

    logo_front: bytes | None = Field(default=None, description="Bytes for the splash logo (PNG/SVG).")
    logo_banner: bytes | None = Field(default=None, description="Bytes for the top-menu banner logo.")
    style_css: str | None = Field(default=None, description="CSS text uploaded via /api/files/style.")
    system_settings: dict[str, str] = Field(
        default_factory=dict,
        description="Free-form system settings (applicationTitle, applicationIntroduction, ...).",
    )


class CustomizationResult(BaseModel):
    """Summary of a customize apply — what was uploaded + which settings were posted."""

    logo_front_uploaded: bool = False
    logo_banner_uploaded: bool = False
    style_uploaded: bool = False
    settings_applied: list[str] = Field(default_factory=list)


class CustomizeAccessor:
    """Branding + theming endpoints on a DHIS2 instance.

    Three orthogonal endpoint families, one thin accessor:

    - `POST /api/staticContent/{logo_front,logo_banner}` — brand image uploads
      (multipart form; `logo_front` shows on the login card, `logo_banner`
      shows in the top menu on every authenticated page).
    - `POST /api/files/style` — custom CSS injection served on every page.
    - `POST /api/systemSettings/{key}` — per-setting POST with a `text/plain`
      body. Login-only keys: `applicationIntroduction`,
      `applicationNotification`, `loginPageLayout`, `loginPageTemplate`.
      Global keys: `applicationTitle`, `applicationFooter`,
      `applicationRightFooter`, `keyStyle`.

    Stateless — every method is a single DHIS2 call plus `apply_preset` which
    stitches them together. Not a general asset-upload surface; user
    documents live under `/api/documents` and data-element images live under
    `/api/fileResources` (neither is in scope here).
    """

    def __init__(self, client: Dhis2Client) -> None:
        """Bind the accessor to a live client (reuses its auth + HTTP pool)."""
        self._client = client

    async def upload_logo_front(self, data: bytes, *, filename: str = "logo_front.png") -> None:
        """Upload the splash logo (shown on the login card).

        Also sets `keyUseCustomLogoFront = true` so DHIS2 actually serves the
        uploaded bytes — without this flag, `GET /api/staticContent/logo_front.png`
        redirects to the built-in default logo even after a successful upload.
        """
        await self._upload_static_content("logo_front", data, filename)
        await self.set_system_setting("keyUseCustomLogoFront", "true")

    async def upload_logo_banner(self, data: bytes, *, filename: str = "logo_banner.png") -> None:
        """Upload the top-menu banner logo (shown on every authenticated page).

        Also sets `keyUseCustomLogoBanner = true`.
        """
        await self._upload_static_content("logo_banner", data, filename)
        await self.set_system_setting("keyUseCustomLogoBanner", "true")

    async def upload_style(self, css: str) -> None:
        """Upload a CSS stylesheet that DHIS2 serves on every page.

        Sets `keyStyle = style` so the custom stylesheet (stored in
        `keyCustomCss`) becomes the active theme instead of one of DHIS2's
        bundled themes.
        """
        await self._client._request(  # noqa: SLF001 — accessor is intentionally tight with the client
            "POST",
            "/api/files/style",
            content=css.encode("utf-8"),
            extra_headers={"Content-Type": "text/css"},
        )
        await self.set_system_setting("keyStyle", "style")

    async def set_system_setting(self, key: str, value: str) -> None:
        """Set a single system setting via `POST /api/systemSettings/{key}`."""
        await self._client._request(  # noqa: SLF001
            "POST",
            f"/api/systemSettings/{key}",
            content=value.encode("utf-8"),
            extra_headers={"Content-Type": "text/plain"},
        )

    async def set_system_settings(self, settings: Mapping[str, str]) -> list[str]:
        """Set multiple system settings sequentially; returns the keys that were applied."""
        applied: list[str] = []
        for key, value in settings.items():
            await self.set_system_setting(key, value)
            applied.append(key)
        return applied

    async def get_login_config(self) -> LoginConfigResponse:
        """Return DHIS2's read-only `/api/loginConfig` summary (what the login app consumes)."""
        return await self._client.get("/api/loginConfig", model=LoginConfigResponse)

    async def apply_preset(self, preset: LoginCustomization) -> CustomizationResult:
        """Apply a declarative branding preset in one call."""
        result = CustomizationResult()
        if preset.logo_front is not None:
            await self.upload_logo_front(preset.logo_front)
            result.logo_front_uploaded = True
        if preset.logo_banner is not None:
            await self.upload_logo_banner(preset.logo_banner)
            result.logo_banner_uploaded = True
        if preset.style_css is not None:
            await self.upload_style(preset.style_css)
            result.style_uploaded = True
        if preset.system_settings:
            result.settings_applied = await self.set_system_settings(preset.system_settings)
        return result

    async def _upload_static_content(self, key: str, data: bytes, filename: str) -> None:
        """Internal: POST a binary file to `/api/staticContent/{key}`."""
        await self._client._request(  # noqa: SLF001
            "POST",
            f"/api/staticContent/{key}",
            files={"file": (filename, data, _guess_content_type(filename))},
        )


def _guess_content_type(filename: str) -> str:
    """Return a sensible Content-Type for common brand-asset extensions."""
    lowered = filename.lower()
    if lowered.endswith(".png"):
        return "image/png"
    if lowered.endswith((".jpg", ".jpeg")):
        return "image/jpeg"
    if lowered.endswith(".svg"):
        return "image/svg+xml"
    if lowered.endswith(".gif"):
        return "image/gif"
    return "application/octet-stream"
