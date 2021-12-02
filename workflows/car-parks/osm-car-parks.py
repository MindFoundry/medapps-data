from typing import Literal, Union

import geopandas as gpd
import osmnx as ox
import pandas as pd

HomeNation = Literal["England", "Scotland", "Wales"]
PROPERTIES_TO_RETAIN = ["parking", "fee", "capacity", "park_ride", "supervised", "maxstay", "opening_hours", "geometry"]


def get_car_parks_from_area(area: Union[HomeNation, str]) -> gpd.GeoDataFrame:
    """
    Retrieve all the car parks in the area
    :param area: a country or another region/place. Must be a name recognized by the Nominatim database
    :return: A GeoDataFrame containing all the car parks found in the are
    """
    parking_gdf = ox.geometries_from_place(area, {"amenity": "parking"})
    parking_gdf = parking_gdf.reset_index()
    parking_gdf = parking_gdf[PROPERTIES_TO_RETAIN]
    return parking_gdf


def main():
    """Get car parks for the whole of Great Britain"""
    en_gdf = get_car_parks_from_area("England")
    sco_gdf = get_car_parks_from_area("Scotland")
    wal_gdf = get_car_parks_from_area("Wales")
    gb_gdf = gpd.GeoDataFrame(pd.concat([en_gdf, sco_gdf, wal_gdf], ignore_index=True), crs=en_gdf.crs)
    gb_gdf.to_file("car-parks.geojson", driver="GeoJSON")


if __name__ == "__main__":
    main()
