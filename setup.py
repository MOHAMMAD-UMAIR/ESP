
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

uri = "mongodb+srv://umair:umairmongo@cluster0.pgkqn44.mongodb.net/?retryWrites=true&w=majority"

# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
import ast

import pymongo
import json
from pymongo import MongoClient, InsertOne

client = pymongo.MongoClient(uri)
db = client.Project0
collection = db.Cluster0
requesting = []

# import urllib library 
from urllib.request import urlopen 
  
#url = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-14.0.json"

#response = urlopen(url) 

#data_json = json.loads(response.read()) 
with open(r"D:\ESP_workspace\ESP\artifacts\data_ingestion\data.json", 'r') as file:
    data = json.load(file)

# Extract the "objects" part of the JSON data
objects = data.get("objects", [])
# for obj in object:
#     print(obj)
#objects

# for jsonObj in data_json:
#     for obj in jsonObj:
#         if obj == 'object':
#             print(obj)
      
#         print(jsonObj)
    # myDict = json.loads(jsonObj)
    # requesting.append(InsertOne(myDict))

# result = collection.bulk_write(requesting)
collection.insert_many(objects)
client.close()