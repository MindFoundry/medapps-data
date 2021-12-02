#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Downloads the National Chargepoint registry data from the uk gov site.
# See: https://www.gov.uk/guidance/find-and-use-data-on-public-electric-vehicle-chargepoints

curl -SL -X "GET" "http://chargepoints.dft.gov.uk/api/retrieve/registry/format/csv" -o ncr-data.csv
