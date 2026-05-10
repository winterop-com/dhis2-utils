"""Local patches applied to DHIS2's OpenAPI spec before emission.

DHIS2's springdoc-generated `openapi.json` has known gaps — polymorphic
`oneOf` unions emitted without a discriminator block, variant schemas
missing the Jackson `type` tag, etc. Every such gap has an entry in
`BUGS.md` awaiting an upstream fix.

This module is how we patch around them locally: each `SpecPatch` runs
against the in-memory `components.schemas` dict and mutates it into what
the spec *should* have been. The normal OAS emitter then sees a clean,
idiomatic spec and produces properly-typed pydantic models.

Each patch is idempotent — it checks whether its fix already exists in
the input and short-circuits if upstream has landed a proper fix. When
that happens the patch becomes a no-op and can be retired.

Every patch carries a `bugs_ref` pointer so the log output names which
gap was worked around, and the `BUGS.md` entry stays synced with the
patch.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, ConfigDict


class SpecPatch(BaseModel):
    """One spec patch — mutates `components.schemas` to fix an upstream gap."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    name: str
    bugs_ref: str
    apply: Callable[[dict[str, dict[str, Any]]], bool]


# Wire `type` tags for the 5 DHIS2 auth-scheme subtypes. Stable across v42 + v43.
_AUTH_SCHEME_MAPPING: dict[str, str] = {
    "http-basic": "HttpBasicAuthScheme",
    "api-token": "ApiTokenAuthScheme",
    "api-headers": "ApiHeadersAuthScheme",
    "api-query-params": "ApiQueryParamsAuthScheme",
    "oauth2-client-credentials": "OAuth2ClientCredentialsAuthScheme",
}

# Parents whose `auth` property carries the full `*AuthScheme` oneOf. DHIS2
# reuses the same set across every integration-like resource; every one here
# is a separate upstream omission of the same discriminator block.
_AUTH_SCHEME_PARENTS: tuple[tuple[str, str], ...] = (
    ("Route", "auth"),
    ("RouteParams", "auth"),
    ("WebhookTarget", "auth"),
)


def _inject_auth_scheme_tags(components: dict[str, dict[str, Any]]) -> None:
    """Add a single-value `type` enum to each `*AuthScheme` variant schema.

    Also restores `scopes` on `OAuth2ClientCredentialsAuthScheme` — DHIS2
    omits it from the OAS even though the server accepts + emits it (tracked
    in BUGS.md #14 alongside the discriminator fix).

    Done once per codegen run; idempotent if called again. The variants are
    referenced from multiple parents (`Route.auth`, `RouteParams.auth`,
    `WebhookTarget.auth`) — tagging them at the component level means every
    parent sees the same shape.
    """
    for tag, class_name in _AUTH_SCHEME_MAPPING.items():
        variant = components.get(class_name)
        if not variant:
            continue
        variant.setdefault("properties", {})
        if "type" not in variant["properties"]:
            variant["properties"]["type"] = {"type": "string", "enum": [tag]}

    oauth2 = components.get("OAuth2ClientCredentialsAuthScheme")
    if oauth2 is not None:
        oauth2.setdefault("properties", {})
        if "scopes" not in oauth2["properties"]:
            oauth2["properties"]["scopes"] = {"type": "string"}


def _patch_auth_scheme_discriminators(components: dict[str, dict[str, Any]]) -> bool:
    """Inject the discriminator block for every `<parent>.auth` oneOf of AuthSchemes (BUGS.md #14).

    Handles three separate DHIS2 schemas that share the same polymorphic
    `oneOf` shape: `Route.auth`, `RouteParams.auth`, `WebhookTarget.auth`.
    Upstream DHIS2 emits all three without a discriminator; this patch
    adds the block on each one + tags every variant schema with its
    `type` Literal.

    Returns True when at least one discriminator was added.
    """
    any_patched = False
    # Tag every variant schema first so the emitted variants carry `type`.
    _inject_auth_scheme_tags(components)

    for parent_name, property_name in _AUTH_SCHEME_PARENTS:
        parent = components.get(parent_name)
        if not parent:
            continue
        prop = parent.get("properties", {}).get(property_name)
        if not isinstance(prop, dict) or "oneOf" not in prop:
            continue
        if "discriminator" in prop:
            # Upstream already carries a discriminator — don't clobber.
            continue
        # Only apply if every expected variant is referenced in the spec —
        # short-circuits gracefully if DHIS2 changes the union membership.
        present_variants = {branch.get("$ref", "").rsplit("/", 1)[-1] for branch in prop["oneOf"]}
        if not all(variant in present_variants for variant in _AUTH_SCHEME_MAPPING.values()):
            continue
        prop["discriminator"] = {
            "propertyName": "type",
            "mapping": {tag: f"#/components/schemas/{cls}" for tag, cls in _AUTH_SCHEME_MAPPING.items()},
        }
        any_patched = True
    return any_patched


# DHIS2 v41's `openapi.json` leaks Spring-internal types — `ApplicationContext`,
# `JsonValue`, `JsonObject`, `InputStreamResource` — that aren't part of the
# DHIS2 API surface. They reference types not in `components/schemas`
# (`BeanFactory`, `JsonTypedAccessStore`, `File`, etc.) so the emitted modules
# can't be imported. v42 removed them from the spec output. We strip them
# locally so v41's OAS tree is importable.
_V41_LEAKED_INTERNAL_CLASSES: frozenset[str] = frozenset(
    {
        "ApplicationContext",
        "InputStreamResource",
        "JsonObject",
        "JsonValue",
    },
)


def _drop_v41_internal_classes(components: dict[str, dict[str, Any]]) -> bool:
    """Strip the Spring-internal classes leaked into v41's `/api/openapi.json`.

    Also rewrites every `$ref: #/components/schemas/<name>` that points at one
    of the dropped classes into `{}` (untyped object) — the emitter resolves
    that to `dict[str, Any]`, which is a reasonable fallback for the small
    handful of API-surface classes that referenced these Spring internals.
    """
    dropped = False
    for name in _V41_LEAKED_INTERNAL_CLASSES:
        if name in components:
            del components[name]
            dropped = True
    if not dropped:
        return False
    bad_refs = {f"#/components/schemas/{name}" for name in _V41_LEAKED_INTERNAL_CLASSES}
    _rewrite_dropped_refs(components, bad_refs)
    return True


def _rewrite_dropped_refs(node: Any, bad_refs: set[str]) -> None:
    """Walk `node` recursively and replace `$ref` entries pointing at dropped classes with `{}`."""
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str) and ref in bad_refs:
            node.clear()
            return
        for value in node.values():
            _rewrite_dropped_refs(value, bad_refs)
    elif isinstance(node, list):
        for item in node:
            _rewrite_dropped_refs(item, bad_refs)


ALL_PATCHES: tuple[SpecPatch, ...] = (
    SpecPatch(
        name="auth-scheme-discriminators",
        bugs_ref="BUGS.md#14",
        apply=_patch_auth_scheme_discriminators,
    ),
    SpecPatch(
        name="strip-v41-spring-internals",
        bugs_ref="local — v41-only",
        apply=_drop_v41_internal_classes,
    ),
)


def apply_patches(components: dict[str, dict[str, Any]]) -> list[SpecPatch]:
    """Apply every registered patch to `components`; return the list of patches that fired.

    `components` is mutated in place — the emitter should call this immediately
    after loading the spec and before classification / rendering. The return
    value is used by the CLI to print which gaps were worked around on each run.
    """
    applied: list[SpecPatch] = []
    for patch in ALL_PATCHES:
        if patch.apply(components):
            applied.append(patch)
    return applied
