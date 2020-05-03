import pandas as pd
from sqlalchemy import create_engine

postgres_url = "postgresql://postgres:docker@localhost:5432/sbd"


def create_table_in_sbd_database(csv_name, table_name):
    # ref https://stackoverflow.com/questions/2987433/how-to-import-csv-file-data-into-a-postgresql-table
    df = pd.read_csv(csv_name)
    df.columns = [c.lower for c in df.columns]
    engine = create_engine(postgres_url)
    df.to_sql(table_name, engine, if_exists="replace")


if __name__ == '__main__':
    create_table_in_sbd_database(csv_name="data/zameldowanie.csv", table_name="check_in")
    create_table_in_sbd_database(csv_name="data/adresy.csv", table_name="address")
    create_table_in_sbd_database(csv_name="data/rodzice.csv", table_name="parent")
    create_table_in_sbd_database(csv_name="data/zwiazki.csv", table_name="spouse")
    create_table_in_sbd_database(csv_name="data/osoby.csv", table_name="person")
