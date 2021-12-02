from glob import glob

import geopandas as gpd
import pandas as pd

PRIMARY_SUBSTATIONS_GEOJSON_FILES_PATTERN = "../dno-*/*-primary-substations.geojson"


def merge_primary_substation_data() -> None:
    """
    Merge all the DNOs Primary Substation data into one GeoDataFrame to be saved to GeoJSON
    The columns of the GeoDataFrame are:
    - "DNO": string representing the name of the DNO
    - "Site Name": string, name of the primary substation
    - "Downstream Voltage": the voltage outputed by the substation (132, 66, 33, 11, etc..)
    - "Total Generation (MW)": number, the total generation produced by the substation
        For WPD this was computed as the sum of three generation fields, see the python script for WPD
    - "Demand Headroom (MVA)": number,
    - "Generation Headroom (MVA)": number, only for WPD
    - "Demand Headroom RAG": string, one of Red, Green, Amber. Color-code for the demand headroom. Only available for WPD
    - "Generation Headroom RAG": string, one of Red, Green, Amber. Color-code for the demand headroom. Only available for WPD
    """
    files_to_merge = glob(PRIMARY_SUBSTATIONS_GEOJSON_FILES_PATTERN)
    print(files_to_merge)
    gdf: gpd.GeoDataFrame = gpd.GeoDataFrame(
        pd.concat((gpd.read_file(file) for file in files_to_merge), ignore_index=True), crs="EPSG:4326"
    )
    gdf.to_file("dnos-primary-substations.geojson", driver="GeoJSON")


if __name__ == "__main__":
    merge_primary_substation_data()
