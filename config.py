from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000) 

db = client["movie_review_db"]
   

movies_collection = db["movies"]
reviews_collection = db["reviews"]