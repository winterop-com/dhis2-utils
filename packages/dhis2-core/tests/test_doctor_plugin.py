"""Tests for the doctor plugin — probe logic, CLI render, plugin descriptor."""

from __future__ import annotations

from collections.abc import Iterator

import httpx
import pytest
import respx
from dhis2_cli.main import build_app
from dhis2_core.plugins.doctor import plugin, service
from dhis2_core.profile import Profile
from typer.testing import CliRunner


@pytest.fixture(autouse=True)
def _isolated_env(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Raw-env profile so `profile_from_env()` resolves without TOML."""
    for key in ("DHIS2_PROFILE", "DHIS2_URL", "DHIS2_PAT", "DHIS2_USERNAME", "DHIS2_PASSWORD"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("DHIS2_URL", "https://dhis2.example")
    monkeypatch.setenv("DHIS2_PAT", "test-token")
    yield


@pytest.fixture
def profile() -> Profile:
    return Profile(base_url="https://dhis2.example", auth="pat", token="test-token")


def _mock_preamble() -> None:
    """Endpoints Dhis2Client.connect() hits before the per-test routes."""
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text=""))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.4"}),
    )


def _mock_all_probes_pass() -> None:
    """Canned responses that make every probe land on `pass`."""
    respx.get("https://dhis2.example/api/me").mock(
        return_value=httpx.Response(200, json={"id": "admin-uid", "username": "admin"}),
    )
    respx.get("https://dhis2.example/api/loginConfig").mock(
        return_value=httpx.Response(
            200,
            json={
                "applicationTitle": "dhis2-utils local",
                "oidcProviders": [{"id": "dhis2"}],
                "useCustomLogoFront": True,
            },
        ),
    )
    respx.get("https://dhis2.example/.well-known/openid-configuration").mock(
        return_value=httpx.Response(
            200,
            json={
                "issuer": "https://dhis2.example",
                "authorization_endpoint": "https://dhis2.example/oauth2/authorize",
                "token_endpoint": "https://dhis2.example/oauth2/token",
                "jwks_uri": "https://dhis2.example/oauth2/jwks",
            },
        ),
    )
    respx.get("https://dhis2.example/api/analytics/rawData").mock(
        return_value=httpx.Response(404, json={"httpStatus": "Not Found", "httpStatusCode": 404}),
    )
    respx.get("https://dhis2.example/api/schemas/userRole").mock(
        return_value=httpx.Response(
            200,
            json={"properties": [{"name": "authority", "fieldName": "authorities"}]},
        ),
    )
    respx.get("https://dhis2.example/api/analytics/outlierDetection").mock(
        return_value=httpx.Response(
            400,
            json={
                "httpStatus": "Bad Request",
                "httpStatusCode": 400,
                "message": "Value 'MOD_Z_SCORE' is not valid for parameter algorithm. "
                "Valid values are: [Z_SCORE, MIN_MAX, MODIFIED_Z_SCORE]",
            },
        ),
    )
    respx.get("https://dhis2.example/api/systemSettings/keyUseCustomLogoFront").mock(
        return_value=httpx.Response(200, json={"keyUseCustomLogoFront": "true"}),
    )


def test_plugin_descriptor() -> None:
    """Plugin registers under the right name + has a description."""
    assert plugin.name == "doctor"
    assert "probe" in plugin.description.lower() or "check" in plugin.description.lower()


@respx.mock
async def test_run_doctor_all_probes_pass(profile: Profile) -> None:
    """Happy path — every probe lands on `pass` against the healthy mock."""
    _mock_preamble()
    _mock_all_probes_pass()
    report = await service.run_doctor(profile)
    assert report.dhis2_version == "2.42.4"
    assert report.base_url == "https://dhis2.example"
    assert report.fail_count == 0
    assert report.warn_count == 0
    # All 8 probes should run and land on pass.
    assert len(report.probes) == 8
    assert report.pass_count == 8


@respx.mock
async def test_run_doctor_version_fails_when_below_minimum(profile: Profile) -> None:
    """Pre-2.42 DHIS2 → dhis2-version probe fails."""
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text=""))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.41.9"}),
    )
    _mock_all_probes_pass()
    report = await service.run_doctor(profile)
    version_probe = next(p for p in report.probes if p.name == "dhis2-version")
    assert version_probe.status == "fail"
    assert "2.42" in version_probe.message


@respx.mock
async def test_run_doctor_oauth2_not_configured_is_skip(profile: Profile) -> None:
    """OAuth2 absence → discovery probe reports `skip`, not `fail`."""
    _mock_preamble()
    _mock_all_probes_pass()
    # Override: discovery 404 means OAuth2 isn't enabled.
    respx.get("https://dhis2.example/.well-known/openid-configuration").mock(
        return_value=httpx.Response(404, json={"httpStatus": "Not Found", "httpStatusCode": 404}),
    )
    report = await service.run_doctor(profile)
    discovery_probe = next(p for p in report.probes if p.name == "oauth2-discovery")
    assert discovery_probe.status == "skip"
    assert "OAuth2 not enabled" in discovery_probe.message


@respx.mock
async def test_run_doctor_rawdata_json_warns_when_bug_gone(profile: Profile) -> None:
    """If /api/analytics/rawData (no suffix) returns 200, BUGS #1 might be fixed upstream."""
    _mock_preamble()
    _mock_all_probes_pass()
    respx.get("https://dhis2.example/api/analytics/rawData").mock(
        return_value=httpx.Response(200, json={"rows": []}),
    )
    report = await service.run_doctor(profile)
    probe = next(p for p in report.probes if p.name == "analytics-rawdata-json-suffix")
    assert probe.status == "warn"
    assert probe.bugs_ref == "BUGS.md #1"


@respx.mock
async def test_run_doctor_userrole_naming_warns_when_shape_changes(profile: Profile) -> None:
    """If the schema shape doesn't match our BUGS #8 assumption, warn rather than fail."""
    _mock_preamble()
    _mock_all_probes_pass()
    respx.get("https://dhis2.example/api/schemas/userRole").mock(
        return_value=httpx.Response(
            200,
            json={"properties": [{"name": "authorities", "fieldName": "authorities"}]},
        ),
    )
    report = await service.run_doctor(profile)
    probe = next(p for p in report.probes if p.name == "userrole-authorities-naming")
    assert probe.status == "warn"


@respx.mock
async def test_run_doctor_outlier_enum_warns_if_server_accepts_old_name(profile: Profile) -> None:
    """If DHIS2 server now accepts MOD_Z_SCORE, BUGS #13 might be fixed — warn to prompt re-check."""
    _mock_preamble()
    _mock_all_probes_pass()
    respx.get("https://dhis2.example/api/analytics/outlierDetection").mock(
        return_value=httpx.Response(200, json={"rows": []}),
    )
    report = await service.run_doctor(profile)
    probe = next(p for p in report.probes if p.name == "outlier-algorithm-enum")
    assert probe.status == "warn"
    assert "MOD_Z_SCORE" in probe.message


@respx.mock
def test_cli_doctor_renders_table_and_exits_zero_on_success() -> None:
    """`dhis2 doctor` against a healthy instance exits 0."""
    _mock_preamble()
    _mock_all_probes_pass()
    result = CliRunner().invoke(build_app(), ["doctor"])
    assert result.exit_code == 0, result.output
    assert "dhis2 doctor" in result.output
    assert "PASS" in result.output


@respx.mock
def test_cli_doctor_json_option_emits_structured_output() -> None:
    """`dhis2 doctor --json` emits the parsed DoctorReport as JSON."""
    _mock_preamble()
    _mock_all_probes_pass()
    result = CliRunner().invoke(build_app(), ["doctor", "--json"])
    assert result.exit_code == 0, result.output
    assert '"probes":' in result.output
    assert '"dhis2_version": "2.42.4"' in result.output


@respx.mock
def test_cli_doctor_exits_nonzero_when_version_fails() -> None:
    """Any probe with status=fail should make the CLI exit non-zero."""
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text=""))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.41.1"}),
    )
    _mock_all_probes_pass()
    result = CliRunner().invoke(build_app(), ["doctor"])
    assert result.exit_code != 0
    assert "FAIL" in result.output
