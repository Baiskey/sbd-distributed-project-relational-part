import json

import pandas as pd
from pymongo import MongoClient

MONGO_URL = "localhost:27017"
DATABASE_NAME = "test_database"


def create_collection(name, csv_path, database):
    collection = database[name]
    data_in_csv = pd.read_csv(csv_path, sep=";")
    data_in_json = json.loads(data_in_csv.to_json(orient='records'))
    collection.insert_many(data_in_json)


def create_database_with_data():
    client = MongoClient(MONGO_URL)
    created_database = client[DATABASE_NAME]
    create_collection("person", "data/osoby.csv", created_database)
    create_collection("address", "data/adresy.csv", created_database)


if __name__ == '__main__':
    create_database_with_data()
