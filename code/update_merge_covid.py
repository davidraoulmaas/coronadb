import wget
import pandas as pd
from pathlib import Path
import os
import numpy as np

proj_dir = Path(__file__).absolute().parent.parent

covid_p = proj_dir  / 'data/01_raw_data/RKI_COVID19.csv'
plz_p = proj_dir    / 'data/01_raw_data/zipcodes.de.csv'
bev_p = proj_dir    / 'data/01_raw_data/bev.csv'
kh_p = proj_dir     / 'data/01_raw_data/krankenh.csv'
pflegebed_p = proj_dir / 'data/01_raw_data/pflegebed.csv'
hochschulen_p = proj_dir / 'data/01_raw_data/numhochschulen_per_plz.csv'


target_p = proj_dir / "data/03_integrated_data/covid_merged.csv"

url_covid = 'https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.csv?session=undefined'

if not os._exists(covid_p):
    wget.download(url_covid, out=str(covid_p))

df_covid = pd.read_csv(covid_p, dtype={"IdLandkreis": 'str'})
df_covid = df_covid[df_covid["IdLandkreis"] != '0-1']

df_plz = pd.read_csv(plz_p).drop(["place", "state", "state_code", "country_code", "province", "province_code",
                                  "latitude", "longitude"], axis=1)

df_covid_knownpos = df_covid[~df_covid["IdLandkreis"].isna()].copy()
df_covid_knownpos["krs"] = df_covid_knownpos["IdLandkreis"].astype("int")
df_covid_knownpos.drop("IdLandkreis", axis=1, inplace=True)
df_covid_knownpos.set_index("krs", inplace=True)

df_bev = pd.read_csv(bev_p, encoding='ISO-8859-1', dtype={"krs": 'int'}).set_index("krs").drop("name", axis=1)
df_kh = pd.read_csv(kh_p, encoding='ISO-8859-1', dtype={"krs": 'int'}).set_index("krs").drop("name", axis=1)
df_pflegebed = pd.read_csv(pflegebed_p, encoding='ISO-8859-1', dtype={"krs": 'int'}).set_index("krs").drop("name",
                                                                                                           axis=1)

df_hs_byplz = pd.read_csv(hochschulen_p)

df_full = df_covid_knownpos.join(df_bev.add_prefix("bev_"), on='krs')
df_full = df_full.join(df_kh.add_prefix("kh_"), on='krs')
df_full = df_full.join(df_pflegebed.add_prefix("pflegebed_"), on='krs')

df_full.to_csv(target_p)
