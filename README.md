# coronadb

### About
The repository provides up-to-date COVID-19 Data **within Germany** on the resolution of Districts ('Landkreise').
This includes information such as the number of hospital, census data and others (for more info, see below). In addition,  centroid coordinates (lon, lat) of the districts, their total area, and projected ([epsg:5243](https://epsg.io/5243)) coordinates are provided.

The COVID-19 case data will be updated daily.

This is still a **work in progress**. We plan to add a few more relevant data sets in the future.

### Merged Data
The final CSVs are available via [Google Drive](https://drive.google.com/drive/folders/1Vsf20J75hAJ6EmgM6yRjsRpyLKqvZhmJ?usp=sharing).

All CSVs include COVID-19 data merged with the different covariates we obtained for each district ('Landkreis').
However, the final CSVs are in different resolutions in respect to age & sex of the infected.
In addition, one data set includes the cumulative case count & death counts for each Landkreis to each point of time (i.e. the full grid).

|filename | description|
|---|---|
| `covid_merged_by_lk.csv`| All new occuring cases per Landkreis, no distinction in regards to sex & age|
| `covid_merged_by_lk_withzero_cumulative.csv`| All cases + cumulative cases per Landkreis, for all timesteps and all Landkreise (full grid)|
| `covid_merged_by_age.csv`| All new occuring cases per Landkreis, additionally split by age group|
| `covid_merged_by_sex.csv`| All new occuring cases per Landkreis, additionally split by sex|
| `covid_merged_by_sexage.csv`| All new occuring cases per Landkreis, split by age group and sex|

### Used Data Sets and Licenses
(see `data/overview_of_datasets.csv` for an up-to-date version)
|name|status|source|description|license|
|--- |---|---|---|---|
|`bev.csv`|1|[regionaldatenbank/genesis Code: 12411-02-03-4](https://www.regionalstatistik.de/genesis/online/logon)|Population by Age brackets and 'Landkreis' (2018-12-31)|[dl-de-by-2.0](https://www.govdata.de/dl-de/by-2-0)|
|`pflegebed.csv`|1|[regionaldatenbank/genesis: Code 22411-02-04-4](https://www.regionalstatistik.de/genesis/online/logon)| Number of people in need of care and currently under care, by 'Landkreis'|[dl-de-by-2.0](https://www.govdata.de/dl-de/by-2-0)|
|`krankenh.csv`|1|[regionaldatenbank/genesis: Code 23111-01-04-4](https://www.regionalstatistik.de/genesis/online/logon)|Information about number of hospitals and bed capacities by 'Landkreis' (2018)|[dl-de-by-2.0](https://www.govdata.de/dl-de/by-2-0)|
|`landkreise_areas.csv`|2|[opendatasoft](https://public.opendatasoft.com/explore/dataset/landkreise-in-germany)|Information about Districts ('Landkreise') including coordinates & areas.|[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)|
|`numhochschulen_per_plz.csv`|1|[npgeo corona](https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/379e258b9a004236a3ddeab031acbb98_0/)| Number of colleges & universities by community/city ('PLZ')|[ODbL](https://opendatacommons.org/licenses/odbl/index.html)|
|zipcodes.de|1|[github:zauberware/postal-codes-json-xml-csv](https://github.com/zauberware/postal-codes-json-xml-csv/blob/master/data/DE/zipcodes.de.csv)|Town/Community Code ('PLZ') and corresponding district code ('Kreisnummer' belonging to 'Landkreis')|[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)|

## Adding new CSVs
Upon adding a csv please run the script in `code/submit_dataset_info.py` to update the list of all datasets in this repo.
