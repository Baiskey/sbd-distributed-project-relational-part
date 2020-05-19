import csv
import json

import pandas as pd
from pymongo import MongoClient

RELATIONSHIP_CSV_PATH = "data/zwiazki.csv"
PERSON_CSV_PATH = "data/osoby.csv"
ADDRESS_CSV_PATH = "data/adresy.csv"
CHECK_IN_CSV_PATH = "data/zameldowanie.csv"
CHILDREN_CSV_PATH = "data/rodzice.csv"

HEADER_ROW = 0
MONGO_URL = "localhost:27017"
DATABASE_NAME = "test_database"
PERSON_COLLECTION_NAME = "person"
ADDRESS_COLLECTION_NAME = "address"


def create_collection_from_csv(name, csv_path, database):
    collection = database[name]
    data_in_csv = pd.read_csv(csv_path, sep=";")
    data_in_json = json.loads(data_in_csv.to_json(orient='records'))
    collection.insert_many(data_in_json)


def create_collection_from_json(name, json, database):
    collection = database[name]
    collection.insert_many(json)


def create_database_with_data():
    client = MongoClient(MONGO_URL)
    created_database = client[DATABASE_NAME]
    create_collection_from_csv(PERSON_COLLECTION_NAME, PERSON_CSV_PATH, created_database)
    create_collection_from_csv(ADDRESS_COLLECTION_NAME, ADDRESS_CSV_PATH, created_database)


def insert_persons_with_relationship_data_and_children_data(relationship_csv_path, person_csv_path, children_csv_path):
    person_csv = pd.read_csv(person_csv_path, sep=";")
    persons_json = json.loads(person_csv.to_json(orient='records'))
    client = MongoClient(MONGO_URL)
    database = client[DATABASE_NAME]

    with open(relationship_csv_path, "r") as f:
        reader = csv.reader(f, delimiter=";")
        for i, line in enumerate(reader):
            if i == HEADER_ROW:
                continue
            first_spouse = int(line[2])
            second_spouse = int(line[3])
            for person in persons_json:
                if person['pesel'] == first_spouse:
                    person['marriage_data'] = {'spouse': second_spouse}
                    break
                if person['pesel'] == second_spouse:
                    person['marriage_data'] = {'spouse': first_spouse}
                    break

    with open(children_csv_path, "r") as f:
        reader = csv.reader(f, delimiter=";")
        for i, line in enumerate(reader):
            if i == HEADER_ROW:
                continue
            child_id = int(line[0])
            parent_id = int(line[1])
            for person in persons_json:
                if person['pesel'] == parent_id:
                    try:
                        person['children'].append(child_id)
                    except KeyError as e:
                        person.update({'children': [child_id]})
                        break

    create_collection_from_json(PERSON_COLLECTION_NAME, persons_json, database)


def insert_address_with_check_in_data(address_csv_path, check_in_csv_path):
    address_csv = pd.read_csv(address_csv_path, sep=";")
    address_json = json.loads(address_csv.to_json(orient='records'))
    client = MongoClient(MONGO_URL)
    database = client[DATABASE_NAME]

    with open(check_in_csv_path, "r") as f:
        reader = csv.reader(f, delimiter=";")
        for i, line in enumerate(reader):
            if i == HEADER_ROW:
                continue
            address_id = int(line[0])
            for address in address_json:
                if address['id'] == address_id:
                    resident_pesel = line[1]
                    resident_moved_date = line[2]
                    address['resident_pesel'] = int(resident_pesel)
                    address['moved_date'] = resident_moved_date
                    break
    create_collection_from_json(ADDRESS_COLLECTION_NAME, address_json, database)


if __name__ == '__main__':
    insert_persons_with_relationship_data_and_children_data(RELATIONSHIP_CSV_PATH, PERSON_CSV_PATH, CHILDREN_CSV_PATH)
    insert_address_with_check_in_data(ADDRESS_CSV_PATH, CHECK_IN_CSV_PATH)
