# from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
# Load the MongoDB connection string from the environment variable MONGODB_URI
CONNECTION_STRING = os.getenv('MONGODB_URI')
db_name = os.getenv('DB_NAME')

class Database:
    client: MongoClient = None

    @classmethod
    def connect_db(cls):
        if not CONNECTION_STRING:
            raise ValueError("MONGODB_URI not found in environment variables")
        cls.client = MongoClient(CONNECTION_STRING)
        return cls.client

    @classmethod
    def close_db(cls):
        if cls.client is not None:
            cls.client.close()

    @classmethod
    def get_db(cls):
        if cls.client is None:
            cls.connect_db()  # Automatically connect if not connected
        return cls.client[db_name]