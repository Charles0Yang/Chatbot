# -*- coding: utf-8 -*-
"""
Created on Wed May  6 19:32:38 2020

@authors: teo hughes and charles yang
"""

# Imports necessary libraries we need
from flask import Flask, render_template, request, flash
import os
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

from forms import ContactForm
from flask_mail import Message, Mail

import json
import random
import requests
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.backend import set_session


# Setting the session for keras - must do this before loading the model
sess = tf.Session()
graph = tf.get_default_graph()
set_session(sess)


# Loads the model from the file
from keras.models import load_model
model = load_model('chatbot_model.h5')

# Loads the intents, words and classes
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))


# Creates a mail
mail = Mail()

# Creates an app connecting to the templates and statics folder
app = Flask(__name__, template_folder='templates', static_folder='statics')

# Create the app key
app.secret_key = 'development key'


# Configurates app so you can send emails in the website
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'bonniebot77@gmail.com'
app.config["MAIL_PASSWORD"] = 'Chelseabest'
 
# Initializes the app in the mail variable
mail.init_app(app)

# Gets the live covid cases in cities in UK data and turn it into a json file
#LOCATIONS_URL = "https://api.covid19uk.live/"
#data = requests.get(LOCATIONS_URL)
#data_json = data.json()


# Gets the live covid cases in countries and turn it into a json file
#COUNTRIES_URL = "https://corona.lmao.ninja/v2/countries"
#country_data = requests.get(COUNTRIES_URL)
#country_data_json = country_data.json()


# Lists of possible locations and countries
locations = ['barking and dagenham', 'barnet', 'barnsley', 'bath and north east somerset', 'bedford', 'bexley', 'birmingham', 'blackburn with darwen', 'blackpool', 'bolton', 'bournemouth, christchurch and poole', 'bracknell forest', 'bradford', 'brent', 'brighton and hove', 'bristol, city of', 'bromley', 'buckinghamshire', 'bury', 'calderdale', 'cambridgeshire', 'camden', 'central bedfordshire', 'cheshire east', 'cheshire west and chester', 'city of london', 'cornwall and isles of scilly', 'county durham', 'coventry', 'croydon', 'cumbria', 'darlington', 'derby', 'derbyshire', 'devon', 'doncaster', 'dorset', 'dudley', 'ealing', 'east riding of yorkshire', 'east sussex', 'enfield', 'essex', 'gateshead', 'gloucestershire', 'greenwich', 'hackney', 'halton', 'hammersmith and fulham', 'hampshire', 'haringey', 'harrow', 'hartlepool', 'havering', 'herefordshire, county of', 'hertfordshire', 'hillingdon', 'hounslow', 'isle of wight', 'islington', 'kensington and chelsea', 'kent', 'kingston upon hull, city of', 'kingston upon thames', 'kirklees', 'knowsley', 'lambeth', 'lancashire', 'leeds', 'leicester', 'leicestershire', 'lewisham', 'lincolnshire', 'liverpool', 'luton', 'manchester', 'medway', 'merton', 'middlesbrough', 'milton keynes', 'newcastle upon tyne', 'newham', 'norfolk', 'north east lincolnshire', 'north lincolnshire', 'north somerset', 'north tyneside', 'north yorkshire', 'northamptonshire', 'northumberland', 'nottingham', 'nottinghamshire', 'oldham', 'oxfordshire', 'peterborough', 'plymouth', 'portsmouth', 'reading', 'redbridge', 'redcar and cleveland', 'richmond upon thames', 'rochdale', 'rotherham', 'rutland', 'salford', 'sandwell', 'sefton', 'sheffield', 'shropshire', 'slough', 'solihull', 'somerset', 'south gloucestershire', 'south tyneside', 'southampton', 'southend-on-sea', 'southwark', 'st. helens', 'staffordshire', 'stockport', 'stockton-on-tees', 'stoke-on-trent', 'suffolk', 'sunderland', 'surrey', 'sutton', 'swindon', 'tameside', 'telford and wrekin', 'thurrock', 'torbay', 'tower hamlets', 'trafford', 'wakefield', 'walsall', 'waltham forest', 'wandsworth', 'warrington', 'warwickshire', 'west berkshire', 'west sussex', 'westminster', 'wigan', 'wiltshire', 'windsor and maidenhead', 'wirral', 'wokingham', 'wolverhampton', 'worcestershire', 'york', 'ayrshire and arran', 'borders', 'dumfries and galloway', 'fife', 'forth valley', 'grampian', 'greater glasgow and clyde', 'highland', 'lanarkshire', 'lothian', 'orkney', 'shetland', 'tayside', 'eileanan siar (western isles)', 'golden jubilee national hospital', 'wales', 'northern ireland']
countries = ['afghanistan', 'albania', 'algeria', 'andorra', 'angola', 'anguilla', 'antigua and barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia', 'bosnia', 'botswana', 'brazil', 'british virgin islands', 'brunei', 'bulgaria', 'burkina faso', 'burundi', 'cabo verde', 'cambodia', 'cameroon', 'canada', 'caribbean netherlands', 'cayman islands', 'central african republic', 'chad', 'channel islands', 'chile', 'china', 'colombia', 'comoros', 'congo', 'costa rica', 'croatia', 'cuba', 'curaçao', 'cyprus', 'czechia', "côte d'ivoire", 'drc', 'denmark', 'diamond princess', 'djibouti', 'dominica', 'dominican republic', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'ethiopia', 'falkland islands (malvinas)', 'faroe islands', 'fiji', 'finland', 'france', 'french guiana', 'french polynesia', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada', 'guadeloupe', 'guatemala', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'holy see (vatican city state)', 'honduras', 'hong kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'isle of man', 'israel', 'italy', 'jamaica', 'japan', 'jordan', 'kazakhstan', 'kenya', 'kuwait', 'kyrgyzstan', "lao people's democratic republic", 'latvia', 'lebanon', 'lesotho', 'liberia', 'libyan arab jamahiriya', 'liechtenstein', 'lithuania', 'luxembourg', 'ms zaandam', 'macao', 'macedonia', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'martinique', 'mauritania', 'mauritius', 'mayotte', 'mexico', 'moldova', 'monaco', 'mongolia', 'montenegro', 'montserrat', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nepal', 'netherlands', 'new caledonia', 'new zealand', 'nicaragua', 'niger', 'nigeria', 'norway', 'oman', 'pakistan', 'palestine', 'panama', 'papua new guinea', 'paraguay', 'peru', 'philippines', 'poland', 'portugal', 'qatar', 'romania', 'russia', 'rwanda', 'réunion', 's. korea', 'saint kitts and nevis', 'saint lucia', 'saint martin', 'saint pierre miquelon', 'saint vincent and the grenadines', 'san marino', 'sao tome and principe', 'saudi arabia', 'senegal', 'serbia', 'seychelles', 'sierra leone', 'singapore', 'sint maarten', 'slovakia', 'slovenia', 'somalia', 'south africa', 'south sudan', 'spain', 'sri lanka', 'st. barth', 'sudan', 'suriname', 'swaziland', 'sweden', 'switzerland', 'syrian arab republic', 'taiwan', 'tajikistan', 'tanzania', 'thailand', 'timor-leste', 'togo', 'trinidad and tobago', 'tunisia', 'turkey', 'turks and caicos islands', 'uae', 'uk', 'usa', 'uganda', 'ukraine', 'uruguay', 'uzbekistan', 'venezuela', 'vietnam', 'western sahara', 'yemen', 'zambia', 'zimbabwe']


# Function that fetches recent cases of cities in UK
def fetch_recent_cases(user_location):

    areas_object = json.loads(data_json['data'][0]['area']) # Turns the string in the api to json so that each area can be accessed
    for areas in areas_object: # For each valid location in the api check whether the location is the same as the location the user inputted
        if user_location.lower() == areas['location'].lower(): # Checks whether the no-caps version of the user input is the same as one of the locations from the api
            return "There are {} cases in {}".format(areas['number'], areas['location']) # If it is return the number of cases in the area


# Function that fetches recent cases of countries around the world
def fetch_country_cases(country):

    cases = -1 # Set to impossible number of cases so we can see if the number has been updated or not
    country_found = "" # The country that the user is searching for
    for c in country_data_json: # For each country that the api supports go through and check whether the name inputted by the user is the same
        if country == (c['country']).lower(): # If the lowercase versions of both input and api name are the same 
            cases = c['cases'] # Set the number of cases to the cases that the API returns
            country_found = c['country'] # Set country_found as the country from the API so the country is outputted with a capital letter instead of all lowercase
    if cases == -1: # If cases hasn't been updated
        return ("No data found about {}".format(country)) # Return that no data isn't found. Shouldn't be returned as if country isn't supported by API earlier error message should be displayed
    else:
        return ("There are {} cases in {}".format(cases, country_found)) # Returns the number of cases in the country in an appropriate format



# Function that checks if their is a city name in the input
def contains_location(input):

    returned_location = "" # Location we want to find cases for 
    words = input 
    for location in locations: # For each location in the locations array
        if location in words: # If the location is in the input somewhere
            returned_location = location # Set the location we want to find cases for as the location found in the input
            break
    return returned_location


# Function that checks if their is a country name in the input
def contains_country(input): 

    returned_country = "" # Country we want to find cases for
    words = input
    for country in countries: # For each country in the countries array
        if country in words: # If the country is in the input somewhere
            returned_country = country # Set the country we want to find cases for as the country found in the input
            break
    return returned_country



# Function that takes the input and pre-processes it via tokenization and lemmatization 
def pre_process_input(input):

    input_words = nltk.word_tokenize(input)
    input_words = [lemmatizer.lemmatize(word.lower()) for word in input_words]
    return input_words


# Function that adds processed words to a bag of words   
def create_bag_of_words(input, words):
    
    # Preprocess the input
    input_words = pre_process_input(input)
    # Creates a bag of words
    bag = [0] * len(words)

    # For loop that changes the bag of words index to 1 if it is in words
    for s in input_words:
        for i, w in enumerate(words):
            if w == s: 
                bag[i] = 1

    # Returns the bag of words as an np.array
    return(np.array(bag))


# Function that predicts the tag (class) of the question
def predict_class(input, model):

    p = create_bag_of_words(input, words) # Creates a bag of words and calls it p
    res = model.predict(np.array([p]))[0] # Generates a list containing each response and the probability of the response
    ERROR_THRESHOLD = 0.25 # Percentage above which will be registered as an intent to be responded to
    
    results = [[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD] # Creates a results list with all results above the Error Threshold
    results.sort(key=lambda x: x[1], reverse=True) # Sorts the results so that the highest probability intent will be responded to
    
    return_list = []
    for r in results: # For all the results
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])}) # Adds the class of the intent and the probability to the return list from which a response will be generated
    
    return return_list



# Function that gets the response
def get_response(ints, intents_json):

    tag = ints[0]["intent"] # Gets the name of the tag of the intent which the user input belongs to
    list_of_intents = intents_json["intents"] # List of all intents 
    min_accuracy = 0.99 # Probability above which the response should be valid. If below this number then bot should reply "Sorry I don't understand what you said"
    
    result = ""
    for i in list_of_intents: # For every intent

        if(i["tag"] == tag): # If the intent of the user input matches the intent

            print(float(ints[0]["probability"])) # Print statement to check the certainty of the model of the user's input. Use to error check
            
            if float(ints[0]["probability"]) > min_accuracy and "long" not in tag: # The model's probability of the response being valid must be above the min_accuracy otherwise the response may be invalid and if it is not a long answer   
  
                    result = random.choice(i["responses"]) # Picks a random response from the list of responses in the intent of the user message
                    break
            
            elif float(ints[0]["probability"]) > min_accuracy and "long" in tag: # For responses with long in the tag, the response will be several lines long so all responses need to be returned so all can be displayed on screen. These are usually very specific questions that have a long response
                
                result = i["responses"] # Returns all the responses in the tag 
                break
            
            else: # If the question isn't understood
            
                # Returns a random response saying I don't understand
                rand = random.randint(0, 2)
                if rand == 0:
                    result = "Sorry I don't understand what you said!"
                elif rand == 1:
                    result = "Sorry I didn't quite get that!"
                else:
                    result = "Sorry I haven't been programmed to answer that question yet!"
                break
    
    return result



# Function that gets the chatbot response
def chatbot_response(input):

    response_list = []
    intent_of_input = predict_class(input, model) # Gets the intent of the user input
    response = get_response(intent_of_input, intents) # Gets a response based off the intent of the user input
    
    #if contains_location(input.lower()) != "":  # Checks whether the input is a location so the correct response can be displayed
        #response_list.append(fetch_recent_cases(contains_location(input.lower()))) # Adds the correct statement if the location is valid and the api contains a number of cases for that area
    
    #elif contains_country(input.lower()) != "": # Checks whether the input is a country so the correct response can be displayed
        #response_list.append(fetch_country_cases(contains_country(input.lower()))) # Adds the correct statement if the country is valid and the api contains a number of cases for that country
    
    if True: # If there is no country or city name in the input

        if "long" not in intent_of_input[0]["intent"]: # If long is not in the intent of the input there is need to add several sentences
            formatted_response = str(("{}".format(response))) # Creates the response
            response_list.append(formatted_response) # Adds the response to the response_list
        
        else: # If it is a long response

            # If the response is an error message it only prints once
            if response == "Sorry I don't understand what you said!" or response == "Sorry I didn't quite get that!" or response == "Sorry I haven't been programmed to answer that question yet!": # Prevents "Sorry I don't understand" from being displayed character by character
                response_list.append(response) # Adds the response to the response_list
            
            else:
                for sentence in response: # If the tag is recognised and long is in the intent, then all the sentences need to returned in the response
                    response_list.append(sentence) # Adds each sentence to the response list separetly
    
    return str(response_list) # Since a list is not allowed to be returned, a string version is returned which can then be converted to a list in javascript



@app.route('/') # Home page
def index():
    return render_template("template.html") # Creates the page with the html from template.html

@app.route("/get") # Way of getting bot response - no HTML and isn't viewed by the user 
def get_bot_response():

    global graph
    global sess
    with graph.as_default(): # Important for the model to be generated and utilised correctly
        set_session(sess) # Sets the session
        userText = request.args.get('msg') # Gets the user input from the textbox
        return chatbot_response(userText) # Returns the appropriate response to the user's input to be used in the javascript file so that the bot's response can be displayed

            
@app.route("/locations") # Location page
def locationsSupported():
    return render_template("locationsSupported.html") # Creates the page with the html from locationsSupported.html


@app.route("/feedback", methods=['GET', 'POST']) # Feedback page
def getFeedback():

    form = ContactForm() # Creates a new form object from the class declared in forms.py
    if request.method == "POST": # If the send button is pressed

        if form.validate() == False: # If all the fields haven't been filled in

            flash('Please complete all fields.') # Displays a pop-up error message
            return render_template("getFeedback.html", form=form) # Returns the same HTML as all fields haven't been filled in

        else: # If the form is valid

            msg = Message(form.subject.data, sender='contact@example.com', recipients=['bonniebot77@gmail.com']) # Creates the message
            msg.body = """ 
            From: %s <%s> 
            %s
            """ % (form.name.data, form.email.data, form.message.data) # Formats the message data in an easily readable format
            mail.send(msg) # Sends the message to bonniebot77@gmail.com

            return render_template('getFeedback.html', success=True) # Displays the page again but returns success as true so that a thank you message can appear

    else:
        return render_template("getFeedback.html", form=form) # If the send button hasn't been pressed, loads the page


@app.route("/about") # About page
def about():
    return render_template("about.html") # Creates the page with the html from about.html


@app.route("/howtouse") # How to use page
def howtouse():
    return render_template("howto.html") # Creates the page with the html from howto.html
    


if __name__ == "__main__": # If this is the file being run
    app.run(debug=True) # Runs the app