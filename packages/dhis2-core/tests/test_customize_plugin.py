"""Unit tests for the customize plugin — CLI surface + descriptor + preset-dir loader."""

from __future__ import annotations

import json
from pathlib import Path
from types import TracebackType
from unittest.mock import patch

import pytest
from dhis2_client.customize import CustomizationResult, LoginCustomization
from dhis2_core.plugins.customize import plugin, service
from dhis2_core.plugins.customize.cli import app as customize_app
from dhis2_core.plugins.dev.cli import app as dev_app
from typer.testing import CliRunner

_runner = CliRunner()


def test_plugin_descriptor_is_mcp_only() -> None:
    """The plugin's CLI is mounted by the dev plugin — register_cli here is a no-op."""
    assert plugin.name == "customize"
    # Calling register_cli should not explode and should not mount anything.
    plugin.register_cli(object())


def test_cli_is_mounted_under_dev() -> None:
    """`dhis2 dev customize` must resolve (regression for the dev-vs-root mount decision)."""
    result = _runner.invoke(dev_app, ["customize", "--help"])
    assert result.exit_code == 0, result.output
    assert "logo-front" in result.output
    assert "logo-banner" in result.output
    assert "apply" in result.output
    assert "show" in result.output


def test_cli_help_lists_every_verb() -> None:
    """Direct help on the customize app lists the full verb surface."""
    result = _runner.invoke(customize_app, ["--help"])
    assert result.exit_code == 0
    for verb in ("logo-front", "logo-banner", "style", "set", "settings", "apply", "show"):
        assert verb in result.output


def test_apply_preset_dir_skips_missing_files(tmp_path: Path) -> None:
    """Empty preset dir is a valid no-op — only preset.json / logos / style.css are picked up."""

    class _FakeClient:
        def __init__(self) -> None:
            self.customize = self

        async def apply_preset(self, preset: LoginCustomization) -> CustomizationResult:
            assert preset.logo_front is None
            assert preset.logo_banner is None
            assert preset.style_css is None
            assert preset.system_settings == {}
            return CustomizationResult()

        async def __aenter__(self) -> _FakeClient:
            return self

        async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc: BaseException | None,
            tb: TracebackType | None,
        ) -> None:
            return None

    async def _run() -> CustomizationResult:
        with patch("dhis2_core.plugins.customize.service.open_client", return_value=_FakeClient()):
            return await service.apply_preset_dir(profile=None, directory=tmp_path)  # type: ignore[arg-type]

    import asyncio

    result = asyncio.run(_run())
    assert not result.logo_front_uploaded


def test_apply_preset_dir_loads_every_file_when_present(tmp_path: Path) -> None:
    """When every file exists, the preset gets logos + CSS + settings populated."""
    (tmp_path / "logo_front.png").write_bytes(b"front-png")
    (tmp_path / "logo_banner.png").write_bytes(b"banner-png")
    (tmp_path / "style.css").write_text("body{}", encoding="utf-8")
    (tmp_path / "preset.json").write_text(
        json.dumps({"applicationTitle": "hello", "keyApplicationFooter": "bye"}),
        encoding="utf-8",
    )

    captured: dict[str, LoginCustomization] = {}

    class _FakeClient:
        def __init__(self) -> None:
            self.customize = self

        async def apply_preset(self, preset: LoginCustomization) -> CustomizationResult:
            captured["preset"] = preset
            return CustomizationResult(
                logo_front_uploaded=True,
                logo_banner_uploaded=True,
                style_uploaded=True,
                settings_applied=list(preset.system_settings),
            )

        async def __aenter__(self) -> _FakeClient:
            return self

        async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc: BaseException | None,
            tb: TracebackType | None,
        ) -> None:
            return None

    async def _run() -> CustomizationResult:
        with patch("dhis2_core.plugins.customize.service.open_client", return_value=_FakeClient()):
            return await service.apply_preset_dir(profile=None, directory=tmp_path)  # type: ignore[arg-type]

    import asyncio

    result = asyncio.run(_run())
    preset = captured["preset"]
    assert preset.logo_front == b"front-png"
    assert preset.logo_banner == b"banner-png"
    assert preset.style_css == "body{}"
    assert preset.system_settings == {"applicationTitle": "hello", "keyApplicationFooter": "bye"}
    assert result.settings_applied == ["applicationTitle", "keyApplicationFooter"]


def test_apply_preset_dir_rejects_non_object_json(tmp_path: Path) -> None:
    """preset.json must be a {key: value} object — a top-level list raises ValueError."""
    (tmp_path / "preset.json").write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="preset.json"):
        import asyncio

        asyncio.run(service.apply_preset_dir(profile=None, directory=tmp_path))  # type: ignore[arg-type]


def test_settings_cli_rejects_non_object(tmp_path: Path) -> None:
    """`dhis2 dev customize settings file.json` fails on non-object JSON."""
    bad = tmp_path / "bad.json"
    bad.write_text('["a", "b"]', encoding="utf-8")
    result = _runner.invoke(customize_app, ["settings", str(bad)])
    assert result.exit_code != 0
    assert "object" in result.output.lower() or "key" in result.output.lower()


def test_apply_cli_rejects_non_directory(tmp_path: Path) -> None:
    """`dhis2 dev customize apply FILE` should fail-fast with a clear message."""
    f = tmp_path / "not-a-dir.txt"
    f.write_text("x")
    result = _runner.invoke(customize_app, ["apply", str(f)])
    assert result.exit_code != 0
    assert "directory" in result.output.lower()
