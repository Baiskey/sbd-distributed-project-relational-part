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
MONGO_LOGIN = "python"
MONGO_PASSWORD = "python"
MONGO_URL = "mongodb+srv://"+MONGO_LOGIN+":"+MONGO_PASSWORD +"@sbdproject-piyfv.mongodb.net/test?retryWrites=true&w=majority"
DATABASE_NAME = "sbd_database"
PERSON_COLLECTION_NAME = "person"
ADDRESS_COLLECTION_NAME = "address"




def create_collection_from_json(name, json, database):
    collection = database[name]
    collection.insert_many(json)


def insert_persons_with_relationship_data_and_children_data_and_check_in_data(relationship_csv_path, person_csv_path,
                                                                              children_csv_path, check_in_csv_path):
    person_csv = pd.read_csv(person_csv_path, sep=";")
    persons_json = json.loads(person_csv.to_json(orient='records'))
    client = MongoClient(MONGO_URL)
    print(client.test)
    database = client[DATABASE_NAME]

    append_relationship_data_to_persons_json(persons_json, relationship_csv_path)
    append_children_data_to_persons_json(children_csv_path, persons_json)
    append_check_in_data_to_persons_json(check_in_csv_path, persons_json)

    create_collection_from_json(PERSON_COLLECTION_NAME, persons_json, database)


def append_relationship_data_to_persons_json(persons_json, relationship_csv_path):
    with open(relationship_csv_path, "r") as f:
        reader = csv.reader(f, delimiter=";")
        for i, line in enumerate(reader):
            if i == HEADER_ROW:
                continue
            first_spouse = int(line[2])
            second_spouse = int(line[3])
            marriage_beginning_date = line[0]
            for person in persons_json:
                if person['pesel'] == first_spouse:
                    person['spouse'] = int(second_spouse)
                    person['marriage_date'] = marriage_beginning_date
                    break
                if person['pesel'] == second_spouse:
                    person['spouse'] = int(first_spouse)
                    person['marriage_date'] = marriage_beginning_date
                    break


def append_children_data_to_persons_json(children_csv_path, persons_json):
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


def append_check_in_data_to_persons_json(check_in_csv_path, persons_json):
    with open(check_in_csv_path, "r") as f:
        reader = csv.reader(f, delimiter=";")
        for i, line in enumerate(reader):
            if i == HEADER_ROW:
                continue
            address_id = int(line[0])
            resident_pesel = int(line[1])
            resident_moved_date = line[2]
            for person in persons_json:
                if person['pesel'] == resident_pesel:
                    person['residence_id'] = address_id
                    person['residence_moved_date'] = resident_moved_date
                    break


def insert_address_with_check_in_data(address_csv_path):
    address_csv = pd.read_csv(address_csv_path, sep=";")
    address_json = json.loads(address_csv.to_json(orient='records'))
    client = MongoClient(MONGO_URL)
    database = client[DATABASE_NAME]

    create_collection_from_json(ADDRESS_COLLECTION_NAME, address_json, database)


if __name__ == '__main__':
    insert_persons_with_relationship_data_and_children_data_and_check_in_data(RELATIONSHIP_CSV_PATH, PERSON_CSV_PATH,
                                                                              CHILDREN_CSV_PATH, CHECK_IN_CSV_PATH)
    insert_address_with_check_in_data(ADDRESS_CSV_PATH)
