#!/usr/bin/env bash
#
# Resolve the pinned `dhis2/core` Docker tag from a minor version key.
#
# When sourced, exports `DHIS2_IMAGE_TAG` (alongside the caller's
# pre-existing `DHIS2_VERSION`) so docker compose picks up both.
# When run directly, prints the tag to stdout — convenient for Make:
#
#     DHIS2_IMAGE_TAG := $(shell scripts/_resolve_image_tag.sh $(DHIS2_VERSION))
#
# Inputs (in priority order):
#   $1                      — minor version key (43)
#   $DHIS2_VERSION env var  — same, used when no positional arg
#
# A fully-qualified tag passed directly (anything containing a dot, e.g.
# "2.43.0.0") bypasses the lookup. Useful for ad-hoc "run a specific tag
# without editing versions.env".
#
# Fails fast if no pin exists for the given minor.
#
# The pin source of truth is `infra/versions.env`. Bumping any pin is an
# explicit action: re-run codegen and commit the regen in the same PR.

set -eu

_input="${1:-${DHIS2_VERSION:-}}"
if [ -z "$_input" ]; then
  echo "_resolve_image_tag.sh: no version provided (positional arg or DHIS2_VERSION env)" >&2
  exit 1
fi

_resolve_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
_versions_env="$_resolve_dir/versions.env"

# Bypass the lookup when the input already looks like a full tag.
case "$_input" in
  *.*)
    _tag="$_input"
    ;;
  *)
    if [ ! -f "$_versions_env" ]; then
      echo "_resolve_image_tag.sh: $_versions_env missing" >&2
      exit 1
    fi
    # shellcheck disable=SC1090
    . "$_versions_env"
    _pin_var="DHIS2_V${_input}"
    if [ -z "${!_pin_var:-}" ]; then
      echo "_resolve_image_tag.sh: no pin for DHIS2_V${_input} in $_versions_env" >&2
      echo "  add 'DHIS2_V${_input}=2.${_input}.0' to fix" >&2
      exit 1
    fi
    _tag="${!_pin_var}"
    ;;
esac

# Sourced: export the resolved tag (and the original minor key for compose's
# dump-path lookup). Run directly: print the tag and exit cleanly.
if (return 0 2>/dev/null); then
  export DHIS2_VERSION="$_input"
  export DHIS2_IMAGE_TAG="$_tag"
else
  printf '%s\n' "$_tag"
fi
