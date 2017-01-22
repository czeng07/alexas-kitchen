import json
from pprint import pprint
import unirest
import sys

def formatIngs(i):
    """Takes in a list of ingredients, formats them so that they can be used"""
    with open(i) as data_file:
        data = json.load(data_file)
    ings = ""
    j = data["ingredients"]
    for x in j:
        if int(x["quantity"]) > 0:
            ings += "%2C" + str(x["name"]).lower()
    return ings[3:]

def getRecipe(ings):
    """returns a json of the recipe"""
    response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?fillIngredients=true&ingredients=" + ings + "&limitLicense=false&number=10&ranking=2",
    headers={
        "X-Mashape-Key": "8v3t0cFZU7mshkZplOb0JmeeGgH6p1S5OL0jsns4c8bSUeFeB3",
        "Accept": "application/json"
    })
    with open('options.json', 'w+') as outfile:
        json.dump(response.body, outfile)

#ingredients = formatIngs(sys.argv[1])
#getRecipe(ingredients)
