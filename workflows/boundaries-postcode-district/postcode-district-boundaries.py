import fiona
import geopandas as gpd
import shapely

# enable the KML driver
gpd.io.file.fiona.drvsupport.supported_drivers["KML"] = "rw"

POSTCODE_DISTRICT_KML_FILE = "PostcodeDistricts.kml"
OUT_FILE = "uk-postcode-districts.geojson"

ATTRIBUTES_TO_KEEP = [
    "Name",
    "geometry",
]


def read_kml_file(filepath: str) -> gpd.GeoDataFrame:
    """Data in the kml file is divided into multiple regions (AB, Al, BB, etc). Have to read each layer to
    get all the data.
    """
    gdf = gpd.GeoDataFrame()

    for layer in fiona.listlayers(filepath):
        layer_df = gpd.read_file(filepath, driver="KML", layer=layer)
        gdf = gdf.append(layer_df, ignore_index=True)

    return gdf


def drop_z_coordinate(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """The kml file contains a Z coordinate (value=0) for all points, do drop this."""
    return gdf.set_geometry(
        gdf.geometry.map(lambda polygon: shapely.ops.transform(lambda x, y, _: (x, y), polygon)), crs="EPSG:4326"
    )


def drop_northern_ireland(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """All postcodes in Northern Ireland start with BT"""
    return gdf.drop(gdf.loc[gdf["Name"].str.startswith("BT")].index)


def convert_kml_file_to_geojson() -> None:
    gdf = read_kml_file(POSTCODE_DISTRICT_KML_FILE)
    gdf = drop_z_coordinate(gdf)
    gdf = drop_northern_ireland(gdf)
    gdf = gdf[ATTRIBUTES_TO_KEEP]
    gdf.to_file(OUT_FILE, driver="GeoJSON")


if __name__ == "__main__":
    convert_kml_file_to_geojson()
