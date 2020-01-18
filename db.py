from pymongo import MongoClient

client = MongoClient("mongodb+srv://default:MDvtwVxB42AJEgko@rvchallenge-vsqmn.mongodb.net/test?retryWrites=true&w=majority")
db = client["robots"]
