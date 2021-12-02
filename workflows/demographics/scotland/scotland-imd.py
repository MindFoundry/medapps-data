import geopandas as gpd
import pandas as pd

SCOTLAND_IMD_SHAPEFILE = "scotland-imd/SG_SIMD_2020.shp"
OUTPUT_GEOJSON = "scotland-imd.geojson"


def main() -> None:
    gdf = gpd.read_file(SCOTLAND_IMD_SHAPEFILE, crs="EPSG:4326")

    # The Scottish IMD data only contains ranks of areas not deciles
    gdf = gdf.rename(columns={"Decilev2": "OverallDecile"})
    gdf["IncomeDecile"] = pd.qcut(gdf["IncRankv2"], 10, labels=False) + 1
    gdf["EducationDecile"] = pd.qcut(gdf["EduRank"], 10, labels=False) + 1
    gdf["CrimeDecile"] = pd.qcut(gdf["CrimeRank"], 10, labels=False) + 1
    gdf["HealthDecile"] = pd.qcut(gdf["HlthRank"], 10, labels=False) + 1

    gdf = gdf[
        [
            "OverallDecile",
            "IncomeDecile",
            "EducationDecile",
            "CrimeDecile",
            "HealthDecile",
            "geometry",
        ]
    ]

    gdf = gdf.to_crs(crs="EPSG:4326")
    gdf.to_file(OUTPUT_GEOJSON, driver="GeoJSON")


if __name__ == "__main__":
    main()
