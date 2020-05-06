import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import numpy
import tflearn
import tensorflow
import random
import json 
import pickle
import numpy
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

words = []
classes = []
documents = []
ignore_words = ['?', '!']

with open("intents.json") as file:
    intents = json.load(file)
    
#Pre-processing on text and intents via tokenisation
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word = nltk.word_tokenize(pattern)
        words.extend(word)
        documents.append((word, intent['tag']))
        
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

#Pre-processing on text and intents via lemmatization
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))
