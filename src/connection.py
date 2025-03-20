from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")

def get_database():
    client = MongoClient(HOST)
    return client.get_database(DATABASE)