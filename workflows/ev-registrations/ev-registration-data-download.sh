#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Downloads registration data for low emissions vehicles, broken down by postcode district
# See: https://www.gov.uk/government/statistical-data-sets/all-vehicles-veh01#licensed-vehicles

curl -SL -X "GET" "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1021019/veh0134.ods" -o veh0134.ods
