import json
from pymongo import MongoClient
import unirest

connect = MongoClient("mongodb://caren:kz7j7qLF1as2ktOG@cluster0-shard-00-00-yeacn.mongodb.net:27017,cluster0-shard-00-01-yeacn.mongodb.net:27017,cluster0-shard-00-02-yeacn.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
db = connect["avail-ingredients"]
pantry = db['pantry']
options = db['recommended']
current = db['currentrec']
searched = db['searched']
currentingredients = db['currentingredients']
currentinstructions = db['currentinstructions']
cStep = db['currentstep']



#get an array of all of the strings of the steps
def getStepsString(inst):
    steps = {}
    stepArray = []
    for doc in inst.find():
        steps[doc['Step Number']] = doc['Step']
    length = 0
    for a in steps:
        length += 1
    for x in xrange(1, length+1):
        stepArray.append(steps[x])
    return stepArray

def recipeSelection(options):
    ops = []
    for doc in options.find():
        ops.append(doc['Title'] + ":::" + str(doc['id']))
    return ops









#print getStepsString(currentinstructions)

#print recipeSelection(options)
