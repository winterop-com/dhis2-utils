"""Re-apply the committed login-page branding preset against a running DHIS2."""

from __future__ import annotations

import json
from pathlib import Path

from dhis2_client import Dhis2Client, LoginCustomization

LOGIN_CUSTOMIZATION_DIR = Path(__file__).resolve().parents[1] / "login-customization"


async def apply_login_customization(client: Dhis2Client) -> None:
    """Upload the logos + style + system settings from `infra/login-customization/`."""
    preset = LoginCustomization()
    logo_front = LOGIN_CUSTOMIZATION_DIR / "logo_front.png"
    if logo_front.exists():
        preset.logo_front = logo_front.read_bytes()
    logo_banner = LOGIN_CUSTOMIZATION_DIR / "logo_banner.png"
    if logo_banner.exists():
        preset.logo_banner = logo_banner.read_bytes()
    style = LOGIN_CUSTOMIZATION_DIR / "style.css"
    if style.exists():
        preset.style_css = style.read_text(encoding="utf-8")
    settings_file = LOGIN_CUSTOMIZATION_DIR / "preset.json"
    if settings_file.exists():
        loaded = json.loads(settings_file.read_text(encoding="utf-8"))
        preset.system_settings = {str(k): str(v) for k, v in loaded.items()}
    result = await client.customize.apply_preset(preset)
    print(
        f"    applied branding: logo_front={result.logo_front_uploaded} "
        f"logo_banner={result.logo_banner_uploaded} style={result.style_uploaded} "
        f"settings={len(result.settings_applied)}",
    )
