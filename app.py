# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     11/15/2023
#
# Copyright 2023 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import json
import logging

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin

import utility as u
import functions_route as fn_r

from authlib.integrations.flask_oauth2 import ResourceProtector
from auth_decorator import Auth0JWTBearerTokenValidator


logging.basicConfig(
    filename="record.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s : %(message)s",
)

app = Flask(__name__)
CORS(app)

app.config.from_file("app_config.json", load=json.load)

for k in app.config:
    fn_r.app_settings[k] = app.config[k]

# auth
require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    fn_r.app_settings["API_DOMAIN"],
    fn_r.app_settings["API_IDENTIFIER"],
)
require_auth.register_token_validator(validator)


@app.route("/")
def root():
    return "Root URL '/' Not Supported<br/>"


#### RECIPE
# returns the entire list, and a separate list of { title, recipeId }
@app.route("/recipe/map/", methods=["GET", "OPTIONS"])
@cross_origin()
def recipe_GET_Map():
    return fn_r.recipe_GET_Map()


@app.route("/recipe/search/<keyword>/", methods=["GET", "OPTIONS"])
@cross_origin()
def recipe_GET_ListSearch(keyword):
    return fn_r.recipe_GET_ListSearch(keyword)


@app.route("/recipe/<recipeid>/", methods=["GET", "OPTIONS"])
@cross_origin()
def recipe_GET(recipeid):
    return fn_r.recipe_GET(recipeid)


@app.route("/recipe/<recipeid>/", methods=["DELETE", "OPTIONS"])
@cross_origin()
@require_auth("admin:all")
def recipe_DELETE(recipeid):
    return fn_r.recipe_DELETE(recipeid)


@app.route("/recipe/route/<routeurl>/", methods=["GET", "OPTIONS"])
@cross_origin()
def recipe_GET_ByRoute(routeurl):
    return fn_r.recipe_GET_ByRoute(routeurl)


@app.route("/recipe/", methods=["POST", "PUT", "OPTIONS"])
@cross_origin()
@require_auth("admin:all")
def recipe_PUT_POST():
    response = None
    if request.method == "PUT":
        # updates a recipe
        response = fn_r.recipe_PUT()
    elif request.method == "POST":
        # creates a recipe
        response = fn_r.recipe_POST()
    return response


#### CONTENT
# returns the entire list, titles and contentId only
@app.route("/content/", methods=["GET", "OPTIONS"])
@cross_origin()
def content_GET_List():
    return fn_r.content_GET_List()


# keyword search
@app.route("/content/search/<keyword>/", methods=["GET", "OPTIONS"])
@cross_origin()
def content_GET_ListSearch(keyword):
    return fn_r.content_GET_ListSearch(keyword)


# returns a specific content
@app.route("/content/<contentid>/", methods=["GET", "OPTIONS"])
@cross_origin()
def content_GET(contentid):
    return fn_r.content_GET(contentid)


# deletes a specific content
@app.route("/content/<contentid>/", methods=["DELETE", "OPTIONS"])
@cross_origin()
@require_auth("admin:all")
def content_DELETE(contentid):
    return fn_r.content_DELETE(contentid)


@app.route("/content/", methods=["POST", "PUT", "OPTIONS"])
@cross_origin()
@require_auth("admin:all")
def content_PUT_POST():
    response = None
    if request.method == "PUT":
        # updates a specific content
        response = fn_r.content_PUT()
    elif request.method == "POST":
        # creates a new content
        response = fn_r.content_POST()
    return response


#### RECIPE_CONTENT
# returns a recipe content relationship
@app.route("/recipecontent/<recipeid>/<contentid>/", methods=["GET", "OPTIONS"])
@cross_origin()
def recipecontent_GET(recipeid, contentid):
    return fn_r.recipeContent_GET(recipeid, contentid)


# deletes a recipe content relationship
@app.route("/recipecontent/<recipeid>/<contentid>/", methods=["DELETE", "OPTIONS"])
@cross_origin()
@require_auth("admin:all")
def recipecontent_DELETE(recipeid, contentid):
    return fn_r.recipeContent_DELETE(recipeid, contentid)


# creates or updates a recipe content relationship
@app.route("/recipecontent/", methods=["PUT", "POST", "OPTIONS"])
@cross_origin()
@require_auth("admin:all")
def recipecontent_PUT_POST():
    response = None
    if request.method == "PUT":
        # retrieves a specific relationship
        response = fn_r.recipeContent_PUT()
    elif request.method == "POST":
        # creates a  relationship
        response = fn_r.recipeContent_POST()
    return response


#### IMAGES
# retrieves a single image
@app.route("/image/<filename>/", methods=["GET", "OPTIONS"])
@cross_origin()
def image_GET(filename):
    return fn_r.image_GET("images", filename)


# retrieves a single thmbnail image
@app.route("/image/thumbnail/<filename>/", methods=["GET", "OPTIONS"])
@cross_origin()
def image_thumbnail_GET(filename):
    return fn_r.image_GET("images/thumbnails", filename)


#### ERROR HANDLER
@app.errorhandler(413)
def filesize_exceeded(e):
    return make_response(jsonify(message="File size exceeded the 16MB maximum"), 413)
