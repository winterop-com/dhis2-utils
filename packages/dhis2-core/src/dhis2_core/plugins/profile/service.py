"""Service layer for the `profile` plugin — profile CRUD + verification."""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dhis2_client import BasicAuth, Dhis2Client, PatAuth
from dhis2_client.auth.base import AuthProvider
from dhis2_client.errors import Dhis2ClientError

from dhis2_core.profile import (
    NoProfileError,
    Profile,
    UnknownProfileError,
    find_project_profiles_file,
    global_profiles_path,
    load_catalog,
    load_profiles_file,
    resolve,
    validate_profile_name,
    write_profiles_file,
)

# ---------------------------------------------------------------------------
# Listing
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProfileSummary:
    """Profile metadata safe to expose without secrets."""

    name: str
    base_url: str
    auth: str
    source: str
    source_path: str | None
    is_default: bool
    shadowed: bool = False  # True if this entry is hidden by a higher-precedence entry with the same name

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "base_url": self.base_url,
            "auth": self.auth,
            "source": self.source,
            "source_path": self.source_path,
            "is_default": self.is_default,
            "shadowed": self.shadowed,
        }


def list_profiles(*, include_shadowed: bool = False, start: Path | None = None) -> list[dict[str, Any]]:
    """Return summaries of every known profile across project + global TOML.

    When `include_shadowed=False` (default), profiles with the same name
    in both scopes are collapsed — only the winning (project) entry shows.
    With `include_shadowed=True`, the shadowed global entry is included too,
    marked `shadowed=True`, so the user can see what's being overridden.
    """
    catalog = load_catalog(start=start)
    default_name = catalog.default_name
    summaries: list[ProfileSummary] = []
    for name, (profile, source, source_path) in sorted(catalog.merged.items()):
        summaries.append(
            ProfileSummary(
                name=name,
                base_url=profile.base_url,
                auth=profile.auth,
                source=source,
                source_path=str(source_path) if source_path else None,
                is_default=(name == default_name),
            )
        )
    if include_shadowed:
        # Surface any global entries that project entries have hidden.
        for name, profile in catalog.global_.profiles.items():
            if name in catalog.project.profiles:
                summaries.append(
                    ProfileSummary(
                        name=name,
                        base_url=profile.base_url,
                        auth=profile.auth,
                        source="global-toml",
                        source_path=str(catalog.global_path),
                        is_default=False,
                        shadowed=True,
                    )
                )
        summaries.sort(key=lambda s: (s.name, s.shadowed))
    return [s.to_dict() for s in summaries]


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class VerifyResult:
    """Outcome of verifying a single profile against a live instance."""

    name: str
    ok: bool
    base_url: str
    auth: str
    version: str | None = None
    username: str | None = None
    latency_ms: int | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "ok": self.ok,
            "base_url": self.base_url,
            "auth": self.auth,
            "version": self.version,
            "username": self.username,
            "latency_ms": self.latency_ms,
            "error": self.error,
        }


async def verify_profile(name: str, *, start: Path | None = None) -> dict[str, Any]:
    """Verify a single profile by calling /api/system/info and /api/me."""
    resolved = resolve(name, start=start)
    return (await _verify_one(resolved.name, resolved.profile)).to_dict()


async def verify_all_profiles(*, start: Path | None = None) -> list[dict[str, Any]]:
    """Verify every known profile; returns one result per profile (ok=False on failure)."""
    catalog = load_catalog(start=start)
    results: list[VerifyResult] = []
    for name in sorted(catalog.merged):
        profile = catalog.merged[name][0]
        results.append(await _verify_one(name, profile))
    return [r.to_dict() for r in results]


async def _verify_one(name: str, profile: Profile) -> VerifyResult:
    """Build a client for the profile, probe /api/system/info + /api/me, report."""
    auth = _build_probe_auth(profile)
    if auth is None:
        return VerifyResult(
            name=name,
            ok=False,
            base_url=profile.base_url,
            auth=profile.auth,
            error=f"verification does not yet support auth type {profile.auth!r}",
        )
    start = time.perf_counter()
    try:
        async with Dhis2Client(profile.base_url, auth=auth, allow_version_fallback=True) as client:
            info = await client.system.info()
            me = await client.system.me()
    except Dhis2ClientError as exc:
        return VerifyResult(name=name, ok=False, base_url=profile.base_url, auth=profile.auth, error=str(exc))
    except Exception as exc:  # noqa: BLE001 — network/DNS/timeout surface as plain str
        return VerifyResult(
            name=name,
            ok=False,
            base_url=profile.base_url,
            auth=profile.auth,
            error=f"{type(exc).__name__}: {exc}",
        )
    latency_ms = int((time.perf_counter() - start) * 1000)
    return VerifyResult(
        name=name,
        ok=True,
        base_url=profile.base_url,
        auth=profile.auth,
        version=info.version,
        username=me.username,
        latency_ms=latency_ms,
    )


def _build_probe_auth(profile: Profile) -> AuthProvider | None:
    """Return a probe-only AuthProvider. OAuth2 profiles are not probed today."""
    if profile.auth == "pat" and profile.token:
        return PatAuth(token=profile.token)
    if profile.auth == "basic" and profile.username and profile.password:
        return BasicAuth(username=profile.username, password=profile.password)
    return None


# ---------------------------------------------------------------------------
# Mutation
# ---------------------------------------------------------------------------


def _resolve_target_path(scope: str, *, start: Path | None = None) -> Path:
    if scope == "project":
        existing = find_project_profiles_file(start)
        if existing is not None:
            return existing
        base = start or Path.cwd()
        return base / ".dhis2" / "profiles.toml"
    if scope == "global":
        return global_profiles_path()
    raise ValueError(f"unknown scope {scope!r}; expected 'project' or 'global'")


@dataclass(frozen=True)
class AddProfileResult:
    """Return value of `add_profile` with shadowing metadata for the caller."""

    path: Path
    shadowed_scope: str | None  # "global" or "project" if this write shadows an existing profile


def add_profile(
    name: str,
    profile: Profile,
    *,
    scope: str = "global",
    make_default: bool = False,
    start: Path | None = None,
) -> AddProfileResult:
    """Upsert a profile into the chosen scope's `profiles.toml`.

    Default scope is `global` (user-wide). Pass `scope="project"` for a
    project-local override. The returned `AddProfileResult.shadowed_scope`
    is set when the write creates (or updates) a profile that shadows or
    is shadowed by another scope — callers (CLI, MCP) can surface a
    warning so the user isn't surprised.
    """
    validate_profile_name(name)
    catalog = load_catalog(start=start)
    shadowed_scope: str | None = None
    if scope == "project" and name in catalog.global_.profiles:
        shadowed_scope = "global"
    elif scope == "global" and name in catalog.project.profiles:
        shadowed_scope = "project"
    path = _resolve_target_path(scope, start=start)
    data = load_profiles_file(path)
    data.profiles[name] = profile
    if make_default or not data.default:
        data.default = name
    write_profiles_file(path, data)
    return AddProfileResult(path=path, shadowed_scope=shadowed_scope)


def remove_profile(name: str, *, scope: str | None = None, start: Path | None = None) -> Path:
    """Remove a profile. If `scope` is None, remove from whichever file holds it."""
    catalog = load_catalog(start=start)
    if name not in catalog.merged:
        raise UnknownProfileError(f"no profile named {name!r}")
    origin_path = catalog.merged[name][2]
    target = _resolve_target_path(scope, start=start) if scope else origin_path
    if target is None:
        raise NoProfileError("cannot remove from project scope — no project profiles.toml exists")
    data = load_profiles_file(target)
    if name not in data.profiles:
        raise UnknownProfileError(f"profile {name!r} is not in {target}")
    del data.profiles[name]
    if data.default == name:
        data.default = next(iter(data.profiles), None)
    write_profiles_file(target, data)
    return target


class ProfileAlreadyExistsError(ValueError):
    """Raised when a rename / create would clobber an existing profile name."""


def rename_profile(old_name: str, new_name: str, *, start: Path | None = None) -> Path:
    """Rename a profile in-place inside whichever file holds it.

    Preserves scope (project / global) and updates the `default` key if the
    renamed profile was the default. Raises `UnknownProfileError` if `old_name`
    isn't defined, `InvalidProfileNameError` if `new_name` fails validation,
    and `ProfileAlreadyExistsError` if `new_name` already exists elsewhere.
    """
    validate_profile_name(new_name)
    catalog = load_catalog(start=start)
    if old_name not in catalog.merged:
        raise UnknownProfileError(f"no profile named {old_name!r}")
    if new_name != old_name and new_name in catalog.merged:
        raise ProfileAlreadyExistsError(
            f"a profile named {new_name!r} already exists; remove it first or pick another name"
        )
    origin_path = catalog.merged[old_name][2]
    if origin_path is None:
        raise NoProfileError(
            f"cannot rename {old_name!r} — it has no source file "
            "(env-raw profiles are derived from environment variables)"
        )
    data = load_profiles_file(origin_path)
    if old_name not in data.profiles:
        raise UnknownProfileError(f"profile {old_name!r} is not present in {origin_path}")
    # Rename while preserving insertion order: build a new dict.
    reordered: dict[str, Profile] = {}
    for key, profile in data.profiles.items():
        reordered[new_name if key == old_name else key] = profile
    data.profiles = reordered
    if data.default == old_name:
        data.default = new_name
    write_profiles_file(origin_path, data)
    return origin_path


def set_default_profile(name: str, *, scope: str = "global", start: Path | None = None) -> Path:
    """Set `default = name` in the chosen scope's `profiles.toml`."""
    validate_profile_name(name)
    path = _resolve_target_path(scope, start=start)
    data = load_profiles_file(path)
    catalog = load_catalog(start=start)
    if name not in catalog.merged and name not in data.profiles:
        raise UnknownProfileError(
            f"no profile named {name!r} exists in project or global files; add it first with `dhis2 profile add`."
        )
    data.default = name
    write_profiles_file(path, data)
    return path


def show_profile(name: str, *, include_secrets: bool = False, start: Path | None = None) -> dict[str, Any]:
    """Return a dict view of one profile. Secrets are redacted unless explicitly requested."""
    resolved = resolve(name, start=start)
    payload = resolved.profile.model_dump(exclude_none=True)
    if not include_secrets:
        for field in ("token", "password", "client_secret"):
            if field in payload:
                payload[field] = "***"
    payload["_meta"] = {
        "name": resolved.name,
        "source": resolved.source,
        "source_path": str(resolved.source_path) if resolved.source_path else None,
    }
    return payload
