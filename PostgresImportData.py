import pandas as pd
import psycopg2
from sqlalchemy import create_engine

database_name = "sbd"
postgres_url = "postgresql://postgres:docker@localhost:5432/" + database_name


def create_table_in_sbd_database(csv_name, table_name):
    # ref https://stackoverflow.com/questions/2987433/how-to-import-csv-file-data-into-a-postgresql-table
    df = pd.read_csv(csv_name, sep=";")
    df.columns = [c.lower() for c in df.columns]
    engine = create_engine(postgres_url)
    df.to_sql(table_name, engine, if_exists="replace")


def create_database():
    # ref https://stackoverflow.com/questions/34484066/create-a-postgres-database-using-python
    con = psycopg2.connect(dbname='postgres',
                           user="postgres", host='localhost',
                           password="docker")
    con.autocommit = True
    cur = con.cursor()
    cur.execute("DROP DATABASE IF EXISTS " + database_name)
    cur.execute("CREATE DATABASE " + database_name)
    con.close()

if __name__ == '__main__':
    create_database()
    create_table_in_sbd_database(csv_name="data/zameldowanie.csv", table_name="check_in")
    create_table_in_sbd_database(csv_name="data/adresy.csv", table_name="address")
    create_table_in_sbd_database(csv_name="data/rodzice.csv", table_name="parent")
    create_table_in_sbd_database(csv_name="data/zwiazki.csv", table_name="spouse")
    create_table_in_sbd_database(csv_name="data/osoby.csv", table_name="person")
