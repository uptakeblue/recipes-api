# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     10/11/2023
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



#### RECIPE
# returns the entire list, and a separate list of { title, recipeId }
@app.route("/recipe/map/", methods = ['GET', 'OPTIONS'])
@cross_origin()
def recipe_GET_Map():
    return fn_r.recipe_GET_Map()  


@app.route("/recipe/search/<keyword>/", methods = ['GET', 'OPTIONS'])
@cross_origin()
def recipe_GET_ListSearch(keyword):
    return fn_r.recipe_GET_ListSearch(keyword)


@app.route("/recipe/<recipeid>/", methods = ['GET', 'DELETE', 'OPTIONS'])
@cross_origin()
def recipe_GET_DELETE(recipeid):
    response = None
    if request.method == 'GET':
        # returns a specific recipe
        response = fn_r.recipe_GET(recipeid)
    elif request.method == 'DELETE':
        # deletes a specific recipe
        response = fn_r.recipe_DELETE(recipeid)
    return response


@app.route("/recipe/", methods=['POST', 'PUT', 'OPTIONS'])
@cross_origin()
def recipe_PUT_POST():
    response = None
    if request.method == 'PUT':
        # updates a recipe
        response = fn_r.recipe_PUT()
    elif request.method == 'POST':
        # creates a recipe
        response = fn_r.recipe_POST()
    return response



#### CONTENT
# returns the entire list, titles and contentId only
@app.route("/content/", methods=['GET', 'OPTIONS'])
@cross_origin()
def content_GET_List():
    return fn_r.content_GET_List()


# keyword search
@app.route("/content/search/<keyword>/", methods=['GET', 'OPTIONS'])
@cross_origin()
def content_GET_ListSearch(keyword):
    return fn_r.content_GET_ListSearch(keyword)


# returns a specific content
@app.route("/content/<contentid>/", methods=['GET', 'DELETE', 'OPTIONS'])
@cross_origin()
def content_GET_DELETE(contentid):
    response = None
    if request.method == 'GET':
        # returns a specific content
        response = fn_r.content_GET(contentid)
    elif request.method == 'DELETE':
        # deletes a specific content
        response = fn_r.content_DELETE(contentid)

    return response

@app.route("/content/", methods=['POST', 'PUT', 'OPTIONS'])
@cross_origin()
def content_PUT_POST():
    response = None
    if request.method == 'PUT':
        # updates a specific content
        response = fn_r.content_PUT()
        pass
    elif request.method == 'POST':
        # creates a new content
        response = fn_r.content_POST()
        pass
    return response


