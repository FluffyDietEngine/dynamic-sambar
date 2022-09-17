from typing import Dict

from prefect import task
from pymongo import MongoClient

DATABASE = 'IGR-MH'
COLLECTION = 'METADATA'

def connection(db_: str = DATABASE, collection: str = COLLECTION):
    database = MongoClient()
    print(db_, collection)
    connection = database[db_][collection]
    return connection

@task(retries=5)
def insert_data(db: str, col: str, data: Dict):
    collection = connection(db, col)
    doc = collection.insert_one(data)
    return doc.inserted_id