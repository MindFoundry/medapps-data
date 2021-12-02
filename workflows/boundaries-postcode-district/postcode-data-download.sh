#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Downloads file with boundary polygons (e.g., BB3, BB4) for postcode districts for the whole UK
# See: https://www.doogal.co.uk/PostcodeDownloads.php

curl -SL -X "GET" "https://www.doogal.co.uk/kml/PostcodeDistricts.kml" -o PostcodeDistricts.kml
