import geopandas as gpd
import pandas as pd

EV_REGISTRATION_FILE = "veh0134.ods"
OUTPUT_FILE = "ev-registrations.geojson"

# Postcode district boundary details
POSTCODE_DISTRICTS_FILE = "../boundaries-postcode-district/uk-postcode-districts.geojson"
POSTCODE_DISTRICT_KEY = "Name"

# There are separate sheets for EV and hybrids. This sheet has registration data for both
SHEET = "VEH0134a"

# The sheet has a number of info rows at the top and bottom.
# Note: It is possible that the number of header rows could change in the future
ROWS_TO_SKIP = 6
LAST_POSTCODE = "ZE2"


def create_ev_registration_data() -> None:
    ev_df = pd.read_excel(EV_REGISTRATION_FILE, sheet_name=SHEET, skiprows=ROWS_TO_SKIP, engine="odf")

    # Get the index of the row with the last postcode so we can skip the footer
    index = ev_df.index[ev_df["Postcode District 2"] == LAST_POSTCODE][0]

    # File contains historical data by quarter. We take only the first two columns which are the postcode district
    #  and the count for the most recent quarter
    ev_df = ev_df.iloc[: index + 1, 0:2]

    # rename the columns
    column_name_map = {
        ev_df.columns[0]: POSTCODE_DISTRICT_KEY,
        ev_df.columns[1]: "count",
    }
    ev_df = ev_df.rename(columns=column_name_map)

    # add in the boundary polygons for the postcode
    postcodes_df = gpd.read_file(POSTCODE_DISTRICTS_FILE)
    result = postcodes_df.merge(ev_df, how="left", on=POSTCODE_DISTRICT_KEY)
    result = result.fillna(0)
    result.to_file(OUTPUT_FILE, driver="GeoJSON")


if __name__ == "__main__":
    create_ev_registration_data()
