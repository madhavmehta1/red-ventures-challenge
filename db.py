from pymongo import MongoClient

client = MongoClient("mongodb+srv://[USER]:[PASS]@rvchallenge-vsqmn.mongodb.net/test?retryWrites=true&w=majority")
db = client["robots"]
