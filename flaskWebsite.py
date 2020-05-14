# -*- coding: utf-8 -*-
"""
Created on Wed May  6 19:32:38 2020

@author: teo hughes and charles yang
"""
from flask import Flask, render_template, request
import os
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import pickle
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.backend import set_session

#Setting the session for keras - must do this before loading the model
sess = tf.Session()
graph = tf.get_default_graph()
set_session(sess)

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))


app = Flask(__name__, template_folder='templates', static_folder='statics')


def pre_process_input(input):
    #Takes the input and pre-processes it via tokenization and lemmatization 
    input_words = nltk.word_tokenize(input)
    input_words = [lemmatizer.lemmatize(word.lower()) for word in input_words]
    return input_words

def create_bag_of_words(input, words):
    #Adds processed words to a bag of words
    input_words = pre_process_input(input)
    bag = [0] * len(words)
    for s in input_words:
        for i, w in enumerate(words):
            if w == s: 
                bag[i] = 1
    return(np.array(bag))

def predict_class(input, model):
    p = create_bag_of_words(input, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25 #Percentage above which will be registered as an intent to be responded to
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True) #Sorts the results so that the highest probability intent will be responded to
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])}) #Adds the class of the intent and the probability to the return list from which a response will be generated
    return return_list

def get_response(ints, intents_json):
    tag = ints[0]["intent"] #Gets the name of the tag of the intent which the user input belongs to
    list_of_intents = intents_json["intents"] #List of all intents 
    min_accuracy = 0.9993 #Probability above which the response should be valid. If below this number then bot should reply "Sorry I don't understand what you said"
    result = ""
    for i in list_of_intents:
        if(i["tag"] == tag): #If the intent of the user input matches the intent
            print(float(ints[0]["probability"])) #Print statement to check the certainty of the model of the user's input. Use to error check
            if float(ints[0]["probability"]) > min_accuracy and "long" not in tag: #The model's probability of the response being valid must be above the min_accuracy otherwise the response may be invalid
                result = random.choice(i["responses"]) #Picks a random response from the list of responses in the intent of the user message
                break
            elif float(ints[0]["probability"]) > min_accuracy and "long" in tag:
                result = i["responses"]
                break
            else:
                result = "Sorry I don't understand what you said" #Returns generic "I don't understand message instead of a listed response
                break
    return result

def chatbot_response(input):
    response_list = []
    intent_of_input = predict_class(input, model) #Gets the intent of the user input
    response = get_response(intent_of_input, intents) #Gets a random response based off the intent of the user input
    if "long" not in intent_of_input[0]["intent"]:
        formatted_response = str(("{}".format(response)))
        response_list.append(formatted_response)
    else:
        for sentence in response:
            response_list.append(sentence)
    return str(response_list)



@app.route('/') #Home page
def index():
    return render_template("template.html") #Creates the page with the html from index.html

@app.route("/get") #Way of getting bot response - no HTML and isn't viewed by the user 
def get_bot_response():
    global graph
    global sess
    with graph.as_default(): #Important for the model to be generated and utilised correctly
        set_session(sess) 
        userText = request.args.get('msg') #Gets the user input from the textbox
        return chatbot_response(userText) #Returns the appropriate response to the user's input to be used in the javascript file so that the bot's response can be displayed

            

if __name__ == "__main__":
    app.run(debug=True) 