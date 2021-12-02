"""
Extracts buildings from OS map data.
"""
import zipfile
from typing import Optional

import fiona
import geopandas as gpd
from tqdm import tqdm

OPEN_MAP_DATA = "os-openmap-local.zip"
BUILDING_LAYER_NAME = "Building"
COLUMNS_TO_KEEP = ["geometry"]


def _extract_roads_single(file_path: str) -> Optional[gpd.GeoDataFrame]:
    if BUILDING_LAYER_NAME not in fiona.listlayers(file_path):
        tqdm.write(f"File {file_path} does not contain a buildings layer")
        return None

    buildings = gpd.read_file(file_path, layer=BUILDING_LAYER_NAME)

    if len(buildings) == 0:
        tqdm.write(f"File {file_path} has no buildings")
        return None

    tqdm.write(f"Loaded {len(buildings)} buildings from {file_path}")

    return buildings


def main():
    with zipfile.ZipFile(OPEN_MAP_DATA) as zip_file:
        file_paths = [f"zip://{OPEN_MAP_DATA}!{f}" for f in zip_file.namelist() if f.endswith(".gml")]

    tqdm.write(f"{len(file_paths)} files to process")

    buildings_map = map(_extract_roads_single, file_paths)

    index_set: set = set()

    for idx, buildings_gdf in enumerate(tqdm(buildings_map)):
        tqdm.write(f"Processing item {idx}")
        if buildings_gdf is None:
            continue
        assert isinstance(buildings_gdf, gpd.GeoDataFrame)
        buildings_gdf = buildings_gdf[[*COLUMNS_TO_KEEP, "gml_id"]]
        already_present_mask = buildings_gdf["gml_id"].isin(index_set)
        buildings_gdf = buildings_gdf[~already_present_mask]
        index_set.update(buildings_gdf["gml_id"].tolist())
        buildings_gdf = buildings_gdf.drop(columns=["gml_id"])
        if idx == 0:
            buildings_gdf.to_file("buildings.gpkg", driver="GPKG")
        else:
            buildings_gdf.to_file("buildings.gpkg", driver="GPKG", mode="a")


if __name__ == "__main__":
    main()
