#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Downloads The Scottish Indices of Deprivation 2020 data set in shapefile format.
# For details of the data see: https://www.spatialdata.gov.scot/geonetwork/srv/eng/catalog.search#/metadata/02866b0b-66e5-46ab-9b1c-d433dc3c2fae

IMD_DOWNLOAD_URL="https://maps.gov.scot/ATOM/shapefiles/SG_SIMD_2020.zip"
OUT_FILE="scotland-imd"

curl -SL -X "GET" $IMD_DOWNLOAD_URL -o "${OUT_FILE}.zip"
unzip "${OUT_FILE}.zip" -d "./${OUT_FILE}"
rm "${OUT_FILE}.zip"
