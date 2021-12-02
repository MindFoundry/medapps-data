import os
from typing import Any

import chardet
import geopandas as gpd
import pandas as pd
import requests

WPD_SUBSTATION_DATASET_URL = "https://connecteddata.westernpower.co.uk/dataset/29d435c2-0cbe-442d-96fe-a229a0307fba/resource/619e5534-090d-4aa8-abcd-74d1dd1a31cf/download/distribution_substation_details.csv"
WPD_GRID_AND_PRIMARY_SUBSTATIONS_DATASET_URL = "resources/WPD-Network-Capacity-Map-19-11-2021.csv"

PROPERTIES_TO_RETAIN_SUBSTATION_DATASET = [
    "DNO",
    "PRIMARY SUBSTATION NAME",
    "PRIMARY SUBSTATION NUMBER",
    "HV FEEDER",
    "SUBSTATION TYPE",
    "SUBSTATION NAME",
    "SUBSTATION NUMBER",
    "GRID REFERENCE",
    "DAY_MAX_DEMAND",
    "NIGHT_MAX_DEMAND",
    "SUBSTATION_RATING",
    "LCT Count",
    "Energy Storage",
    "EV Charge Point",
    "Heat Pump",
    "Photovoltaic",
    "CUSTOMERS COUNT",
]


# retaining the attributes visualized on the WPD Network Capacity Map (https://www.westernpower.co.uk/our-network/network-capacity-map-application)
PROPERTIES_TO_RETAIN_NETWORK_CAPACITY_DATASET = [
    "Substation Name",
    "Downstream Voltage",
    "Demand Headroom (MVA)",
    "Total Generation (MVA)",
    "Generation Headroom (MVA)",  # aka 'Reverse Power Headroom'
    "Demand Headroom RAG",
    "Generation Headroom RAG",
]

DNO_WPD = "WPD"


def get_file_encoding_chardet(file_path: str) -> Any:
    """
    Get the encoding of a file using chardet package
    :param file_path:
    :return:
    """
    with open(file_path, "rb") as file:

        result = chardet.detect(file.read())
        return result["encoding"]


def download_data(file_name: str) -> None:
    """
    Download the CSV dataset. This could be optimised as a streamed download.
    Pandas complains if the file is downloaded using curl or similar commands so this approach was followed
    :param file_name: the name of the downloaded CSV file
    """
    res = requests.get(WPD_SUBSTATION_DATASET_URL)
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(res.text)


def generate_primary_substation_data() -> None:
    """
    Generate a GeoJSON file containing the WPD network capacity data
    """
    ps_df: pd.DataFrame = pd.read_csv(WPD_GRID_AND_PRIMARY_SUBSTATIONS_DATASET_URL)
    # We are only interested in Primary Substations (filter out Grid/Bulk Substations)
    ps_df = ps_df[ps_df["Asset Type"] == "Primary"]
    ps_df = ps_df.drop(columns=["Asset Type"])
    # sum the three generation fields to get total generation (we need to verify this is correct)
    ps_df["Total Generation (MVA)"] = (
        ps_df["Generation Connected (kVA)"]
        + ps_df["Generation Offered Not Accepted (kVA)"]
        + ps_df["Generation Accepted Not Connected (kVA)"]
    ) / 1000
    geometry = gpd.points_from_xy(ps_df["Longitude"], ps_df["Latitude"])
    ps_gdf = gpd.GeoDataFrame(ps_df[PROPERTIES_TO_RETAIN_NETWORK_CAPACITY_DATASET], geometry=geometry, crs="EPSG:4326")
    ps_gdf = ps_gdf.rename(
        columns={
            "Substation Name": "Site Name",
            "Downstream Voltage": "Downstream Voltage",
            # NB: we are assuming here that 1 VA = 1W which is true for DC only
            "Total Generation (MVA)": "Total Generation (MW)",
            "Headroom": "Demand Headroom (MVA)",
        }
    )
    ps_df["DNO"] = DNO_WPD
    ps_gdf.to_file("wpd-primary-substations.geojson", driver="GeoJSON")


def generate_all_substation_data():
    """
    Generate a GeoJSON file containing the substation data for the WPD network
    """
    file_name = WPD_SUBSTATION_DATASET_URL.rsplit("/", maxsplit=1)[-1]
    if not os.path.isfile(file_name):
        download_data(file_name)
    encoding = get_file_encoding_chardet(file_name)
    with pd.read_csv(file_name, encoding=encoding, chunksize=10 ** 4) as reader:
        for index, chunk in enumerate(reader):
            geometry = gpd.points_from_xy(chunk["LONGITUDE"], chunk["LATITUDE"])
            geo_df = gpd.GeoDataFrame(
                chunk[PROPERTIES_TO_RETAIN_SUBSTATION_DATASET], geometry=geometry, crs="EPSG:4326"
            )
            if index == 0:
                # have to do this because GeoDataFrame.to_file does not seem to
                # create the file if mode is "a" (i.e. "append")
                geo_df.to_file("wpd-substation-data.geojson", driver="GeoJSON")
            else:
                geo_df.to_file("wpd-substation-data.geojson", driver="GeoJSON", mode="a")


def main():
    generate_all_substation_data()
    generate_primary_substation_data()


if __name__ == "__main__":
    main()
