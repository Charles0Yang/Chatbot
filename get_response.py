import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

def pre_process_input(input):
    input_words = nltk.word_tokenize(input)
    input_words = [lemmatizer.lemmatize(word.lower()) for word in input_words]
    return input_words

def create_bag_of_words(input, words):
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
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(ints, intents_json):
    tag = ints[0]["intent"]
    print(tag)
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if(i["tag"] == tag):
            result = random.choice(i["responses"])
            break
    return result

def chatbot_response(input):
    intent_of_input = predict_class(input, model)
    response = get_response(intent_of_input, intents)
    print("Bonnie: {}".format(response))

def main():
    print("Welcome to the chatbot called Bonnie Bot!\nAll you need to do is type what you want to know and just type quit or exit to leave.")
    inp = input("You: ")
    leave = False
    while leave == False:
        chatbot_response(inp)
        inp = input("You: ")
        if inp == "quit" or inp == "exit":
            print("Sorry to see you go!")
            leave = True
main()

