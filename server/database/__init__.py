from pymongo import MongoClient

mongo_client = MongoClient("mongo")
db = mongo_client["projectDB"]

accounts = db['accounts'] # account data
files = db['files'] # file data

