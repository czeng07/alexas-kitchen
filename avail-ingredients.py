
from pymongo import MongoClient
#import pymongo
import json


client = MongoClient("mongodb://caren:kz7j7qLF1as2ktOG@cluster0-shard-00-00-yeacn.mongodb.net:27017,cluster0-shard-00-01-yeacn.mongodb.net:27017,cluster0-shard-00-02-yeacn.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
db = client['avail-ingredients']


pantry = db['pantry']
recommended = db['recommended']
currentrec= db['currentrec']
searched = db['searched']


with open('pantry.json') as data_file:
  data = json.load(data_file)
  pantry.insert(data)
  #pantry.update(data, {'upsert': False})
  #pantry.ingredients.delete_many({})
  #pantry.replaceOne({}, data, False)
  pantry.delete_many({})
  #pantry.insert({"name":"cherry","quantity":3})
  #pantry.insert({"name":"apple","quantity":4})
  #pantry.insert({"name":"peach","quantity":1})


with open('options.json') as data_file:
    data = json.load(data_file)
    recommended.delete_many({})

with open('searched.json') as data_file:
    data = json.load(data_file)
    searched.delete_many({})

#for doc in pantry.find():
#    print doc["name"]

#pantry.remove({"name":"cherry"})
#pantry.remove()




    #print doc
    #print doc["ingredients"]
    #for
    #print i["name"]

    #break
