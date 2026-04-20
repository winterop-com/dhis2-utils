#!/usr/bin/env bash
# `dhis2 doctor` — one command, pure reads, probes every known BUGS.md gotcha + workspace requirement.
# Run via `uv run bash examples/cli/doctor.sh`.
set -euo pipefail

echo "--- human-readable report (Rich table)"
dhis2 doctor

echo
echo "--- structured JSON for scripting / CI"
dhis2 doctor --json | python3 -c "
import json, sys
report = json.load(sys.stdin)
print(f'profile={report.get(\"profile_name\")} version={report.get(\"dhis2_version\")}')
for probe in report['probes']:
    print(f'  {probe[\"status\"].upper():4} {probe[\"name\"]}')
"

# dhis2 doctor exits 1 if any probe fails — drop it into CI / Makefile:
# - pass: workspace requirements met, bug workarounds still effective
# - warn: bug may have been fixed upstream; re-check the related BUGS.md entry
# - fail: auth broken, version too old, or a required endpoint is missing
# - skip: feature disabled on this instance (e.g. OAuth2 not configured)
