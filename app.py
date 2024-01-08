# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     1/7/2024
#
# Copyright 2023 - 2024 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import json
import time

import global_utility as gu
import functions_content as fn_c
import functions_image as fn_i
import functions_recipe as fn_r
import functions_recipecontent as fn_rc

MODULE = "app module"

genericError = None


def parseEvent(event):
    util = gu.Global_Utility("misc")

    if not gu.isLocalDevelopment:
        util.writeEventDebug("EVENT", event)

    resourcePath = event["context"]["resource-path"]
    httpMethod = event["context"]["http-method"]
    pathParams = event["params"]["path"]
    requestBody = event["body-json"]

    methodNotSupportedException = gu.UptakeblueException(
        Exception(f"http-method {httpMethod} is not supported for {resourcePath}"),
        f"{MODULE}.parseEvent()",
    )

    source = f"{MODULE}, resourcePath={resourcePath}, method={httpMethod}"
    startTime = time.perf_counter()

    try:
        #### CONTENT
        if resourcePath == "/content/{contentid}":
            if httpMethod not in ["DELETE", "GET"]:
                raise methodNotSupportedException
            if httpMethod == "DELETE":
                response = fn_c.content_DELETE(util, pathParams)
                util.writeEventTiming("func", "fn_c.content_DELETE()", startTime)
            elif httpMethod == "GET":
                response = fn_c.content_GET(util, pathParams)
                util.writeEventTiming("func", "fn_c.content_GET()", startTime)

        elif resourcePath == "/content/search/{keyword}":
            if httpMethod not in ["GET"]:
                raise methodNotSupportedException
            response = fn_c.content_GET_ListSearch(util, pathParams)
            util.writeEventTiming("func", "fn_c.content_GET_ListSearch()", startTime)

        elif resourcePath == "/content":
            if httpMethod not in ["GET", "POST", "PUT"]:
                raise methodNotSupportedException
            if httpMethod == "GET":
                response = fn_c.content_GET_List(util)
                util.writeEventTiming("func", "fn_c.content_GET_List()", startTime)
            elif httpMethod == "POST":
                response = fn_c.content_POST(util, requestBody)
                util.writeEventTiming("func", "fn_c.content_POST()", startTime)
            elif httpMethod == "PUT":
                response = fn_c.content_PUT(util, requestBody)
                util.writeEventTiming("func", "fn_c.content_PUT()", startTime)

        #### IMAGE
        #### RECIPE
        elif resourcePath == "/recipe{recipeid}":
            if httpMethod not in ["DELETE", "GET"]:
                raise methodNotSupportedException
            if httpMethod == "DELETE":
                response = fn_r.recipe_DELETE(util, pathParams)
                util.writeEventTiming("func", "fn_c.content_DELETE()", startTime)
            elif httpMethod == "GET":
                response = fn_r.recipe_GET(util, pathParams)
                util.writeEventTiming("func", "fn_c.content_GET()", startTime)

        return response

    except gu.UptakeblueException as e:
        e.SourceAppend(source)
        genericError = e

    except Exception as e:
        genericError = gu.UptakeblueException(e, source=source)

    if genericError:
        print(genericError.Message)
        return gu.exceptionResponse(genericError)


# @app.route("/")
def root():
    return "Root URL '/' Not Supported<br/>"


#### RECIPE
# returns the entire list, and a separate list of { title, recipeId }
# @app.route("/recipe/map/", methods=["GET", "OPTIONS"])
# @cross_origin()
def recipe_GET_Map():
    return fn_r.recipe_GET_Map()


# @app.route("/recipe/search/<keyword>/", methods=["GET", "OPTIONS"])
# @cross_origin()
def recipe_GET_ListSearch(keyword):
    return fn_r.recipe_GET_ListSearch(keyword)


# @app.route("/recipe/<recipeid>/", methods=["GET", "OPTIONS"])
# @cross_origin()
def recipe_GET(recipeid):
    return fn_r.recipe_GET(recipeid)


# @app.route("/recipe/<recipeid>/", methods=["DELETE", "OPTIONS"])
# @cross_origin()
# @require_auth("admin:all")
def recipe_DELETE(recipeid):
    return fn_r.recipe_DELETE(recipeid)


# @app.route("/recipe/route/<routeurl>/", methods=["GET", "OPTIONS"])
# @cross_origin()
def recipe_GET_ByRoute(routeurl):
    return fn_r.recipe_GET_ByRoute(routeurl)


# @app.route("/recipe/", methods=["POST", "PUT", "OPTIONS"])
# @cross_origin()
# @require_auth("admin:all")
def recipe_PUT_POST():
    response = None
    # if request.method == "PUT":
    #     # updates a recipe
    #     response = fn_r.recipe_PUT()
    # elif request.method == "POST":
    #     # creates a recipe
    #     response = fn_r.recipe_POST()
    return response


#### CONTENT
# returns the entire list, titles and contentId only
# @app.route("/content/", methods=["GET", "OPTIONS"])
# @cross_origin()
def content_GET_List():
    return fn_r.content_GET_List()


# keyword search
# @app.route("/content/search/<keyword>/", methods=["GET", "OPTIONS"])
# @cross_origin()
def content_GET_ListSearch(keyword):
    return fn_r.content_GET_ListSearch(keyword)


# returns a specific content
# @app.route("/content/<contentid>/", methods=["GET", "OPTIONS"])
# @cross_origin()
# def content_GET(contentid):
#     return fn_r.content_GET(contentid)


# deletes a specific content
# @app.route("/content/<contentid>/", methods=["DELETE", "OPTIONS"])
# @cross_origin()
# @require_auth("admin:all")
# def content_DELETE(contentid):
#     return fn_r.content_DELETE(contentid)


# @app.route("/content/", methods=["POST", "PUT", "OPTIONS"])
# @cross_origin()
# @require_auth("admin:all")
def content_PUT_POST():
    response = None
    # if request.method == "PUT":
    #     # updates a specific content
    #     response = fn_r.content_PUT()
    # elif request.method == "POST":
    #     # creates a new content
    #     response = fn_r.content_POST()
    return response


#### RECIPE_CONTENT
# returns a recipe content relationship
# @app.route("/recipecontent/<recipeid>/<contentid>/", methods=["GET", "OPTIONS"])
# @cross_origin()
def recipecontent_GET(recipeid, contentid):
    return fn_r.recipeContent_GET(recipeid, contentid)


# deletes a recipe content relationship
# @app.route("/recipecontent/<recipeid>/<contentid>/", methods=["DELETE", "OPTIONS"])
# @cross_origin()
# @require_auth("admin:all")
def recipecontent_DELETE(recipeid, contentid):
    return fn_r.recipeContent_DELETE(recipeid, contentid)


# creates or updates a recipe content relationship
# @app.route("/recipecontent/", methods=["PUT", "POST", "OPTIONS"])
# @cross_origin()
# @require_auth("admin:all")
def recipecontent_PUT_POST():
    response = None
    # if request.method == "PUT":
    #     # retrieves a specific relationship
    #     response = fn_r.recipeContent_PUT()
    # elif request.method == "POST":
    #     # creates a  relationship
    #     response = fn_r.recipeContent_POST()
    return response


#### IMAGES
# retrieves a single image
# @app.route("/image/<filename>/", methods=["GET", "OPTIONS"])
# @cross_origin()
def image_GET(filename):
    return fn_r.image_GET("images", filename)


# retrieves a single thmbnail image
# @app.route("/image/thumbnail/<filename>/", methods=["GET", "OPTIONS"])
# @cross_origin()
def image_thumbnail_GET(filename):
    return fn_r.image_GET("images/thumbnails", filename)


#### ERROR HANDLER
# @app.errorhandler(413)
# def filesize_exceeded(e):
#     return make_response(jsonify(message="File size exceeded the 16MB maximum"), 413)
