from pymongo import MongoClient

client = MongoClient(" INSERT CONNECTION STRING")
db = client["robots"]
