# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     10/9/2023
#
# Copyright 2023 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import json
import functions_route as fn_r
import utility as u
import logging

from datetime import datetime, date
from flask import Flask, request
from flask_cors import CORS, cross_origin

logging.basicConfig(
    filename="record.log", 
    level=logging.DEBUG, 
    format="%(asctime)s %(levelname)s : %(message)s"
    )

app = Flask(__name__)
CORS(app)

app.config.from_file("app_config.json", load=json.load)

for k in app.config:
    fn_r.app_settings[k] = app.config[k]


@app.route("/")
def root():
    return "Root URL '/' Not Supported<br/>"

@app.route("/recipe/map", methods = ['GET', 'OPTIONS'])
@cross_origin()
def recipe_GET_Map():
    return fn_r.recipe_GET_Map()  

@app.route("/recipe/<recipeid>/", methods = ['GET', 'DELETE', 'OPTIONS'])
@cross_origin()
def recipe_GET(recipeid):
    return fn_r.recipe_GET(recipeid)
