# Bot.py is the python code for the actual chatbot's neural network

# Importing libraries we will need for later
import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import numpy as np
import tensorflow
import random
import json 
import pickle
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD


# Creating lists that will be filled with the data from intents
words = [] # Adds the words of the questions
classes = [] # Adds the tags of the questions
documents = [] # Adds the words of a question and it's tag in a 2D array
ignore_words = ['?', '!']


# Creates a dictionary called intents
data_file = open('intents.json').read()
intents = json.loads(data_file)


# Pre-processing on text and intents via tokenisation
for intent in intents['intents']:
    # Goes through the patterns
    for pattern in intent['patterns']:
        # Tokenize patterns into word (split them into separate words)
        wrds = nltk.word_tokenize(pattern)
        # Basically like append
        words.extend(wrds)
        documents.append((wrds, intent['tag']))

        # Adds tags to classes
        if intent['tag'] not in classes:
            classes.append(intent['tag'])


# Pre-processing on text and intents via lemmatization
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words] # lemmatizes lower of words if it is not in ignore_words
words = sorted(list(set(words))) # Removes duplicates (set), makes it a list and sorts it
classes = sorted(classes) # Sorts the tags


# Stores the words and classes in pickle for later use in flaskWebsite.py
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))



# Creates training data



# List for our training data
training = []
# Create an empty array full of 0s for our output based on how many tags there are
output_empty = [0] * len(classes)

# For every question and it's tag
for doc in documents:

    # List for our bag of words
    bag = []
    # List of tokenized words for the pattern
    pattern_words = doc[0]
    # Lemmatize words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]


    # Create bag of words
    for w in words:

        # Adds a 0 or a 1 to the bag if the word in words is in pattern_words
        if w in pattern_words:
            bag.append(1)
        else:
            bag.append(0)

    # Basically now the bag list is a list of 0s and 1s the length of the list words where it is a 1 if the word is in the question

    # Creates an output row of 0s representing the tags but there is a 1 where it is the tag that is being used
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    # Adds the bag of words saying which words are in the question and the output_row which says which tag it is
    training.append([bag, output_row])


# Shuffle and turn into an np.array
random.shuffle(training)
training = np.array(training)


# Create train and test lists. X - "bag of words", Y - "bag of classes"
train_x = list(training[:,0])
train_y = list(training[:,1])




# Create AI model (Neural Network)


model = Sequential()
# Adds an input layer to the neural network with how many neurons there are words
model.add(Dense(128, input_shape = (len(train_x[0]),), activation="relu"))
# Randomly selects 50% of the neurons not to be used when training
model.add(Dropout(0.5))
# Adds a hidden layer
model.add(Dense(64, activation="relu"))
# Same as above
model.add(Dropout(0.5))
# Adds an ouput layer with how many neurons there are tags
model.add(Dense(len(train_y[0]), activation="softmax"))




# Compiles the model


# Sets the optimizer
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
# Compiles the model with the sgd optimizer
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

# Fitting and saving the model
hist = model.fit(np.array(train_x), np.array(train_y), epochs = 200, batch_size = 5, verbose = 1)

# Saves the model to the chatbot_model.h5 file
model.save("chatbot_model.h5", hist)

