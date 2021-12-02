#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

UKPN_GRID_AND_PRIMARY_SITES_CSV_URL="https://ukpowernetworks.opendatasoft.com/explore/dataset/grid-and-primary-sites/download/?format=csv&timezone=GMT&lang=en&use_labels_for_header=true&csv_separator=%2C"
UKPN_NETWORK_HEADROOM_CSV_URL="https://ukpowernetworks.opendatasoft.com/explore/dataset/network-headroom-report/download/?format=csv&timezone=Europe/London&lang=en&use_labels_for_header=true&csv_separator=%2C"

UKPN_GRID_AND_PRIMARY_SITES_CSV_FILE="grid-and-primary-sites.csv"
UKPN_NETWORK_HEADROOM_CSV_FILE="network-headroom.csv"


curl -SL -X "GET" "$UKPN_GRID_AND_PRIMARY_SITES_CSV_URL" -o $UKPN_GRID_AND_PRIMARY_SITES_CSV_FILE
curl -SL -X "GET" "$UKPN_NETWORK_HEADROOM_CSV_URL" -o $UKPN_NETWORK_HEADROOM_CSV_FILE

