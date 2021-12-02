import geopandas as gpd
import osmnx as ox
import pandas as pd

PROPERTIES_TO_RETAIN = ["isStation", "geometry"]


def get_bus_stops_and_stations_from_area(area: str) -> gpd.GeoDataFrame:
    """
    Retrieve all the bus stops and bus station in the area
    according to these three tags:
        - amenity=bus_station (https://wiki.openstreetmap.org/wiki/Tag:amenity%3Dbus_station)
        - highway=bus_stop (https://wiki.openstreetmap.org/wiki/Tag:highway%3Dbus_stop)
    There is one more tag who includes train and tram stations so we don't use it for now:
        - public_transport=station (https://wiki.openstreetmap.org/wiki/Tag:public_transport%3Dstation)
    :param area:
    :return: GeoDataFrame with all bus stops and stations, one stop per row.
    """
    tags = {
        "amenity": "bus_station",
        "highway": "bus_stop",
    }
    stops_and_stations_gdf = ox.geometries_from_place(area, tags)
    stops_and_stations_gdf = stops_and_stations_gdf.reset_index()
    stops_and_stations_gdf["isStation"] = stops_and_stations_gdf["amenity"] == "bus_station"
    stops_and_stations_gdf = stops_and_stations_gdf[PROPERTIES_TO_RETAIN]
    return stops_and_stations_gdf


def main():
    """Get bus stops and bus stations for the whole of Great Britain"""
    en_gdf = get_bus_stops_and_stations_from_area("England")
    sco_gdf = get_bus_stops_and_stations_from_area("Scotland")
    wal_gdf = get_bus_stops_and_stations_from_area("Wales")
    gb_gdf = gpd.GeoDataFrame(pd.concat([en_gdf, sco_gdf, wal_gdf], ignore_index=True), crs=en_gdf.crs)
    gb_gdf.to_file("bus-stops-and-stations.geojson", driver="GeoJSON")


if __name__ == "__main__":
    main()
