import json
import unirest
import sys
from pymongo import MongoClient

connect = MongoClient("mongodb://caren:kz7j7qLF1as2ktOG@cluster0-shard-00-00-yeacn.mongodb.net:27017,cluster0-shard-00-01-yeacn.mongodb.net:27017,cluster0-shard-00-02-yeacn.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
db = connect["avail-ingredients"]
pantry = db['pantry']
options = db['recommended']
current = db['currentrec']
searched = db['searched']
currentingredients = db['currentingredients']
currentinstructions = db['currentinstructions']
cStep = db['currentstep']
cart = db['shopping']

"""items that are at 0 in the pantry"""
def shoppingCart(cart, pantry):
    items = []
    for doc in pantry.find():
        if doc['quantity'] == 0:
            items.append(doc['name'])
    return items


print shoppingCart(cart, pantry)
