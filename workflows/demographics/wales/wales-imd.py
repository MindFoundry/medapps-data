import geopandas as gpd
import pandas as pd

LSOA_BOUNDARIES_FILE = "../../boundaries-lsoa/lsoa-boundaries.geojson"
WALES_IMD_FILE = "wales-imd/wales-imd-raw.csv"
OUTPUT_GEOJSON = "wales-imd.geojson"


def main() -> None:
    imd_df = pd.read_csv(WALES_IMD_FILE)

    # The Wales IMD data only contains ranks of areas not deciles
    # note: 1 is the most deprived decile
    imd_df["OverallDecile"] = pd.qcut(imd_df["Overall rank(2019)"], 10, labels=False) + 1
    imd_df["IncomeDecile"] = pd.qcut(imd_df["Income(2019)"], 10, labels=False) + 1
    imd_df["EducationDecile"] = pd.qcut(imd_df["Education(2019)"], 10, labels=False) + 1
    # note: Wales doesn't have a separate 'Crime' score; community safety takes into account crime and a few other factors
    imd_df["CrimeDecile"] = pd.qcut(imd_df["Community Safety(2019)"], 10, labels=False) + 1
    imd_df["HealthDecile"] = pd.qcut(imd_df["Health(2019)"], 10, labels=False) + 1

    imd_df = imd_df[
        [
            "Local Area (2011 LSOA)",
            "OverallDecile",
            "IncomeDecile",
            "EducationDecile",
            "CrimeDecile",
            "HealthDecile",
        ]
    ]

    lsoa_df = gpd.read_file(LSOA_BOUNDARIES_FILE, crs="EPSG:4326")
    lsoa_df = lsoa_df[["LSOA11CD", "geometry"]]

    gdf = lsoa_df.merge(imd_df, how="right", left_on="LSOA11CD", right_on="Local Area (2011 LSOA)")
    gdf = gdf.drop(columns=["Local Area (2011 LSOA)", "LSOA11CD"])

    gdf.to_file(OUTPUT_GEOJSON, driver="GeoJSON")


if __name__ == "__main__":
    main()
