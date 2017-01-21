import json
import sys

"""Searches for specific ingredients"""
"""takes two parameters, first is the options.json file, the second is the string to search for"""
"""First the program will seach the options available for that item, if it doesn't find anything, it will do a general search for that item"""
def search(i, item):
    """Searches for a item (String) in the i file"""
    with open(i) as data_file:    
        data = json.load(data_file)
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
            "X-Mashape-Key": "8v3t0cFZU7mshkZplOb0JmeeGgH6p1S5OL0jsns4c8bSUeFeB3",
            "Accept": "application/json"
        })
        with open('searched.json', 'w+') as outfile:
            json.dump(response.body, outfile)





search(sys.argv[1], sys.argv[2])





