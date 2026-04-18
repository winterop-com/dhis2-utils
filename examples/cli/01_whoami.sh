#!/usr/bin/env bash
# Simplest possible dhis2 CLI invocation — who am I, and what version is the server?
# Assumes `dhis2 profile add local --default` has been run (or DHIS2_URL + DHIS2_PAT are in env).
set -euo pipefail

dhis2 system whoami
dhis2 system info
