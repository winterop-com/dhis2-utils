"""Print the DHIS2 versions available on Docker Hub as `dhis2/core` tags.

Used by `make list` in `infra/`. Keeps the logic out of the Makefile so it's
readable and testable. Uses `httpx` (already in the workspace venv).
"""

from __future__ import annotations

import re
import sys

import httpx

_ENDPOINT = "https://hub.docker.com/v2/repositories/dhis2/core/tags"
_VERSION_RE = re.compile(r"^(\d+(?:\.\d+)*)(?:-SNAPSHOT)?$")


def main() -> int:
    """Fetch, filter, and print version-looking tags; return 0 on success."""
    try:
        response = httpx.get(_ENDPOINT, params={"page_size": 100}, timeout=15.0)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"!!! Failed to reach Docker Hub: {exc}", file=sys.stderr)
        return 1

    data = response.json()
    tags: list[tuple[int, int, str]] = []
    for entry in data.get("results", []):
        name = entry.get("name", "")
        match = _VERSION_RE.match(name)
        if not match:
            continue
        parts = [int(p) for p in match.group(1).split(".")]
        if len(parts) < 2:
            continue
        tags.append((parts[0], parts[1], name))

    if not tags:
        print("!!! No version-looking tags found on Docker Hub.", file=sys.stderr)
        return 1

    print("Available DHIS2 versions on Docker Hub (dhis2/core:*):")
    print()
    for major, minor, name in sorted(set(tags), key=lambda t: (t[0], t[1], t[2])):
        print(f"  {name:12}  (major={major} minor={minor})")
    print()
    print("Run a specific version:")
    print("  make up DHIS2_VERSION=42")
    print("  make up DHIS2_VERSION=43")
    print()
    print("Full tag list: https://hub.docker.com/r/dhis2/core/tags")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
