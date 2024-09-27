from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize MongoDB connection
def get_mongo_client():
    client = MongoClient(os.getenv('MONGO_URI'))
    return client

# Check MongoDB connection
def check_mongo_connection(client):
    try:
        client.admin.command('ping')
        print("MongoDB connection: Successful")
    except errors.ConnectionFailure:
        print("MongoDB connection: Failed")

# Get the database
def get_database(client, db_name=os.getenv('DB_NAME')):
    return client.get_database(db_name)

# Initialize the database and check the connection
client = get_mongo_client()
check_mongo_connection(client)
database = get_database(client)