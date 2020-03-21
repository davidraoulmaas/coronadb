import wget
import pandas as pd
from pathlib import Path
import os

proj_dir = Path(__file__).absolute().parent.parent

covid_p = proj_dir / 'data/01_raw_data/RKI_COVID19.csv'
plz_p = proj_dir / 'data/01_raw_data/zipcodes.de.csv'
bev_p = proj_dir / 'data/01_raw_data/bev.csv'
kh_p = proj_dir / 'data/01_raw_data/krankenh.csv'
pflegebed_p = proj_dir / 'data/01_raw_data/pflegebed.csv'
hochschulen_p = proj_dir / 'data/01_raw_data/numhochschulen_per_plz.csv'
intensiv_p = proj_dir / 'data/01_raw_data/intensiv.csv'

target_p = proj_dir / "data/03_integrated_data/covid_merged.csv"

url_covid = 'https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.csv?session=undefined'

if not os.path.exists(covid_p):
    wget.download(url_covid, out=str(covid_p))

df_covid = pd.read_csv(covid_p, dtype={"IdLandkreis": 'str'})

# remove entries that don't have any location..
df_covid = df_covid[df_covid["IdLandkreis"] != '0-1']
df_covid = df_covid[~df_covid["IdLandkreis"].isna()]

# the krs data already truncated the ids to ints, so also do this for the covid data
df_covid["krs"] = df_covid["IdLandkreis"].astype("int")
df_covid.drop("IdLandkreis", axis=1, inplace=True)
df_covid.set_index("krs", inplace=True)

# group by landkreis
df_covid = df_covid.groupby(["krs", "Bundesland", "Landkreis", "Altersgruppe"])[
    ["AnzahlFall", "AnzahlTodesfall"]].sum().reset_index()
df_plz = pd.read_csv(plz_p).drop(["place", "state", "state_code", "country_code", "province", "province_code",
                                  "latitude", "longitude"], axis=1)

df_bev = pd.read_csv(bev_p, encoding='ISO-8859-1', dtype={"krs": 'int'}).set_index("krs").drop("name", axis=1)
df_kh = pd.read_csv(kh_p, encoding='ISO-8859-1', dtype={"krs": 'int'}).set_index("krs").drop("name", axis=1)
df_pflegebed = pd.read_csv(pflegebed_p, encoding='ISO-8859-1', dtype={"krs": 'int'}).set_index("krs").drop("name",
                                                                                                           axis=1)
df_intensiv_byplz = pd.read_csv(intensiv_p, encoding='ISO-8859-1', dtype={"krs": 'int'}).set_index("krs").drop("land",
                                                                                                               axis=1)
# Pandas is weird, the reset_indx->set_idx is necessary for the join
df_intensiv = df_intensiv_byplz.groupby(["krs"])["intensivkliniken"].sum().reset_index().set_index("krs")

# TODO: Hochschulen..
# df_hs_byplz = pd.read_csv(hochschulen_p)

df_full = df_covid.join(df_bev.add_prefix("bev_"), on='krs')
df_full = df_full.join(df_kh.add_prefix("kh_"), on='krs')
df_full = df_full.join(df_pflegebed.add_prefix("pflegebed_"), on='krs')
df_full = df_full.join(df_intensiv.add_prefix("intensiv_"), on='krs')

df_full.to_csv(target_p)
