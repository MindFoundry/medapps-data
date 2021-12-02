"""
Extracts roads from OS map data.
"""
import zipfile
from typing import Optional

import fiona
import geopandas as gpd
from tqdm import tqdm

OPEN_MAP_DATA = "os-openmap-local.zip"
ROAD_LAYER_NAME = "Road"
COLUMNS_TO_KEEP = ["distinctiveName", "roadNumber", "classification", "geometry"]


def _extract_roads_single(file_path: str) -> Optional[gpd.GeoDataFrame]:
    if ROAD_LAYER_NAME not in fiona.listlayers(file_path):
        tqdm.write(f"File {file_path} does not contain a roads layer")
        return None

    roads = gpd.read_file(file_path, layer=ROAD_LAYER_NAME)

    if len(roads) == 0:
        tqdm.write(f"File {file_path} has no roads")
        return None

    tqdm.write(f"Loaded {len(roads)} roads from {file_path}")

    return roads


def main():
    with zipfile.ZipFile(OPEN_MAP_DATA) as zip_file:
        file_paths = [f"zip://{OPEN_MAP_DATA}!{f}" for f in zip_file.namelist() if f.endswith(".gml")]

    tqdm.write(f"{len(file_paths)} files to process")

    roads_map = map(_extract_roads_single, file_paths)

    index_set: set = set()

    for idx, roads_gdf in enumerate(tqdm(roads_map)):
        tqdm.write(f"Processing item {idx}")
        if roads_gdf is None:
            continue
        assert isinstance(roads_gdf, gpd.GeoDataFrame)
        if "distinctiveName" not in roads_gdf:
            roads_gdf["distinctiveName"] = None
        if "roadNumber" not in roads_gdf:
            roads_gdf["roadNumber"] = None
        roads_gdf = roads_gdf[[*COLUMNS_TO_KEEP, "gml_id"]]
        already_present_mask = roads_gdf["gml_id"].isin(index_set)
        roads_gdf = roads_gdf[~already_present_mask]
        index_set.update(roads_gdf["gml_id"].tolist())
        roads_gdf = roads_gdf.drop(columns=["gml_id"])
        if idx == 0:
            roads_gdf.to_file("roads.gpkg", driver="GPKG")
        else:
            roads_gdf.to_file("roads.gpkg", driver="GPKG", mode="a")


if __name__ == "__main__":
    main()
