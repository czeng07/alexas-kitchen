import json
import pprint as pprint
import sys

def formatIngs(i):
    """Takes in a list of ingredients, formats them so that they can be used"""
    with open(i) as data_file:    
        data = json.load(data_file)
    ings = ""
    j = data["ingredients"]
    for x in j:
        ings += "%2C" + str(x["name"]).lower()
    return ings[3:]


def a(i):
    with open(i) as data_file:    
        data = json.load(data_file)

a(sys.argv[1])
