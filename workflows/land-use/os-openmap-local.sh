#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Downloads The OS OpenMap Local data set for the entirety of the UK in GML format.
# For details of the data see: https://www.ordnancesurvey.co.uk/business-government/products/open-map-local
# For details of the API see: https://osdatahub.os.uk/docs/downloads/technicalSpecification

# From the licensing for the data:
# Our open data products are covered by the Open Government Licence (OGL), which allows you
#   - copy, distribute and transmit the data;
#   - adapt the data; and
#   - exploit the data commercially, whether by sub-licensing it, combining it with other data, or including it in your own product or application.
#
# We simply ask that you acknowledge the copyright and the source of the data by including the following attribution statement:
#
#   - Contains OS data © Crown copyright and database right 2021
#   - Where you use Code-Point Open data, you must also use the following attribution statements:
#   - Contains Royal Mail data © Royal Mail copyright and Database right 2021
#   - Contains National Statistics data © Crown copyright and database right 2021

# AREA="SP"  # Oxford only
AREA="GB"  # whole UK

curl -SL -X "GET" \
  "https://api.os.uk/downloads/v1/products/OpenMapLocal/downloads?area=${AREA}&format=GML&redirect=true" \
  -H "accept: application/json" \
  -o os-openmap-local.zip
