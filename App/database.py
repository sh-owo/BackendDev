import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")

# Create a MongoDB client
client = MongoClient(MONGO_URI)

# Access the database
db = client.get_database()

# Access the collection
notes_collection = db.get_collection("notes")

# Example usage of ObjectId
object_id = ObjectId()
print(object_id)