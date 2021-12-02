#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Downloads file with boundary polygons for LSOAs for the whole UK
# See: https://geoportal.statistics.gov.uk/datasets/ons::lower-layer-super-output-areas-december-2011-boundaries-generalised-clipped-bgc-ew-v3/about

curl -SL -X "GET" "https://opendata.arcgis.com/api/v3/datasets/8bbadffa6ddc493a94078c195a1e293b_0/downloads/data?format=geojson&spatialRefId=4326" -o lsoa-boundaries.geojson
