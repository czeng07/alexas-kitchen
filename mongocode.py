import json
import unirest
import sys
from pymongo import MongoClient



"""take json, and add to pantry"""
def addToMongo(mongPantry):
    with open('pantry.json') as data_file:    
        data = json.load(data_file)
    a = data['ingredients']
    for x in a:
        mongPantry.insert(x)
    
"""format names for API call"""
def nameFormat(mongPantry):
    ings = ""
    for doc in pantry.find():
        if int(doc["quantity"]) > 0:
            ings += "%2C" + str(doc["name"]).lower()
    return ings[3:]

def getOptions(mongPantry, options):
    """puts everything into the databasae"""
    response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?fillIngredients=true&ingredients=" + nameFormat(mongPantry) + "&limitLicense=false&number=20&ranking=2",
    headers={
        "X-Mashape-Key": "98cyiW4b9Omsh5H1Io9DyijHZESsp1wfa1BjsnSXqNq9fAyPC8",
        "Accept": "application/json"
    })
    for x in response.body:
        c = x['usedIngredients']
        d = []
        for ops in c:
            d.append(ops['name'])
        options.insert({"Title": x['title'], "id": x["id"], "ingredients": d})
    
"""add new item to the pantry"""
def addNew(mongPantry, item):
    mongPantry.insert({"name": item, "quantity": 5})


"""makes an item count go to 0"""
def remove(mongPantry, item):
    for doc in mongPantry.find():
        if doc['name'] == item:
            mongPantry.remove({"name": item})
            mongPantry.insert({"name": item, "quantity": 0})
            return True
    return False




"""Searches for specific ingredients"""
"""takes two parameters, first is the options.json file, the second is the string to search for"""
"""First the program will seach the options available for that item, if it doesn't find anything, it will do a general search for that item"""
def search(mSearch, item, options):
    """Searches for a item (String) in the i file"""
    count = 0
    for doc in options.find():
        if item in doc['ingredients']:
            mSearch.insert({"Title": doc['Title'], "id": doc['id']})
    if count < 0: #checks to see if there are items in the options json that have the ingredient
        response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?fillIngredients=true&ingredients=" + item + "&limitLicense=false&number=10&ranking=2",
        headers={
            "X-Mashape-Key": "98cyiW4b9Omsh5H1Io9DyijHZESsp1wfa1BjsnSXqNq9fAyPC8",
            "Accept": "application/json"
        })
        for x in response.body:
            mSearch.insert({"Title": x['title'], "id": x["id"]})
        
"""returns the ingredients list"""
def recipeIngredients(currentingredients, aId):
    response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/" + str(aId) + "/information?includeNutrition=false",
      headers={
        "X-Mashape-Key": "98cyiW4b9Omsh5H1Io9DyijHZESsp1wfa1BjsnSXqNq9fAyPC8",
        "Accept": "application/json"
      }
    )
    data = response.body["extendedIngredients"]
    for x in data:
        currentingredients.insert({"name": x['name'], "amount": str(x['amount']) + " " + x['unit'], "Image": x['image']})
        

"""instruction list"""
def recipeInstructions(currentinstructions, aId):
    response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/" + str(aId) + "/analyzedInstructions?stepBreakdown=true",
      headers={
        "X-Mashape-Key": "98cyiW4b9Omsh5H1Io9DyijHZESsp1wfa1BjsnSXqNq9fAyPC8",
        "Accept": "application/json"
      }
    )
    data = response.body
    number = 1
    for a in data:
        b = a['steps']
        for x in b:
            currentinstructions.insert({"Step Number": number, "Step": x['step']})
            number += 1

    currentinstructions.insert({"current step": 1})

    


"""wrapper method"""
def recipe(currentingredients, currentinstructions, aId):
    recipeIngredients(currentingredients, aId)
    recipeInstructions(currentinstructions, aId)
                                 
                                  

    
    



connect = MongoClient("mongodb://caren:kz7j7qLF1as2ktOG@cluster0-shard-00-00-yeacn.mongodb.net:27017,cluster0-shard-00-01-yeacn.mongodb.net:27017,cluster0-shard-00-02-yeacn.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
db = connect["avail-ingredients"]
pantry = db['pantry']
options = db['recommended']
current = db['currentrec']
searched = db['searched']
currentingredients = db['currentingredients']
currentinstructions = db['currentinstructions']


addToMongo(pantry)

getOptions(pantry, options)

search(searched, "chicken", options)

recipe(currentingredients, currentinstructions, 602708)












