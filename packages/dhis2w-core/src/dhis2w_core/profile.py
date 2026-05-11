"""Profile resolution for dhis2w-core.

Profiles live in either a project-local `.dhis2/profiles.toml` (discovered by
walking up from `$PWD`) or a user-wide `~/.config/dhis2/profiles.toml`.
Environment variables remain supported as a fallback (and as an override via
`DHIS2_PROFILE`).

Resolution precedence (highest wins):
  1. `name` argument to `resolve_profile(name)` — explicit per-call.
  2. `DHIS2_PROFILE` env var — set by CLI `--profile` or MCP server config.
  3. `DHIS2_URL` + credentials env — raw env mode (CI-friendly, no TOML).
  4. Project TOML `default` — nearest `.dhis2/profiles.toml` walking up.
  5. User-wide TOML `default` — `~/.config/dhis2/profiles.toml`.
  6. `NoProfileError` — nothing configured.
"""

from __future__ import annotations

import os
import re
import tomllib
from pathlib import Path
from typing import Literal

import tomli_w
from pydantic import BaseModel, ConfigDict, Field

ProfileSource = Literal["arg", "env-profile", "env-raw", "project-toml", "global-toml"]

ProfileVersion = Literal["v41", "v42", "v43"]


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
    version: ProfileVersion | None = None


class ResolvedProfile(BaseModel):
    """A resolved profile together with its provenance."""

    model_config = ConfigDict(frozen=True)

    name: str
    profile: Profile
    source: ProfileSource
    source_path: Path | None = None


class MergedProfile(BaseModel):
    """An entry in `ProfileCatalog.merged` — a profile plus where it came from."""

    model_config = ConfigDict(frozen=True)

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


class InvalidProfileNameError(ValueError):
    """Raised when a profile name does not match the required format."""


# ---------------------------------------------------------------------------
# Name validation
# ---------------------------------------------------------------------------

PROFILE_NAME_MAX_LEN = 64
_PROFILE_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


def validate_profile_name(name: str) -> str:
    """Validate and return a profile name.

    Rules:
      - must not be empty
      - first character must be an ASCII letter (A-Z, a-z)
      - remaining characters must be letters, digits, or underscore
      - max length 64 characters

    Typical valid names: `local`, `prod`, `prod_eu`, `test42`, `laohis42`.
    Raises `InvalidProfileNameError` on violation. The constraint keeps names
    safe as env var suffixes, TOML keys, and unquoted shell arguments.
    """
    if not name:
        raise InvalidProfileNameError("profile name must be a non-empty string")
    if len(name) > PROFILE_NAME_MAX_LEN:
        raise InvalidProfileNameError(f"profile name {name!r} exceeds the {PROFILE_NAME_MAX_LEN}-character limit")
    if not _PROFILE_NAME_RE.match(name):
        raise InvalidProfileNameError(
            f"profile name {name!r} is invalid — must start with a letter "
            "and contain only letters, digits, and underscores (a-z, A-Z, 0-9, _)"
        )
    return name


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


class ProfileCatalog(BaseModel):
    """Merged profile namespace across project + global TOML files."""

    model_config = ConfigDict(frozen=True)

    project: ProfilesFile
    project_path: Path | None
    global_: ProfilesFile
    global_path: Path

    @property
    def merged(self) -> dict[str, MergedProfile]:
        """Return all profiles keyed by name, project overrides global."""
        merged: dict[str, MergedProfile] = {}
        for name, profile in self.global_.profiles.items():
            merged[name] = MergedProfile(profile=profile, source="global-toml", source_path=self.global_path)
        for name, profile in self.project.profiles.items():
            merged[name] = MergedProfile(profile=profile, source="project-toml", source_path=self.project_path)
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
    # 3. Raw env (DHIS2_URL + creds) — CI-friendly, no TOML needed.
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
    entry = merged[name]
    # If caller asked by explicit name (`arg`/`env-profile`), report THAT origin rather than TOML layer.
    reported_source = source if source in {"arg", "env-profile"} else entry.source
    return ResolvedProfile(name=name, profile=entry.profile, source=reported_source, source_path=entry.source_path)


def _profile_from_env_raw() -> Profile | None:
    base_url = os.environ.get("DHIS2_URL", "").rstrip("/")
    if not base_url:
        return None
    version = _env_version()
    pat = os.environ.get("DHIS2_PAT")
    if pat:
        return Profile(base_url=base_url, auth="pat", token=pat, version=version)
    username = os.environ.get("DHIS2_USERNAME")
    password = os.environ.get("DHIS2_PASSWORD")
    if username and password:
        return Profile(base_url=base_url, auth="basic", username=username, password=password, version=version)
    return None


def _env_version() -> ProfileVersion | None:
    """Read `DHIS2_VERSION` env (`"43"` or `"v43"`) into a `ProfileVersion`.

    Returns None when unset or malformed — `open_client` then falls back to
    auto-detect via `/api/system/info`.
    """
    raw = os.environ.get("DHIS2_VERSION", "").strip().lower()
    if not raw:
        return None
    candidate = raw if raw.startswith("v") else f"v{raw}"
    match candidate:
        case "v41" | "v42" | "v43":
            return candidate
        case _:
            return None


def profile_from_env() -> Profile:
    """Resolve a `Profile` through the full precedence chain (TOML + env).

    Alias for `resolve_profile()` that returns only the `Profile` (drops the
    `ResolvedProfile` envelope). For env-only resolution, read `os.environ`
    directly.
    """
    return resolve_profile()
