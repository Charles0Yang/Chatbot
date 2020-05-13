import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import numpy as np #ADDED AS NP
import tensorflow
import random
import json 
import pickle
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

words = []
classes = []
documents = []
ignore_words = ['?', '!']

#Creates a dictionary called intents
data_file = open('intents.json').read()
intents = json.loads(data_file)
    
#Pre-processing on text and intents via tokenisation
for intent in intents['intents']:
    #Goes through the patterns
    for pattern in intent['patterns']:
        #Tokenize patterns into word (split them into separate words)
        wrds = nltk.word_tokenize(pattern)
        #Basically like append
        words.extend(wrds)
        documents.append((wrds, intent['tag']))

        #Adds tags to classes
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

#Pre-processing on text and intents via lemmatization
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(classes)

#print (len(documents), "documents")
#print (len(classes), "classes", classes)
#print (len(words), "unique lemmatized words", words)


#Stores the words and classes
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))



#List for our training data
training = []
#Create an empty array for our output
output_empty = [0] * len(classes)

#Training set, bag of words for each sentence
for doc in documents:

    #List for our bag of words
    bag = []
    #List of tokenized words fot the pattern
    pattern_words = doc[0]
    #Lemmatize words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]


    #Create bag of words
    for w in words:
        if w in pattern_words:
            bag.append(1)
        else:
            bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])


#Shuffle and turn into np.array
random.shuffle(training)
training = np.array(training)

#Create train and test lists. X - patterns, Y - intents
train_x = list(training[:,0])
train_y = list(training[:,1])

#print("Training data created")



#Create AI model
model = Sequential()
model.add(Dense(128, input_shape = (len(train_x[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))

#Compile model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

#Fitting and saving the model
hist = model.fit(np.array(train_x), np.array(train_y), epochs = 1000, batch_size = 5, verbose = 1)
model.save("chatbot_model.h5", hist)

