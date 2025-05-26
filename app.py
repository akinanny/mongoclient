from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pprint import pprint
import os

app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
DATABASE_NAME = "clinicdb"
COLLECTION_NAME = "patients"

# Init DB connection once
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()
    print("✅ Connected to MongoDB")
except ConnectionFailure as e:
    print(f"❌ Cannot connect to MongoDB: {e}")
    exit(1)

db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

@app.on_event("startup")
def ensure_sample():
    if collection.count_documents({}) == 0:
        collection.insert_one({
            "name": "Ali Kinany",
            "age": 30,
            "gender": "Male",
            "condition": "Flu"
        })
        print("✅ Inserted sample patient")

@app.get("/patients")
def list_patients():
    return list(collection.find({}, {"_id": 0}))

