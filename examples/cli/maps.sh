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
OPD_MAP=MapOpdCh001
ANC_MAP=MapAncCh001

# ---------------------------------------------------------------------------
# List + inspect
# ---------------------------------------------------------------------------

dhis2 metadata map list
dhis2 metadata map show "$OPD_MAP"

# ---------------------------------------------------------------------------
# Create from flags
# ---------------------------------------------------------------------------

dhis2 metadata map create \
    --name "Demo: deliveries 2024 choropleth" \
    --de DEdelFacilt \
    --pe 2024 \
    --ou NORNorway01 \
    --ou-level 2 \
    --longitude 15 \
    --latitude 64.5 \
    --zoom 4 \
    --classes 5 \
    --color-low '#eff3ff' \
    --color-high '#08519c' \
    --uid MapCliDemo01

# Clone it with a new name.
dhis2 metadata map clone MapCliDemo01 \
    --new-name "Demo: deliveries (clone)" \
    --new-uid MapCliClone1

# ---------------------------------------------------------------------------
# Capture as PNG via the Maps app (requires the [browser] extra)
# ---------------------------------------------------------------------------

# uv add 'dhis2-cli[browser]' && playwright install chromium

dhis2 browser map screenshot \
    --output-dir /tmp/map-screenshots \
    --only "$OPD_MAP" --only "$ANC_MAP"

# ---------------------------------------------------------------------------
# Clean up
# ---------------------------------------------------------------------------

dhis2 metadata map delete MapCliDemo01 -y
dhis2 metadata map delete MapCliClone1 -y
