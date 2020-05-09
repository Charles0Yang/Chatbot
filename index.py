# -*- coding: utf-8 -*-
"""
Created on Wed May  6 19:32:38 2020

@author: teo hughes and charles yang
"""
from flask import Flask, render_template, request
import os
import get_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    print(get_response.chatbot_response("Hello"))
    #return str(get_response.chatbot_response(userText))

if __name__ == "__main__":
    app.run(debug=True)