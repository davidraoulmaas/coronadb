# coronadb

Upon adding a csv please run the script in `code/submit_dataset_info.py` to update the list of all datasets in this repo.
### Merged Data
In `data/03_integrated_data` you can find the final CSVs,
which are all COVID-19 data merged with the different covariates we obtained for each landkreis.
However, the final CSVs are in different resolutions in respect to age & sex of the infected.
In addition, one data set includes the cumulative case & death counts for each Landkreis to each point of time (i.e. the full grid).

|filename | description|
|---|---|
| covid_merged_by_lk.csv| All new occuring cases per Landkreis, no distinction in regards to sex & age|
| covid_merged_by_lk_withzero_cumulative.csv| All cases + cumulative cases per Landkreis, for all timesteps and all Landkreise (full grid)|
||
| covid_merged_by_age.csv| All new occuring cases per Landkreis, additionally split by age group|
| covid_merged_by_sex.csv| All new occuring cases per Landkreis, additionally split by sex|
| covid_merged_by_sexage.csv| All new occuring cases per Landkreis, split by age group and sex|

### Used Data Sets 
(see `data/overview_of_datasets.csv` for an up-to-date version)
|name|status|source|description|license|
|--- |---|---|---|---|
|bev|2|regionaldatenbank/genesis|Bevoelkerung nach Altersklasse auf Kreisebene (Stand 2018)|dl-de-by-2.0|
|pflegebed|2|regionaldatenbank/genesis|Pflegebeduerftige/Pflegegeldempfaenger nach Kreis|dl-de-by-2.0|
|krankenh|2|regionaldatenbank/genesis|Informationen ueber Krankenhauszahl und Bettenkapazitaeten nach Abteilung per Kreis (2018)|dl-de-by-2.0|
|intensiv|2|DIVI Intensivregister|Anzahl Intensivkliniken pro PLZ|erhoben von divi.de|
|landkreise_areas|2|https://public.opendatasoft.com/explore/dataset/landkreise-in-germany|Landkreise, their centroids, and their area.|CC BY-NC-SA 4.0|
|numhochschulen_per_plz|1|https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/379e258b9a004236a3ddeab031acbb98_0/|Anzahl Hochschulen  per Stadt/PLZ|ODbL|
|zipcodes.de|1|https://github.com/zauberware/postal-codes-json-xml-csv/blob/master/data/DE/zipcodes.de.csv|PLZ und zugehörige Landkreisnummern|CC-BY-4.0|
