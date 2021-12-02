"""
Downloads the county boundaries from Open Street Map using the OSMNX python library.

NB: an attempt was done at using pyrosm, which would be significantly faster. However,
the boundaries returned are broken due to a bug in pyrosm
"""
from glob import glob
from typing import List, Literal

import geopandas as gpd
import osmnx as ox
import pandas as pd

COUNTRY = "Great Britain"
OSM_ID_COL = "osmid"

PROPERTIES_TO_RETAIN = ["display_name", "geometry"]

HomeNations = Literal["England", "Scotland", "Wales", "Northern Ireland"]


def get_county_boundaries_from_csv_files(file_list: List[str]) -> gpd.GeoDataFrame:
    """
    Given a list of files containing the OSM IDs for the UK counties (dovided by home country)
    build a GeoDataFrame containing all the boundaries
    :param file_list: a list of CSV files (e.g. one per home country)
    :return: GeoDataFrame with boundaries for each county
    """
    counties_df = pd.concat((pd.read_csv(file) for file in file_list), ignore_index=True)
    counties_df = counties_df.drop_duplicates(subset=[OSM_ID_COL])
    county_osm_ids = counties_df[OSM_ID_COL].tolist()
    gdf: gpd.GeoDataFrame = ox.geocode_to_gdf(county_osm_ids, by_osmid=True)
    gdf = gdf[PROPERTIES_TO_RETAIN]
    return gdf


def get_administrative_counties_from_osm(country: HomeNations) -> gpd.GeoDataFrame:
    """
    Retrieve all the administrative counties from one of the four UK Countries
    By "administrative counties" we mean here metropolitan and non-metropolitan counties
    with a county council and unitary authorities whereby a county does not have a county council
    (e.g. Berkshire). All these "counties" are tagged as "admin_level" 6 in OSM.
    NB: this function is not used in the workflow but it has been used offline to
        generate the CSV files for the administrative counties.
        It could be used to generate the boundaries of the administrative counties directly.
        However, we have opted not to do so for now because:
            - this function is considerably slower
            - it is still a bit error-prone due to curation errors on OSM (e.g. some administrative boundaries
              are marked as ceremonial) so one has to manually check the CSV files against the resulting map
            - the manually curated counties lists are unlikely to change frequently
        This function cannot generate the CSV files for ceremonial counties.
    :param country: one of the four UK Countries
    :return: a GeoDataFrame containing all the unitary authorities within the specified country of the UK
    """
    # Within the UK, counties and unitary authorities correspond to administrative level 6.
    # See https://wiki.openstreetmap.org/wiki/Tag:boundary%3Dadministrative#10_admin_level_values_for_specific_countries
    admin_level_6_geometries_df = ox.geometries_from_place(country, {"admin_level": "6"})
    # We are only interested in the "relation" rows, which are the ones that define boundaries
    county_boundaries_df = admin_level_6_geometries_df.loc["relation"].copy()
    county_boundaries_df = county_boundaries_df.reset_index()
    county_boundaries_df[OSM_ID_COL] = county_boundaries_df[OSM_ID_COL].astype(str)
    # Retain only administrative boundaries (there are some spurious historic and traditional boundaries)
    # NB: you must retain ceremonial counties otherwise Merseyside and Tyne and Wear are missing (perplexing)
    county_boundaries_df = county_boundaries_df[
        county_boundaries_df["boundary"] == "administrative" or county_boundaries_df["boundary"] == "ceremonial"
    ]
    # As the osm id is only unique within a feature type whe need prepend the type identifier
    # (in this case R for relationship) to guarantee uniqueness.
    # This composite ID will be useful for future searches in the Nominatim database (e.g. using osmnx.geocode_to_gdf())
    county_boundaries_df[OSM_ID_COL] = "R" + county_boundaries_df[OSM_ID_COL]
    county_boundaries_df = county_boundaries_df.sort_values(by="name")
    return county_boundaries_df


def main() -> None:
    admin_file_list = sorted(glob("static-src/administrative-counties-*.csv"))
    ceremonial_file_list = sorted(glob("static-src/ceremonial-counties-*.csv"))
    administrative_counties_df = get_county_boundaries_from_csv_files(admin_file_list)
    ceremonial_counties_df = get_county_boundaries_from_csv_files(ceremonial_file_list)
    ceremonial_counties_df.to_file("ceremonial-county-boundaries.geojson", driver="GeoJSON")
    administrative_counties_df.to_file("administrative-county-boundaries.geojson", driver="GeoJSON")


if __name__ == "__main__":
    main()
