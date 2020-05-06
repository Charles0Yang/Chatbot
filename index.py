# -*- coding: utf-8 -*-
"""
Created on Wed May  6 19:32:38 2020

@author: teo hughes and charles yang
"""
#TESTING out flask
from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
