import geopandas as gpd
import pandas as pd

NCR_DATA_CSV = "ncr-data.csv"
CHARGE_POINTS_GEOJSON = "charge-points.geojson"

ATTRIBUTES = [
    "chargeDeviceID",
    "name",
    "latitude",
    "longitude",
    "town",
    "county",
    "postcode",
    "chargeDeviceStatus",
    "locationType",
    "connector1RatedOutputKW",
]


def main() -> None:
    ncr_df: pd.DataFrame = pd.read_csv(NCR_DATA_CSV, lineterminator="\n", usecols=ATTRIBUTES)
    ncr_gdf = gpd.GeoDataFrame(
        ncr_df, geometry=gpd.points_from_xy(ncr_df["longitude"], ncr_df["latitude"], crs="EPSG:4326")
    )
    ncr_gdf.to_file(CHARGE_POINTS_GEOJSON, driver="GeoJSON")


if __name__ == "__main__":
    main()
