import json
from pymongo import MongoClient
client = None  #the client will be specified in the main code

#check if a step number is within the bounds of the recipe
def isValidStepNum(stepNum):
    recipe = client['avail-currentrec']
    return len(recipe['steps']) >= stepNum > 0

#get an array of all of the strings of the steps
def getStepsString():
    db = client['avail-currentrec']
    recipe = db
    steps = []
    for i in range(len(recipe['steps'])):
        steps[i] = "Step " + (i + 1) + " . " + recipe['steps'][i]['step']

    return steps

#get the String for the stepNum-th step
def getStep(stepNum):
    recipe = client['avail-ingredients.currentrec']
    return "Step " + stepNum + "." + recipe['steps'][stepNum - 1]['step']

#set the choice-th recipe on the list to the current recipe
def setRecipe(choice):
    recipeList = client['avail-options']
    idNum = recipeList[choice - 1]['id']
    getRecipe(id, 'avail-ingredients.currentrec')
    return

def isValidRecipeNum(choice):
    return 0 < choice <= 10

#get the String for the choice-th recipe from the options list
def getRecipe(choice):
    recipeList = client['avail-options']
    return "Recipe " + (choice) + "." + recipeList[choice-1]['name']