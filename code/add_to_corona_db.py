import psycopg2
import numpy as np
import re
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


def add_table(path, id, cred):
    sql_add_column = 'ALTER TABLE %s\
        ADD %s %s;'
    sql_update = 'UPDATE %s\
        SET %s = %s\
        WHERE %s = %s'
    con = psycopg2.connect(
            dbname = cred['dbname'],
            user= cred['username'], 
            password = cred['password'],
            port = cred['port'])
    cur = con.cursor()
    data = read_csv(file_p)
    columns = data.columns  
    if id not in ['plz', 'krs', 'land', 'fall']: 
        id = 'NA'
    if id == 'NA':
        if 'plz' in columns: 
            id = 'plz'
        elif 'krs' in columns: 
            id = 'krs'
        elif 'land' in columns: 
            id = 'land'     
    if id == 'plz':
        table = 'bezirk'
    elif id == 'krs': 
        table = 'kreis'
    elif id == 'land':
        table = 'land'
    keys = data[id]
    columns = [col for col in columns if col not in ['Unnamed: 0', 'name', 'plz', 'krs', 'land']]
    for col in columns:
        insert_col = input('Insert Column ' + col + '? ')
        if insert_col == 'T':
            col_ = re.sub("[- ]", "_", col)
            type = input('Data Type: ')
            cur.execute(sql_add_column % (table, col_, type))
            for i in range(len(data[col])):
                if not np.isnan(data[col][i]):
                    cur.execute(sql_update % (table, col_, data[col][i], id, keys[i]))
    con.commit()
    con.close()


file = input('Add CSV: ')
id = input('Id Variable: ')
main_dir = Path(__file__).absolute().parent.parent
file_p = Path.joinpath(main_dir, 'data', '01_raw_data', file)
cred = get_credentials()
add_table(file_p, id, cred)

