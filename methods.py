import json
import unirest
import sys
from pymongo import MongoClient
<<<<<<< HEAD
from pprint import pprint
import bson
from bson import json_util
import re
import ast
from bson.json_util import dumps


def delete(collectdata):
    collectdata.delete_many({})
=======




>>>>>>> b3e090c3be73d9180d46995eae23d265bd8e0226


"""puts ingredients in a string"""
def formatIngs(i):
    """Takes in a json of ingredients, formats them so that they can be used"""
    with open(i) as data_file:    
        data = json.load(data_file)
    ings = ""
    j = data["ingredients"]
    for x in j:
        if int(x["quantity"]) > 0:
            ings += "%2C" + str(x["name"]).lower()
    return ings[3:]
        
def getOptions(ings, options):
    """returns a json of a list of recipe. Takes in output of formatIngs"""
    response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?fillIngredients=true&ingredients=" + ings + "&limitLicense=false&number=10&ranking=2",
    headers={
<<<<<<< HEAD
        "X-Mashape-Key": "98cyiW4b9Omsh5H1Io9DyijHZESsp1wfa1BjsnSXqNq9fAyPC8",
=======
        "X-Mashape-Key": "8v3t0cFZU7mshkZplOb0JmeeGgH6p1S5OL0jsns4c8bSUeFeB3",
>>>>>>> b3e090c3be73d9180d46995eae23d265bd8e0226
        "Accept": "application/json"
    })
    options.update(response.body)


"""Searches for specific ingredients"""
"""takes two parameters, first is the options.json file, the second is the string to search for"""
"""First the program will seach the options available for that item, if it doesn't find anything, it will do a general search for that item"""
def search(searched, item, options):
    """Searches for a item (String) in the i file"""
    data = options
    results = []
    for titles in data:
        ings = titles['usedIngredients']
        for x in ings:
            if str(x['name']) == item:
                results.append(titles)
    if len(results) > 0: #checks to see if there are items in the options json that have the ingredient
        with open('searched.json', 'w+') as outfile:
            json.dump(results, outfile)
    else: #now will do a new search
        response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?fillIngredients=true&ingredients=" + item + "&limitLicense=false&number=10&ranking=2",
        headers={
<<<<<<< HEAD
            "X-Mashape-Key": "98cyiW4b9Omsh5H1Io9DyijHZESsp1wfa1BjsnSXqNq9fAyPC8",
=======
            "X-Mashape-Key": "8v3t0cFZU7mshkZplOb0JmeeGgH6p1S5OL0jsns4c8bSUeFeB3",
>>>>>>> b3e090c3be73d9180d46995eae23d265bd8e0226
            "Accept": "application/json"
        })
        searched.update(response.body)



"""params are the id of the item, returns array of ingredients"""
def getIngredients(identity):
    stuff = []
    response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/" + str(identity) + "/information?includeNutrition=false",
      headers={
<<<<<<< HEAD
        "X-Mashape-Key": "98cyiW4b9Omsh5H1Io9DyijHZESsp1wfa1BjsnSXqNq9fAyPC8",
=======
        "X-Mashape-Key": "8v3t0cFZU7mshkZplOb0JmeeGgH6p1S5OL0jsns4c8bSUeFeB3",
>>>>>>> b3e090c3be73d9180d46995eae23d265bd8e0226
        "Accept": "application/json"
      }
    )
    data = response.body["extendedIngredients"]
    for x in data:
        ing = {}
        ing['name'] = x['name'].encode('ascii')
        ing['quantity'] = (str(x['amount']) + " " + x['unit']).encode('ascii')
        stuff.append(ing)
    
    return stuff
                    
"""gets the recipe steps and puts it into a collection with ingredients"""
def recipe(identity, current):
    response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/324694/analyzedInstructions?stepBreakdown=true",
      headers={
<<<<<<< HEAD
        "X-Mashape-Key": "98cyiW4b9Omsh5H1Io9DyijHZESsp1wfa1BjsnSXqNq9fAyPC8",
=======
        "X-Mashape-Key": "8v3t0cFZU7mshkZplOb0JmeeGgH6p1S5OL0jsns4c8bSUeFeB3",
>>>>>>> b3e090c3be73d9180d46995eae23d265bd8e0226
        "Accept": "application/json"
      }
    )
    steps = []
    data = response.body
    number = 1
    for a in data:
        b = a['steps']
        for x in b:
            this = {}
            this['number'] = number
            this['step'] = x['step'].encode('ascii')
            number += 1
            steps.append(this)
    ings = getIngredients(identity)
    total = {"ingredients": ings, "steps": steps, "current step": 1}
    current.update(total)


"""add item to the pantry"""
def add(item, pantry):
<<<<<<< HEAD
    data = pantry['ingredients']
    data.append({"name": item, "quality": 4})
    return pantry

def remove(item, pantry):
    data = pantry['ingredients']
    for x in data:
        if x['name'] == item:
            x['quantity'] = 0
=======
    newPantry = pantry.copy()
    data = newPantry['ingredients']
    data.append({item: 4})
    pantry.update(newPantry)

def remove(item, pantry):
    newPantry = pantry.copy()
    data = newPantry['ingredients']
    for x in data:
        if x['name'] == item:
            x['quantity'] = 0
            pantry.update(newPantry)
>>>>>>> b3e090c3be73d9180d46995eae23d265bd8e0226
            return True
    return False


<<<<<<< HEAD
def todictionary(mongoFile):    
    for doc in pantry.find():
        e = dict(doc)
    return e
=======
        
>>>>>>> b3e090c3be73d9180d46995eae23d265bd8e0226
    

connect = MongoClient("mongodb://caren:kz7j7qLF1as2ktOG@cluster0-shard-00-00-yeacn.mongodb.net:27017,cluster0-shard-00-01-yeacn.mongodb.net:27017,cluster0-shard-00-02-yeacn.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
db = connect["avail-ingredients"]
pantry = db['pantry']
options = db['recommended']
current = db['currentrec']
searched = db['searched']

<<<<<<< HEAD
print e['ingredients']
print add("mushroom", todictionary(pantry))

#add("mushrooms", pantry)
#remove("apples", pantry)
=======
add("mushrooms", pantry)
>>>>>>> b3e090c3be73d9180d46995eae23d265bd8e0226









