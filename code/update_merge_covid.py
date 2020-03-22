#!/usr/bin/env python3
"""
Script for merging covid data with other covariates.
TODO: add universities (Hochschulen)
"""
import wget
import pandas as pd
from pathlib import Path
import os
import argparse
import numpy as np
from tqdm import tqdm
import math


def preproc_covid_df():
    """
    Load & Preprocess covid19 case counts.
    :return: List of dataframes, and list of filenames where they should be saved after merging
    """
    df_covid = pd.read_csv(covid_p, dtype={"IdLandkreis": 'str'})

    # remove entries that don't have any location..
    df_covid = df_covid[df_covid["IdLandkreis"] != '0-1']
    df_covid = df_covid[~df_covid["IdLandkreis"].isna()]

    df_covid["Meldedatum"] = pd.to_datetime(pd.to_datetime(df_covid["Meldedatum"]).dt.date)

    # the krs data already truncated the ids to ints, so also do this for the covid data
    df_covid["krs"] = df_covid["IdLandkreis"].astype("int")
    df_covid.drop("IdLandkreis", axis=1, inplace=True)
    df_covid.set_index("krs", inplace=True)

    required_columns = ["krs", "Meldedatum"]

    # covid grouped by landkreis and age group
    df_covid_byage = df_covid.groupby(required_columns + ["Altersgruppe"])[
        ["AnzahlFall", "AnzahlTodesfall"]].sum().reset_index()

    # covid grouped by landkreis and sex
    df_covid_bysex = df_covid.groupby(required_columns + ["Geschlecht"])[
        ["AnzahlFall", "AnzahlTodesfall"]].sum().reset_index()

    # covid grouped by landkreis, sex + age group
    df_covid_bysex_age = df_covid.groupby(required_columns + ["Altersgruppe", "Geschlecht"])[
        ["AnzahlFall", "AnzahlTodesfall"]].sum().reset_index()

    # covid grouped by landkreis only
    df_covid_bylk = df_covid.groupby(required_columns)[
        ["AnzahlFall", "AnzahlTodesfall"]].sum().reset_index()

    dfs = [df_covid_byage,
           df_covid_bysex,
           df_covid_bysex_age,
           df_covid_bylk]

    filenames = ["covid_merged_by_age.csv",
                 "covid_merged_by_sex.csv",
                 "covid_merged_by_sex_age.csv",
                 "covid_merged_by_lk.csv"]

    return dfs, filenames


def preproc_covariates():
    """
    Load & Preprocess Covariate data.
    :return: Dataframe consisting of all merged data, with 'krs' as index
    """
    # df_plz = pd.read_csv(plz_p).drop(["place", "state", "state_code", "country_code", "province", "province_code",
    #                                   "latitude", "longitude"], axis=1)
    df_bev = pd.read_csv(bev_p, dtype={"krs": 'int'}).set_index("krs").drop("name", axis=1)
    df_kh = pd.read_csv(kh_p,  dtype={"krs": 'int'}).set_index("krs").drop("name", axis=1)
    df_pflegebed = pd.read_csv(pflegebed_p,
                               dtype={"krs": 'int'}).set_index("krs").drop("name", axis=1)
    df_lk_area = pd.read_csv(lk_area_p).set_index("krs")  # .drop(["hasc_2", "bundesland", "name"], axis=1)

    df_intensiv_byplz = pd.read_csv(intensiv_p, dtype={"krs": 'int'}).set_index("krs").drop(
        "land", axis=1)
    # Pandas is weird, the reset_indx->set_idx is necessary for the join
    df_intensiv = df_intensiv_byplz.groupby(["krs"])["intensivkliniken"].sum().reset_index().set_index("krs")

    # NAs are where no clinics exist -> 0
    df_intensiv = df_intensiv.fillna(0)

    # TODO: Hochschulen..
    # df_hs_byplz = pd.read_csv(hochschulen_p)
    df_covs = df_bev.add_prefix("bev_")
    df_covs = df_covs.join(df_kh.add_prefix("kh_"), on='krs')
    df_covs = df_covs.join(df_pflegebed.add_prefix("pflegebed_"), on='krs')
    df_covs = df_covs.join(df_intensiv.add_prefix("intensiv_"), on='krs')
    df_covs = df_covs.join(df_lk_area.add_prefix("lk_"), on='krs')

    # all codes must consist of 5 numbers, longer ones are cities
    df_covs = df_covs[df_covs.index<1e6]

    return df_covs


def create_zeros_df(df_covs, df):
    """
    Create DF that contains values for all 'Landkreise'/districts and each timestep (day).
    That is, all the places where there are 0 cases are now also available, together with the covariates.
    In addition, the cumulative cases are counted.
    :param df_covs:
    :param df:
    :return:
    """
    first_day, last_day = df["Meldedatum"].min(), df["Meldedatum"].max()
    date_range = pd.date_range(first_day, last_day)

    # add zeros
    new_df_l = []
    for index, row in tqdm(df_covs.reset_index().iterrows()):
        for date in date_range:
            row_dict = dict(row)
            row_dict["Meldedatum"] = date

            new_df_l.append(row_dict)
    df_covs_alltimes = pd.DataFrame(new_df_l)
    df_withzeros = pd.merge(df, df_covs_alltimes, how='right', on=['krs', 'Meldedatum'])
    df_withzeros["AnzahlFall"].fillna(0, inplace=True)
    df_withzeros["AnzahlTodesfall"].fillna(0, inplace=True)

    # Now add cumulative counts of cases and deaths
    print("Calculating cumulative cases")
    df_withzeros["cum_AnzahlFall"] = 0
    df_withzeros["cum_AnzahlTodesfall"] = 0

    lks = df_withzeros["krs"].unique()
    dates = np.sort(df_withzeros["Meldedatum"].unique())

    for lk in tqdm(lks):
        count = 0.
        count_deaths = 0.
        for date in dates:
            idx_krs = df_withzeros["krs"] == lk
            idx_date = df_withzeros["Meldedatum"] == date
            row_idx = idx_krs & idx_date

            count += df_withzeros.loc[row_idx, "AnzahlFall"].iloc[0]
            count_deaths += df_withzeros.loc[row_idx, "AnzahlTodesfall"].iloc[0]

            df_withzeros.loc[row_idx, "cum_AnzahlFall"] = count
            df_withzeros.loc[row_idx, "cum_AnzahlTodesfall"] = count_deaths
    colnames = list(df_withzeros.columns)
    new_col_order = colnames[:4] + colnames[-2:] + colnames[4:-2]

    return df_withzeros[new_col_order].sort_values(["krs", "Meldedatum"])


def main():
    df_covs = preproc_covariates()
    dfs, filenames = preproc_covid_df()

    # merge the different covid dataframes with the covariates.
    for df, fn in zip(dfs, filenames):
        df_merged = df.join(df_covs, on=['krs'])
        df_merged.to_csv(target_p / fn, index=False, encoding='utf-8')
        print(f"Created file: '{target_p / fn}'")

    # create dataset that also contains the zeros (ie no cases) with corresponding covariates
    #  up till now only for the one without age groups.. Because it's kinda tedious
    print("Creating CSV with zeros")
    df_withzeros = create_zeros_df(df_covs, dfs[-1])
    df_withzeros.to_csv(target_p / "covid_merged_by_lk_withzeros_cumulative.csv", encoding='utf-8', index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--force-covid-download", action='store_true',
                        help="Download COVID Data again, even if it exists.")
    args = parser.parse_args()

    proj_dir = Path(__file__).absolute().parent.parent

    # Files with Landkreis key
    covid_p = proj_dir / 'data/01_raw_data/RKI_COVID19.csv'
    plz_p = proj_dir / 'data/01_raw_data/zipcodes.de.csv'
    bev_p = proj_dir / 'data/01_raw_data/bev.csv'
    kh_p = proj_dir / 'data/01_raw_data/krankenh.csv'
    pflegebed_p = proj_dir / 'data/01_raw_data/pflegebed.csv'
    intensiv_p = proj_dir / 'data/01_raw_data/intensiv.csv'
    lk_area_p = proj_dir / 'data/02_pre_processed/landkreis_areas.csv'

    # files with PLZ key
    hochschulen_p = proj_dir / 'data/01_raw_data/numhochschulen_per_plz.csv'

    target_p = proj_dir / "data/03_integrated_data/"

    URL_COVID = 'https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.csv?session=undefined'
    if not os.path.exists(covid_p) or args.force_covid_download:
        wget.download(URL_COVID, out=str(covid_p))

    main()
