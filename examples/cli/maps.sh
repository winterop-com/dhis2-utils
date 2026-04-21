#!/usr/bin/env bash
# `dhis2 metadata map ...` + `dhis2 browser map screenshot` —
# thematic choropleth authoring + PNG capture.
#
# A DHIS2 Map is a viewport (longitude, latitude, zoom) plus an ordered
# list of layers. Thematic (choropleth) is the most common layer type
# and is what `dhis2 metadata map create` builds from flags. Multi-layer
# maps (thematic + boundary + facility) need raw construction from the
# library side.
set -euo pipefail

# Seeded thematic choropleths shipped with the e2e dump.
DOSES_MAP=y3jLMnZTV6i
IMMUNIZATION_MAP=iKgbemGaDUh

# ---------------------------------------------------------------------------
# List + inspect
# ---------------------------------------------------------------------------

dhis2 metadata map list
dhis2 metadata map show "$DOSES_MAP"

# ---------------------------------------------------------------------------
# Create from flags
# ---------------------------------------------------------------------------

dhis2 metadata map create \
    --name "Demo: first doses given 2024 choropleth" \
    --de I78gJm4KBo7 \
    --pe 2024 \
    --ou ImspTQPwCqd \
    --ou-level 2 \
    --longitude 15 \
    --latitude 64.5 \
    --zoom 4 \
    --classes 5 \
    --color-low '#eff3ff' \
    --color-high '#08519c' \
    --uid MapCliDem01

# Clone it with a new name.
dhis2 metadata map clone MapCliDem01 \
    --new-name "Demo: first doses given (clone)" \
    --new-uid MapCliCln01

# ---------------------------------------------------------------------------
# Capture as PNG via the Maps app (requires the [browser] extra)
# ---------------------------------------------------------------------------

# uv add 'dhis2-cli[browser]' && playwright install chromium

dhis2 browser map screenshot \
    --output-dir /tmp/map-screenshots \
    --only "$DOSES_MAP" --only "$IMMUNIZATION_MAP"

# ---------------------------------------------------------------------------
# Clean up
# ---------------------------------------------------------------------------

dhis2 metadata map delete MapCliDem01 -y
dhis2 metadata map delete MapCliCln01 -y
