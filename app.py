# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     11/2/2023
#
# Copyright 2023 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import json
import functions_route as fn_r
import utility as u
import logging

from datetime import datetime, date
from flask import Flask, request, make_response, jsonify
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


@app.route("/recipe/route/<routeurl>/", methods = ['GET', 'OPTIONS'])
@cross_origin()
def recipe_GET_ByRoute(routeurl):
    return fn_r.recipe_GET_ByRoute(routeurl)


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
    elif request.method == 'POST':
        # creates a new content
        response = fn_r.content_POST()
    return response


#### RECIPE_CONTENT
# retrives or deletes a recipe content relationship
@app.route("/recipecontent/<recipeid>/<contentid>/", methods=['GET', 'DELETE', 'OPTIONS'])
@cross_origin()
def recipecontent_GET_DELETE(recipeid, contentid):
    response = None
    if request.method == 'GET':
        # retrieves a specific reltionship
        response = fn_r.recipeContent_GET(recipeid, contentid)
    elif request.method == 'DELETE':
        # deletes a specific reltionship
        response = fn_r.recipeContent_DELETE(recipeid, contentid)
    return response


# creates or updates a recipe content relationship
@app.route("/recipecontent/", methods=['PUT', 'POST', 'OPTIONS'])
@cross_origin()
def recipecontent_PUT_POST():
    response = None
    if request.method == 'PUT':
        # retrieves a specific reltionship
        response = fn_r.recipeContent_PUT()
    elif request.method == 'POST':
        # deletes a specific reltionship
        response = fn_r.recipeContent_POST()
    return response



#### IMAGES
# retrieves a single image
@app.route("/image/<filename>/", methods = ['GET', 'OPTIONS'])
@cross_origin()
def image_GET(filename):
    return fn_r.image_GET('images', filename)


# retrieves a single thmbnail image
@app.route("/image/thumbnail/<filename>/", methods = ['GET', 'OPTIONS'])
@cross_origin()
def image_thumbnail_GET(filename):
    return fn_r.image_GET('images/thumbnails', filename)


# retrieves a single image
@app.route("/image/", methods = ['POST', 'OPTIONS'])
@cross_origin()
def image_POST():
    return fn_r.image_POST()



#### ERROR HANDLER
@app.errorhandler(413)
def filesize_exceeded(e):
    return make_response(jsonify(message='File size exceeded the 16MB maximum'), 413)