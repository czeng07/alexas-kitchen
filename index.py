
from __future__ import print_function

from mon_code import *
from shopping import *
from recipe import *
from recipeStuff import *
from pymongo import MongoClient

connect = MongoClient("mongodb://caren:kz7j7qLF1as2ktOG@cluster0-shard-00-00-yeacn.mongodb.net:27017,cluster0-shard-00-01-yeacn.mongodb.net:27017,cluster0-shard-00-02-yeacn.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
db = connect["avail-ingredients"]
pantry = db['pantry']
options = db['recommended']
current = db['currentrec']
searched = db['searched']
currentingredients = db['currentingredients']
currentinstructions = db['currentinstructions']
lists = db['lists']


#import requests

# --------------- Helpers that build all of the responses ----------------------


# Builds a generic error
def build_error_response():
    return build_response({}, build_speechlet_response('Sorry',
                            'Command not recognized.', 'Command not recognized',
                             ' ', True))


# Builds a customized speech response based on parameters
def build_speechlet_response(title, output, text, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': text
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


# Builds an entire response, including attributes
def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------


# Called when Gordan is opened without arguments
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hello, I am Gordon Ramsay, your personal cooking " \
                    "assistant. To learn more about my abilities, say " \
                    "help."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Sorry, I could not understand. Please say help for a " \
                    "list of options."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, speech_output, reprompt_text,
        should_end_session))

# Called when the session is about to end.
def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Command cancelled."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, speech_output, None, should_end_session))



# Dictates main help menu option to users
def get_main_help_response(intent, session):
    session_attributes = {}
    text_output = "Commands:\n - Pantry help\n - Search help\n - Recipe help"
    speech_output = "Please choose one of the following. Pantry help. " \
                    "Search help. Or Recipe help."
    reprompt_text = "Please say Pantry help, search help, or recipe help."

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        "Main Help", speech_output, text_output, reprompt_text,
        should_end_session))


# Gets user's selection from the main help menu
def get_main_help_selection(intent, session):

    choice = str(intent['slots']['main_help_choice']['value'])
    session_attributes = {}



    if choice == 'pantry help':
        title = "Pantry Help"
        text_output = "Commands:\n - Add help\n - Remove help."
        speech_output = "Please choose one of the following. Add " \
                        "help. Or Remove help."
        reprompt_text = "Please say Add Help or Remove help"
        should_end_session = False
    elif choice == 'search help':
        title = "Search Help"
        speech_output = "Please choose one of the following. Find help. " \
                        "Recommend help"
        text_output = "Commands:\n - Find help\n - Recommend help"
        reprompt_text = "Please say Find help or Recommend help"
        should_end_session = False
    elif choice == 'recipe help':
        title = "Recipe Help"
        speech_output = "Please choose one of the following. Ingredient help. " \
                        "Or Instruction help"
        text_output = "Commands:\n - Ingredient help\n - Instruction help"
        reprompt_text = "Please say Ingredient help or Instruction help"
        should_end_session = False
    else:
        return build_error_response()



    return build_response(session_attributes, build_speechlet_response(
        title, speech_output, text_output, reprompt_text, should_end_session))


# Gets user's selection from the pantry help menu
def get_pantry_help_selection(intent, session):

    choice = str(intent['slots']['pantry_help_choice']['value'])
    session_attributes = {}

    if choice == 'add help':
        title = "Add Help"
        speech_output = "You can add an item to the pantry by saying," \
                        "add, item name, to pantry."
        text_output = "Add item to pantry\n" \
                        " - \'add [item_name] to pantry.\'"
        reprompt_text = "If you would like to use another command, say it now."
        should_end_session = False
    elif choice == 'remove help':
        title = "Remove Help"
        speech_output = "You can remove an item from the pantry by saying," \
                        "remove, item name, from pantry."
        text_output = "Remove item from pantry\n" \
                        " - \'remove [item_name] from pantry.\'"
        reprompt_text = "If you would like to use another command, say it now."
        should_end_session = False
    else:
        return build_error_response()


    return build_response(session_attributes, build_speechlet_response(
        title, speech_output, text_output, reprompt_text, should_end_session))


# Gets user's selection from the search help menu
def get_search_help_selection(intent, session):

    choice = str(intent['slots']['search_help_choice']['value'])
    session_attributes = {}

    if choice == 'find help':
        title = "Find Help"
        speech_output = "You can search recipes with a specific item by " \
                        "saying, find recipes with, item name"
        text_output = "Search recipes with item:\n" \
                        " - \'find recipes with [item_name]\'"
        reprompt_text = "If you would like to use another command, say it now."
        should_end_session = False
    elif choice == 'recommend help':
        title = "Recommend Help"
        speech_output = "You can get recommended recipes based on your pantry" \
                        " by saying, recommend, or, suggest."
        text_output = "Get suggested recipes:\n" \
                        " - \'recommend\'\n - \'suggest\'"
        reprompt_text = "If you would like to use another command, say it now."
        should_end_session = False
    else:
        return build_error_response()


    return build_response(session_attributes, build_speechlet_response(
        title, speech_output, text_output, reprompt_text, should_end_session))


# Removes a pantry item, if it exists
def remove_pantry_item(intent, session):
    item = str(intent['slots']['remove_pantry_item']['value']).lower()
    title = "Remove Item from Pantry"
    session_attributes = {}

    success = remove(pantry,item)

    if success:
        speech_output = "Succesfully removed " + item + " from pantry."
        text_output = "Succesfully removed " + item + " from pantry."
        reprompt_text = " "
    else:
        speech_output = "You had no " + item + " in your pantry."
        text_output = "You had no " + item + " in your pantry."
        reprompt_text = " "
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        title, speech_output, text_output, reprompt_text, should_end_session))


#Adds an item to the pantry
def add_pantry_item(intent, session):
    item = str(intent['slots']['add_pantry_item']['value']).lower()
    session_attributes = {"add_item":item}
    title = "Add Item to Pantry"
    speech_output = "Are you sure you would like to add " + item + " to "\
                    "your pantry list."
    text_output = "Add " + item + " to pantry list?\n" \
                " Yes/No?"
    reprompt_text = "Please say yes or no."
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
            title, speech_output, text_output, reprompt_text, should_end_session))


# Handle Yes/No user input for adding item
def accept_add(intent, session):
    acceptance = str(intent['slots']['yes_or_no']['value'])
    if "add_item" in session["attributes"]:
        item = str(session['attributes']['add_item'])
        session_attributes = {}
        if acceptance == "yes":

            title = "Added"
            speech_output = "Item was added succesfully."
            text_output = "Item was added succesfully."
            reprompt_text = "If you would like to add or remove items from the " \
                            "the pantry, use the commands add and remove."
            should_end_session = False

            # Adds item to the MongoDB database
            addNew(pantry,item)

        else:

            title = "Not Added"
            speech_output = "Item was not added."
            text_output = "Item was not added."
            reprompt_text = "If you would like to add or remove items from the " \
                            "the pantry, use the commands add and remove."
            should_end_session = False

        return build_response(session_attributes, build_speechlet_response(
                title, speech_output, text_output, reprompt_text, should_end_session))
    else:
        return build_error_response()


# Gets user's selection from the search help menu
def get_recipe_help_selection(intent, session):

    choice = str(intent['slots']['recipe_help_choice']['value'])
    session_attributes = {}

    if choice == 'ingredient help':
        title = "Ingredient Help"
        speech_output = "To list all ingredients, say, list ingredients."
        text_output = "List all ingredients:\n - \'list ingredients\'"
        reprompt_text = "If you would like to use another command, say it now."
        should_end_session = False
    elif choice == 'instruction help':
        title = "Instruction Help"
        speech_output = "To start listing steps, say, start recipe. " \
                        "To list the next step, say, go to next step. ... " \
                        "To list the previous step, say, go to previous step. " \
                        "...To repeat the current step, say, repeat step. ... " \
                        "To list a specific step, say, repeat step, followed " \
                        "by the step number. "
        text_output = "Start recipe: \'start recipe\'\n" \
                        "List the next step: \'go to next step\'\n" \
                        "List the previous step: \'go to previous step\'\n" \
                        "Repeat the current step: \'repeat\'\n" \
                        "List a specific step: \'repeat step [number]\'\n"
        reprompt_text = "If you would like to use another command, say it now."
        should_end_session = False
    else:
        return build_error_response


    return build_response(session_attributes, build_speechlet_response(
        "Recipe Help", speech_output, text_output, reprompt_text, should_end_session))


#List all items in the pantry
def list_pantry_items(intent, session):
    session_attributes = {}
    title = "Pantry Items"
    speech_output = "Your pantry contains"
    text_output = "Your pantry contains:\n"
    for doc in pantry.find():
        if doc["quantity"] != 0:
            speech_output = speech_output + ", " + doc["name"]
            text_output = text_output + " - " + doc["name"] + "\n"
    reprompt_text = "If you would like to add or remove items from the " \
                    "the pantry, use the commands add and remove."
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        title, speech_output, text_output, reprompt_text, should_end_session))


# Find recipes with an ingredient
def find_recipes(intent, session):

    item = str(intent['slots']['find_recipe_item']['value'])
    session_attributes = {}
    title = "Recommend Recipes"
    speech_output = "I have found some recipes with " + item + ". If you "\
                    "would like to hear them, please say, list recipes."
    text_output = "Say 'list recipes' to hear the recipes I found."
    reprompt_text = "Say, list recipes, to hear the available recipes."
    should_end_session = False

    lists.delete_many({})
    search(lists, item, options)

    return build_response(session_attributes, build_speechlet_response(
            title, speech_output, text_output, reprompt_text, should_end_session))


# Find recipes by pantry items
def recommend_recipes(intent, session):


    session_attributes = {}
    title = "Recommend Recipes"
    speech_output = "I have found some recipes based on your pantry items. If you "\
                    "would like to hear them, please say, list recipes."
    text_output = "Say 'list recipes' to hear the recipes I found."
    reprompt_text = "Say, list recipes, to hear the available recipes."
    should_end_session = False

    options.delete_many({})
    lists.delete_many({})
    getOptions(pantry, options, lists)

    return build_response(session_attributes, build_speechlet_response(
            title, speech_output, text_output, reprompt_text, should_end_session))



# Allows a user to choose a recipe by number
def choose_recipe(intent, session):

    recipe_number = int(intent['slots']['recipe_choice']['value'])
    print(recipe_number)
    session_attributes = {}
    if recipe_number > 7 or recipe_number < 1:
        title = "Choose Recipes"
        speech_output = "That is not a valid recipe number."
        text_output = "Not valid."
        reprompt_text = " "
        should_end_session = True
    else:
        title = "Choose Recipes"
        recipe_array = recipeSelection(lists)
        speech_output = "You have chosen recipe " + str(recipe_number) + "." \
         " " + str(recipe_array[recipe_number-1]).split(":::")[0]
        text_output = "You have chosen recipe " + str(recipe_number) + "."
        Aid = str(recipe_array[recipe_number-1]).split(":::")[1]
        currentingredients.delete_many({})
        currentinstructions.delete_many({})
        recipe(currentingredients, currentinstructions, Aid)
        reprompt_text = " "
        should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
            title, speech_output, text_output, reprompt_text, should_end_session))


# Lists the recipes available as a result of user search
def list_recipes(intent, session):

    session_attributes = {}
    print("hell no")
    title = "List Recipes"
    recipe_array = recipeSelection(lists)
    recipe_string = " "
    for i in xrange(len(recipe_array)):
        recipe_string = recipe_string + "Recipe number " + str(i+1) + "." \
        " " + recipe_array[i].split(":::")[0] + ".\n"
    speech_output = "Here are several recipes you might like. " + recipe_string + " " \
        " You can choose a recipe by saying the phrase, 'choose recipe', followed " \
        " by the number of the recipe."
    text_output = "Recipes:\n"+recipe_string
    reprompt_text = " You can choose a recipe by saying the phrase, 'choose recipe', followed " \
    " by the number of the recipe."
    should_end_session = False


    return build_response(session_attributes, build_speechlet_response(
            title, speech_output, text_output, reprompt_text, should_end_session))


# List all ingredients (with amounts) used in the recipe
def list_ingredients(intent, session):
    session_attributes = {}
    title = "List Ingredients"
    ingredients = ""
    for doc in currentingredients.find():
        ingredients = ingredients + doc['amount']+" "+doc['name']+","
    speech_output = ingredients
    text_output = ingredients
    reprompt_text = "Say start recipe to listen to the first step."
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
            title, speech_output, text_output, reprompt_text, should_end_session))


# Read a step in the recipe
def read_step(intent,session,index):

    steps = getStepsString(currentinstructions)
    session_attributes = {}
    if index > len(steps) or index < 1:
        title = "Invalid Command"
        speech_output = "Invalid step. Please try another command."
        text_output = "Invalid step. Please try another command."
        reprompt_text = "Please say a valid command."
        should_end_session = False
    else:
        change_current_step(index)
        title = "Step "+str(index)
        speech_output = "Step " + str(index) + ". " + steps[index-1]
        text_output = "Step " + str(index) + ". " + steps[index-1]
        reprompt_text = " "
        should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
            title, speech_output, text_output, reprompt_text, should_end_session))


# Read items that may need to be bought
def read_shopping_items(intent, session):
    shopping_items = shoppingCart(1, pantry)
    shopping_string = ""
    for item in shopping_items:
        shopping_string = shopping_string + item + ". "
    session_attributes = {}
    title = "Shopping"
    speech_output = "Based on the items you have removed from your pantry, you" \
                    "may need the following. " + shopping_string
    text_output = shopping_string
    reprompt_text = "Please say a valid command."
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
            title, speech_output, text_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()



# --------------

# Intent Handling

# --------------

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers

    if intent_name == "AMAZON.HelpIntent":
        return get_main_help_response(intent, session)
    elif intent_name == "ListMainHelpIntent":
        return get_main_help_response(intent, session)
    elif intent_name == "MainHelpSelectionIntent":
        return get_main_help_selection(intent, session)
    elif intent_name == "PantryHelpSelectionIntent":
        return get_pantry_help_selection(intent, session)
    elif intent_name == "SearchHelpSelectionIntent":
        return get_search_help_selection(intent, session)
    elif intent_name == "RecipeHelpSelectionIntent":
        return get_recipe_help_selection(intent, session)
    elif intent_name == "RemovePantryItemIntent":
        return remove_pantry_item(intent, session)
    elif intent_name == "AddPantryItemIntent":
        return add_pantry_item(intent, session)
    elif intent_name == "AcceptAddIntent":
        return accept_add(intent, session)
    elif intent_name == "ListPantryItemsIntent":
        return list_pantry_items(intent, session)
    elif intent_name == "FindRecipeIntent":
        return find_recipes(intent, session)
    elif intent_name == "RecommendRecipeIntent":
        return recommend_recipes(intent, session)
    elif intent_name == "ChooseRecipeIntent":
        return choose_recipe(intent, session)
    elif intent_name == "ListRecipesIntent":
        return list_recipes(intent, session)
    elif intent_name == "ListIngredientsIntent":
        return list_ingredients(intent, session)
    elif intent_name == "ListFirstStepIntent":
        return read_step(intent,session,1)
    elif intent_name == "ChooseStepIntent":
        return read_step(intent,session,int(intent['slots']['step_number']['value']))
    elif intent_name == "ListPreviousStepIntent":
        return read_step(intent,session,int(get_current_step())-1)
    elif intent_name == "ListNextStepIntent":
        return read_step(intent,session,int(get_current_step())+1)
    elif intent_name == "RepeatStepIntent":
        return read_step(intent,session,int(get_current_step()))
    elif intent_name == "ShoppingIntent":
        return read_shopping_items(intent,session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])

    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
