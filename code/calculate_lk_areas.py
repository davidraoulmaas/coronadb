#!/usr/bin/env python3
"""
Script to extract area of the 'Landkreise' and respective Centroids.
As projection, EPSG:5243 (ETRS89) is used.
Additionally, the projected coordinates are calculated (x_epsg5243, y_epsg5243)

Note that GDAL/OGR is required aside from the python libraries.
(https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html)
"""
import wget
import pandas as pd
from pathlib import Path
import geojson
from shapely.geometry import shape
from shapely.ops import transform
from functools import partial
import pyproj
from tqdm import tqdm
import os


def main():
    with open(lk_geojson_p) as f:
        lk = geojson.load(f)
    features = lk['features']

    dict_list = []
    for feature in tqdm(features):
        prop, geom = feature["properties"], feature["geometry"]

        poly = shape(geom)
        lon, lat = poly.centroid.coords[0]

        # project to EPSG:5243 (ETRS89) for correct area calculation
        proj = partial(pyproj.transform, pyproj.Proj(init='epsg:4326'),
                       pyproj.Proj(init='epsg:5243'))
        poly_projected = transform(proj, poly)
        x_epsg5243, y_epsg5243 = poly_projected.centroid.coords[0]
        projected_area = poly_projected.area
        try:
            dict_list.append(
                {"name": prop["name_2"],
                 "hasc_2": prop["hasc_2"],
                 "krs": prop["cca_2"],
                 "bundesland": prop["name_1"],
                 "centr_lon": lon,
                 "centr_lat": lat,
                 "x_epsg5243": x_epsg5243,
                 "y_epsg5243": y_epsg5243,
                 "total_area_epsg5243": projected_area
                 }
            )
        except KeyError:
            print(f"Incomplete Row was skipped: \n{prop}")
            continue

    df_lks = pd.DataFrame(dict_list).set_index("krs").sort_index().reset_index()

    # Fix error in lk data set for Göttingen. ID should be 03159
    idx = df_lks["krs"] == "03152"
    df_lks.loc[idx, "krs"] = "03159"
    df_lks.to_csv(proj_dir / "data/02_pre_processed/landkreis_areas.csv", encoding='utf-8')


if __name__ == '__main__':
    proj_dir = Path(__file__).absolute().parent.parent

    URL_LANDKREISE_OPENDATA = "https://public.opendatasoft.com/explore/dataset/landkreise-in-germany/download/?format=geojson&timezone=Europe/Berlin&lang=en"
    lk_geojson_p = proj_dir / 'data/01_raw_data/landkreise-in-germany.geojson'

    if not os.path.exists(lk_geojson_p):
        wget.download(URL_LANDKREISE_OPENDATA, out=str(lk_geojson_p))

    main()
