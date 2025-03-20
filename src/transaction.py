import connection
import json


def get_transaction():
    transaction = []
    for collection in connection.get_database().list_collection_names():
        transaction.extend(list(connection.get_database().get_collection(collection).find()))
    return transaction
