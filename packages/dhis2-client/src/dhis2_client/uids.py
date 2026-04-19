"""Client-side DHIS2 UID generator — mirrors `dhis2-core/CodeGenerator.java`.

DHIS2 UIDs are 11-character strings over `[0-9A-Za-z]`. The first character
is always a letter (`[A-Za-z]`), the remaining ten are any alphanumeric.
The regex `^[A-Za-z][A-Za-z0-9]{10}$` is the canonical validation form,
used across the DHIS2 codebase.

Upstream reference:
  dhis-2/dhis-api/src/main/java/org/hisp/dhis/common/CodeGenerator.java

Generating client-side avoids a round-trip to `/api/system/id` for every
new UID — useful when minting bulk payloads for `/api/metadata` imports.
Uses `secrets.choice` (CSPRNG) so UIDs are unguessable — which matters for
share-with-user workflows where the UID acts as a capability.
"""

from __future__ import annotations

import re
import secrets

UID_LENGTH = 11
"""Fixed DHIS2 UID length (11 characters)."""

UID_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
"""First-character alphabet — 52 letters, upper + lower."""

UID_ALPHABET = "0123456789" + UID_LETTERS
"""Full 62-character alphanumeric alphabet — digits + upper + lower."""

UID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]{10}$")
"""Canonical DHIS2 UID regex — matches what dhis2-core validates on write."""


def generate_uid() -> str:
    """Return one fresh DHIS2 UID.

    The first character is drawn from the 52-letter alphabet; the remaining
    ten from the 62-character alphanumeric set. Uses `secrets.choice` for
    cryptographic randomness (matches `dhis2-core/CodeGenerator.java`'s
    security-sensitive path).
    """
    first = secrets.choice(UID_LETTERS)
    rest = "".join(secrets.choice(UID_ALPHABET) for _ in range(UID_LENGTH - 1))
    return first + rest


def generate_uids(count: int) -> list[str]:
    """Return `count` fresh DHIS2 UIDs. Collisions are statistically negligible."""
    if count < 0:
        raise ValueError(f"count must be >= 0, got {count}")
    return [generate_uid() for _ in range(count)]


def is_valid_uid(candidate: str) -> bool:
    """Return True iff `candidate` matches DHIS2's canonical UID format."""
    return bool(UID_RE.match(candidate))


__all__ = [
    "UID_ALPHABET",
    "UID_LENGTH",
    "UID_LETTERS",
    "UID_RE",
    "generate_uid",
    "generate_uids",
    "is_valid_uid",
]
