"""Profile resolution for dhis2-core.

Profiles live in either a project-local `.dhis2/profiles.toml` (discovered by
walking up from `$PWD`) or a user-wide `~/.config/dhis2/profiles.toml`.
Environment variables remain supported as a fallback (and as an override via
`DHIS2_PROFILE`).

Resolution precedence (highest wins):
  1. `name` argument to `resolve_profile(name)` — explicit per-call.
  2. `DHIS2_PROFILE` env var — set by CLI `--profile` or MCP server config.
  3. `DHIS2_URL` + credentials env — raw env mode (backward compat, no TOML).
  4. Project TOML `default` — nearest `.dhis2/profiles.toml` walking up.
  5. User-wide TOML `default` — `~/.config/dhis2/profiles.toml`.
  6. `NoProfileError` — nothing configured.
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import tomli_w
from pydantic import BaseModel, ConfigDict, Field

ProfileSource = Literal["arg", "env-profile", "env-raw", "project-toml", "global-toml"]


class Profile(BaseModel):
    """Resolved DHIS2 connection settings for a single session."""

    model_config = ConfigDict(frozen=True)

    base_url: str
    auth: Literal["pat", "basic", "oauth2"]
    token: str | None = None
    username: str | None = None
    password: str | None = None
    client_id: str | None = None
    client_secret: str | None = None
    scope: str | None = None
    redirect_uri: str | None = None


@dataclass(frozen=True)
class ResolvedProfile:
    """A resolved profile together with its provenance."""

    name: str
    profile: Profile
    source: ProfileSource
    source_path: Path | None = None


class ProfilesFile(BaseModel):
    """Parsed contents of a `profiles.toml` file."""

    default: str | None = None
    profiles: dict[str, Profile] = Field(default_factory=dict)


class NoProfileError(RuntimeError):
    """Raised when no DHIS2 profile can be resolved."""


class UnknownProfileError(LookupError):
    """Raised when a named profile is requested but does not exist in any profile file."""


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_DIRNAME = ".dhis2"
PROFILES_FILENAME = "profiles.toml"


def global_profiles_path() -> Path:
    """Return `~/.config/dhis2/profiles.toml` (does not create it)."""
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg) if xdg else Path.home() / ".config"
    return base / "dhis2" / PROFILES_FILENAME


def find_project_profiles_file(start: Path | None = None) -> Path | None:
    """Walk up from `start` (defaulting to `$PWD`) looking for `.dhis2/profiles.toml`."""
    cwd = start or Path.cwd()
    for parent in [cwd, *cwd.parents]:
        candidate = parent / PROJECT_DIRNAME / PROFILES_FILENAME
        if candidate.exists():
            return candidate
    return None


# ---------------------------------------------------------------------------
# Read / write
# ---------------------------------------------------------------------------


def load_profiles_file(path: Path) -> ProfilesFile:
    """Load a `profiles.toml` file. Missing file → empty `ProfilesFile`."""
    if not path.exists():
        return ProfilesFile()
    raw = tomllib.loads(path.read_text(encoding="utf-8"))
    default = raw.get("default")
    profiles_section = raw.get("profiles", {})
    profiles: dict[str, Profile] = {}
    for name, settings in profiles_section.items():
        if not isinstance(settings, dict):
            continue
        profiles[name] = Profile.model_validate(settings)
    return ProfilesFile(default=default, profiles=profiles)


def write_profiles_file(path: Path, data: ProfilesFile) -> None:
    """Write a `profiles.toml` file with 0600 perms. Creates parents as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, object] = {}
    if data.default is not None:
        payload["default"] = data.default
    if data.profiles:
        payload["profiles"] = {
            name: {k: v for k, v in profile.model_dump(exclude_none=True).items()}
            for name, profile in data.profiles.items()
        }
    path.write_text(tomli_w.dumps(payload), encoding="utf-8")
    path.chmod(0o600)


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProfileCatalog:
    """Merged profile namespace across project + global TOML files."""

    project: ProfilesFile
    project_path: Path | None
    global_: ProfilesFile
    global_path: Path

    @property
    def merged(self) -> dict[str, tuple[Profile, ProfileSource, Path | None]]:
        """Return all profiles keyed by name, project overrides global."""
        merged: dict[str, tuple[Profile, ProfileSource, Path | None]] = {}
        for name, profile in self.global_.profiles.items():
            merged[name] = (profile, "global-toml", self.global_path)
        for name, profile in self.project.profiles.items():
            merged[name] = (profile, "project-toml", self.project_path)
        return merged

    @property
    def default_name(self) -> str | None:
        """Return the effective default name (project wins over global)."""
        return self.project.default or self.global_.default


def load_catalog(start: Path | None = None) -> ProfileCatalog:
    """Load and merge profiles from the project and global TOML files."""
    project_path = find_project_profiles_file(start)
    project = load_profiles_file(project_path) if project_path else ProfilesFile()
    global_path = global_profiles_path()
    global_ = load_profiles_file(global_path)
    return ProfileCatalog(project=project, project_path=project_path, global_=global_, global_path=global_path)


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------


def resolve_profile(name: str | None = None, *, start: Path | None = None) -> Profile:
    """Resolve a `Profile` using the documented precedence chain."""
    return resolve(name, start=start).profile


def resolve(name: str | None = None, *, start: Path | None = None) -> ResolvedProfile:
    """Return the resolved profile together with its provenance."""
    # 1. Explicit name argument.
    if name:
        return _resolve_by_name(name, source="arg", start=start)
    # 2. DHIS2_PROFILE env var.
    env_name = os.environ.get("DHIS2_PROFILE")
    if env_name:
        return _resolve_by_name(env_name, source="env-profile", start=start)
    # 3. Raw env (DHIS2_URL + creds) — backward compat.
    raw = _profile_from_env_raw()
    if raw is not None:
        return ResolvedProfile(name="<env>", profile=raw, source="env-raw")
    # 4. Project TOML default.
    # 5. Global TOML default.
    catalog = load_catalog(start=start)
    default_name = catalog.default_name
    if default_name:
        return _resolve_by_name(default_name, source="project-toml", start=start, catalog=catalog)
    raise NoProfileError("no DHIS2 profile is configured")


def _resolve_by_name(
    name: str,
    *,
    source: ProfileSource,
    start: Path | None,
    catalog: ProfileCatalog | None = None,
) -> ResolvedProfile:
    catalog = catalog or load_catalog(start=start)
    merged = catalog.merged
    if name not in merged:
        available = sorted(merged)
        raise UnknownProfileError(
            f"no profile named {name!r} (available: {', '.join(available) if available else 'none'}). "
            "Run `dhis2 profile list` to see all profiles."
        )
    profile, origin_source, origin_path = merged[name]
    # If caller asked by explicit name (`arg`/`env-profile`), report THAT origin rather than TOML layer.
    reported_source = source if source in {"arg", "env-profile"} else origin_source
    return ResolvedProfile(name=name, profile=profile, source=reported_source, source_path=origin_path)


def _profile_from_env_raw() -> Profile | None:
    base_url = os.environ.get("DHIS2_URL", "").rstrip("/")
    if not base_url:
        return None
    pat = os.environ.get("DHIS2_PAT")
    if pat:
        return Profile(base_url=base_url, auth="pat", token=pat)
    username = os.environ.get("DHIS2_USERNAME")
    password = os.environ.get("DHIS2_PASSWORD")
    if username and password:
        return Profile(base_url=base_url, auth="basic", username=username, password=password)
    return None


# ---------------------------------------------------------------------------
# Backward-compat alias
# ---------------------------------------------------------------------------


def profile_from_env() -> Profile:
    """Resolve a Profile via the full precedence chain (backward-compatible alias).

    Existing code may import this as `profile_from_env`; it now resolves from
    TOML as well as env. To guarantee env-only resolution, read `os.environ`
    directly.
    """
    return resolve_profile()
