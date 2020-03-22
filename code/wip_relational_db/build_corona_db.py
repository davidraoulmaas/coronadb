import psycopg2
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
from pathlib import Path
from pandas import read_csv



def get_credentials():
    dbname = input('DB-Name: ')
    username = input('User Name: ')
    if len(username) == 0: username = 'postgres'
    password = input('Password: ')
    port = input('Port: ')
    if len(port) == 0: port = '5432'
    return {'dbname' : dbname, 'username' : username, 'password' : password, 'port' : port}

def create_corona_db(cred):
    con = psycopg2.connect(
        dbname = 'postgres',
        user = cred['username'], 
        password = cred['password'],
        port = cred['port'])
    con.autocommit = True
    cur = con.cursor()
    cur.execute('CREATE DATABASE {};'.format('corona_db'))
    con.close()


def tables_corona_db(cred):
    sql_land = 'CREATE TABLE land(\
        land CHAR(2),\
        name VARCHAR(255),\
        PRIMARY KEY(land)\
        );'
    sql_kreis = 'CREATE TABLE kreis(\
        krs INT,\
        land CHAR(2),\
        name VARCHAR(255),\
        PRIMARY KEY(krs),\
        FOREIGN KEY(land) REFERENCES land(land)\
        );'
    sql_bezirk = 'CREATE TABLE bezirk(\
        plz INT,\
        krs INT,\
        PRIMARY KEY(plz, krs),\
        FOREIGN KEY(krs) REFERENCES kreis(krs)\
        );'
    sql_faelle = 'CREATE TABLE faelle(\
        krs INT,\
        faelle INT,\
        geheilt INT,\
        todesfaelle INT,\
        datum DATE,\
        PRIMARY KEY(krs, datum),\
        FOREIGN KEY(krs) REFERENCES kreis(krs)\
        );'
    con = psycopg2.connect(
        dbname = cred['dbname'],
        user= cred['username'], 
        password = cred['password'],
        port = cred['port'])
    cur = con.cursor()
    cur.execute(sql_land)
    cur.execute(sql_kreis)
    cur.execute(sql_bezirk)
    cur.execute(sql_faelle)
    con.commit()
    con.close()


def init_corona_db(cred, path):
    sql_insert_land = 'INSERT INTO land\
        VALUES (%s, %s);'
    sql_insert_kreis = 'INSERT INTO kreis\
        VALUES (%s, %s, %s);'
    sql_insert_bezirk = 'INSERT INTO bezirk\
        VALUES (%s, %s);'
    con = psycopg2.connect(
        dbname = cred['dbname'],
        user= cred['username'], 
        password = cred['password'],
        port = cred['port'])
    cur = con.cursor()
    zip = read_csv(zip_p)
    laender = zip.loc[:,['state_code', 'state']].drop_duplicates()
    kreise = zip.loc[:,['community_code', 'state_code', 'community']].drop_duplicates()
    bezirke = zip.loc[:,['zipcode', 'community_code']].drop_duplicates()
    for index, row in laender.iterrows():
        cur.execute(sql_insert_land, (row['state_code'], row['state']))
    for index, row in kreise.iterrows():
        cur.execute(sql_insert_kreis, (row['community_code'], row['state_code'], row['community']))
    for index, row in bezirke.iterrows():
        cur.execute(sql_insert_bezirk, (row['zipcode'], row['community_code']))
    con.commit()
    con.close()


main_dir = Path(__file__).absolute().parent.parent.parent
zip_p = Path.joinpath(main_dir, 'data', '01_raw_data', 'zipcodes.de.csv')
cred = get_credentials()
create_corona_db(cred)
tables_corona_db(cred)
init_corona_db(cred, zip_p)