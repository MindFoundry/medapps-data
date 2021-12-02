#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Downloads The English Indices of Deprivation 2019 data set in shapefile format.
# For details of the data see: https://data-communities.opendata.arcgis.com/datasets/indices-of-multiple-deprivation-imd-2019/about

# Licensing: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

# You are free to:
#  - copy, publish, distribute and transmit the Information;
#  - adapt the Information;
#  - exploit the Information commercially and non-commercially for example, by combining it with other Information, or by including it in your own product or application.
#
# You must (where you do any of the above):
#  - acknowledge the source of the Information in your product or application by including or linking to any attribution statement specified by the Information Provider(s) and, where possible, provide a link to this licence;
#
# If the Information Provider does not provide a specific attribution statement, you must use the following:
# Contains public sector information licensed under the Open Government Licence v3.0.

IMD_DOWNLOAD_URL="https://www.arcgis.com/sharing/rest/content/items/5e1c399d787e48c0902e5fe4fc1ccfe3/data"
OUT_FILE="england-imd"

curl -SL -X "GET" $IMD_DOWNLOAD_URL -o "${OUT_FILE}.zip"
unzip "${OUT_FILE}.zip" -d "./${OUT_FILE}"
rm "${OUT_FILE}.zip"
