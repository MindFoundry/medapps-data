import geopandas as gpd

ENGLAND_IMD_SHAPEFILE = "england-imd/IMD_2019.shp"
OUTPUT_GEOJSON = "england-imd.geojson"


def main() -> None:
    gdf = gpd.read_file(ENGLAND_IMD_SHAPEFILE)

    gdf = gdf.rename(
        columns={
            "IMD_Decile": "OverallDecile",
            "IncDec": "IncomeDecile",
            "EduDec": "EducationDecile",
            "CriDec": "CrimeDecile",
            "HDDDec": "HealthDecile",
        }
    )

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
