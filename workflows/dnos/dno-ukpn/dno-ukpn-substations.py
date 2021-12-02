import sys

import geopandas as gpd
import pandas as pd

SITE_ID = "SiteFunctionalLocation"

PROPERTIES_TO_RETAIN_GRID_AND_PRIMARY = [
    "SiteName",
    SITE_ID,
    "SiteVoltage",
    "Total_Generation",
]

PROPERTIES_TO_RETAIN_HEADROOM = [SITE_ID, "Headroom"]

CURRENT_YEAR = 2021

DNO_UKPN = "UKPN"


def main():
    grid_and_primary_sites_file_name = sys.argv[1]
    headroom_capacity_file_name = sys.argv[2]
    grid_and_primary_sites_df: pd.DataFrame = pd.read_csv(grid_and_primary_sites_file_name)
    headroom_capacity_df: pd.DataFrame = pd.read_csv(headroom_capacity_file_name)
    # fetch the headroom capacity for the current year (e.g. 2021) or the closest year available preceding the current
    curr_headroom_capacity_df = headroom_capacity_df[
        (headroom_capacity_df["Year"] == CURRENT_YEAR) & (headroom_capacity_df["Scenario"] == "Planning Scenario")
    ]
    idx_mask = curr_headroom_capacity_df.groupby(SITE_ID)["Year"].transform(max) == curr_headroom_capacity_df["Year"]
    curr_headroom_capacity_df = curr_headroom_capacity_df[idx_mask]
    curr_headroom_capacity_df = curr_headroom_capacity_df[PROPERTIES_TO_RETAIN_HEADROOM].set_index(SITE_ID)
    grid_and_primary_sites_df = grid_and_primary_sites_df.set_index(SITE_ID)
    ps_df: pd.DataFrame = grid_and_primary_sites_df.merge(
        curr_headroom_capacity_df, how="left", left_index=True, right_index=True
    )
    # We are only interested in Primary Substations (filter out Grid Substations)
    ps_df = ps_df.reset_index()
    # We are only interested in Primary Substations (filter out Grid Substations)
    ps_df = ps_df[ps_df["SiteType"] == "Primary Substation"]
    # remove siteType column drop rows where geospatial information is missing (4 rows)
    ps_df = ps_df.drop(columns=["SiteType"]).dropna(subset=["Longitude", "Latitude"])
    geometry = gpd.points_from_xy(ps_df["Longitude"], ps_df["Latitude"])
    # drop duplicates in columns to retain
    columns_to_retain = list(set(PROPERTIES_TO_RETAIN_GRID_AND_PRIMARY + PROPERTIES_TO_RETAIN_HEADROOM))
    # 4) build GeoDataFrame
    ps_gdf = gpd.GeoDataFrame(
        ps_df.loc[:, columns_to_retain],
        geometry=geometry,
        crs="EPSG:4326",
    )
    # rename columns to align names
    ps_gdf = ps_gdf.rename(
        columns={
            "SiteName": "Site Name",
            "SiteVoltage": "Downstream Voltage",
            "Total_Generation": "Total Generation (MW)",
            "Headroom": "Demand Headroom (MVA)",
        }
    )
    # add a column with DNO name (useful after merging all DNO datasets)
    ps_gdf["DNO"] = DNO_UKPN
    # save to GeoJSON
    ps_gdf.to_file("ukpn-primary-substations.geojson", driver="GeoJSON")


if __name__ == "__main__":
    main()
