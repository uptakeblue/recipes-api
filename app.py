# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     1/8/2024
#
# Copyright 2023 - 2024 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import json
import time

import global_utility as gu
import functions_content as fn_c

# import functions_image as fn_i
import functions_recipe as fn_r
import functions_recipecontent as fn_rc

MODULE = "app module"

genericError = None


def parseEvent(event):
    util = gu.Global_Utility("recipes")

    if not gu.isLocalDevelopment:
        util.writeEventDebug("EVENT", event)

    resourcePath = None
    httpMethod = None
    requestBody = None
    pathParams = None
    if "context" in event:
        resourcePath = event["context"]["resource-path"]
        httpMethod = event["context"]["http-method"]
        requestBody = event["body-json"]
        pathParams = event["params"]["path"]
    else:
        resourcePath = event["resource"]
        httpMethod = event["httpMethod"]
        requestBody = event["body"]
        contentTypeHeader = event["headers"]["Content-Type"]

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
        elif resourcePath == "/recipe/{recipeid}":
            if httpMethod not in ["DELETE", "GET"]:
                raise methodNotSupportedException
            if httpMethod == "DELETE":
                response = fn_r.recipe_DELETE(util, pathParams)
                util.writeEventTiming("func", "fn_c.content_DELETE()", startTime)
            elif httpMethod == "GET":
                response = fn_r.recipe_GET(util, pathParams)
                util.writeEventTiming("func", "fn_c.content_GET()", startTime)

        elif resourcePath == "/recipe":
            if httpMethod not in ["POST", "PUT"]:
                raise methodNotSupportedException
            if httpMethod == "POST":
                response = fn_r.recipe_POST_multipartFormdata(
                    util,
                    requestBody,
                    contentTypeHeader,
                )
                util.writeEventTiming(
                    "func", "fn_r.recipe_POST_multipartFormdata()", startTime
                )
                # response = fn_r.recipe_POST(util, requestBody)
                # util.writeEventTiming("func", "fn_r.recipe_POST()", startTime)
            elif httpMethod == "PUT":
                response = fn_r.recipe_PUT(util, requestBody)
                util.writeEventTiming("func", "fn_r.recipe_PUT()", startTime)

        elif resourcePath == "/recipe/map":
            if httpMethod not in ["GET"]:
                raise methodNotSupportedException
            response = fn_r.recipe_GET_ListMap(util)
            util.writeEventTiming("func", "fn_r.recipe_GET_ListMap()", startTime)

        elif resourcePath == "/recipe/route/{routeurl}":
            if httpMethod not in ["GET"]:
                raise methodNotSupportedException
            response = fn_r.recipe_GET_ByRoute(util, pathParams)
            util.writeEventTiming("func", "fn_r.recipe_GET_ByRoute()", startTime)

        elif resourcePath == "/recipe/search/{keyword}":
            if httpMethod not in ["GET"]:
                raise methodNotSupportedException
            response = fn_r.recipe_GET_ListSearch(util, pathParams)
            util.writeEventTiming("func", "fn_r.recipe_GET_ListSearch()", startTime)

        #### RECIPE
        elif resourcePath == "/recipecontent":
            if httpMethod not in ["POST", "PUT"]:
                raise methodNotSupportedException
            if httpMethod == "POST":
                response = fn_rc.recipeContent_POST(util, requestBody)
                util.writeEventTiming("func", "fn_rc.recipeContent_POST()", startTime)
            elif httpMethod == "PUT":
                response = fn_rc.recipeContent_PUT(util, requestBody)
                util.writeEventTiming("func", "fn_rc.recipeContent_PUT()", startTime)

        elif resourcePath == "/recipecontent":
            if httpMethod not in ["DELETE", "GET"]:
                raise methodNotSupportedException
            if httpMethod == "DELETE":
                response = fn_rc.recipeContent_DELETE(util, pathParams)
                util.writeEventTiming("func", "fn_rc.recipeContent_DELETE()", startTime)
            elif httpMethod == "GET":
                response = fn_rc.recipeContent_GET(util, pathParams)
                util.writeEventTiming("func", "fn_rc.recipeContent_GET()", startTime)

        else:
            raise gu.UptakeblueException(
                Exception(f"Resource path {resourcePath} does not exist"),
                f"{MODULE}.parseEvent()",
            )

        return response

    except gu.UptakeblueException as e:
        e.SourceAppend(source)
        genericError = e

    except Exception as e:
        genericError = gu.UptakeblueException(e, source=source)

    if genericError:
        print(genericError.Message)
        return gu.exceptionResponse(genericError)
