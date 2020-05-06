# -*- coding: utf-8 -*-
"""
Created on Wed May  6 19:32:38 2020

@author: charl
"""
from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/home')
def index():
    return render_template('index.html')

