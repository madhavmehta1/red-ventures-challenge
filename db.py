from pymongo import MongoClient

client = MongoClient("mongodb+srv://default:G5WPf6xVW2AoFWmz@rvchallenge-vsqmn.mongodb.net/test?retryWrites=true&w=majority")
db = client["robots"]
