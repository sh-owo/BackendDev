import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

client = MongoClient(MONGODB_URL)
db = client['para2']

# 컬렉션 설정
users_collection = db['users']
notes_collection = db['notes']
