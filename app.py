# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     2/1/2024
#
# Copyright 2023 - 2024 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import time
import urllib.parse

import global_utility as gu
import functions_content as fn_c

import functions_image as fn_i
import functions_recipe as fn_r
import functions_recipecontent as fn_rc
import functions_misc as fn_m

MODULE = "app module"

genericError = None


def parseEvent(event):
    util = gu.Global_Utility("recipes")

    if (
        not gu.isLocalDevelopment
        and "log_event" in util.settings
        and util.settings["log_event"] in ["true", "1"]
    ):
        util.writeEventDebug("EVENT", event)

    resourcePath = None
    httpMethod = None
    requestBody = None
    pathParams = None
    contentTypeHeader = None

    if "context" in event:
        resourcePath = event["context"]["resource-path"]
        httpMethod = event["context"]["http-method"]
        requestBody = event["body-json"]
        pathParams = event["params"]["path"]
    else:
        resourcePath = event["resource"]
        httpMethod = event["httpMethod"]
        requestBody = event["body"]
        if "headers" in event:
            if "Content-Type" in event["headers"]:
                contentTypeHeader = event["headers"]["Content-Type"]
            elif "content-type" in event["headers"]:
                contentTypeHeader = event["headers"]["content-type"]
        pathParams = getPathParams(event["resource"], event["path"])

    if pathParams:
        for param in pathParams:
            pathParams[param] = urllib.parse.unquote(pathParams[param])

    methodNotSupportedException = gu.UptakeblueException(
        Exception(f"http-method {httpMethod} is not supported for {resourcePath}"),
        f"{MODULE}.parseEvent()",
    )

    source = f"{MODULE}, resourcePath={resourcePath}, method={httpMethod}"
    startTime = time.perf_counter()

    try:
        #### AUTHTOKENS
        if resourcePath == "/authtokens":
            if httpMethod not in ["POST"]:
                raise methodNotSupportedException
            response = fn_m.authtokens_POST(util, requestBody)

        #### CONTENT
        elif resourcePath == "/content/{contentid}":
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
        elif resourcePath == "/image/{filename}":
            if httpMethod not in ["GET"]:
                raise methodNotSupportedException
            response = fn_i.image_GET(util, "image", pathParams)

        elif resourcePath == "/imagethumb/{filename}":
            if httpMethod not in ["GET"]:
                raise methodNotSupportedException
            response = fn_i.image_GET(util, "imagethumb", pathParams)

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
                response = fn_r.recipe_POST(
                    util,
                    requestBody,
                    contentTypeHeader,
                )
                util.writeEventTiming("func", "fn_r.recipe_POST()", startTime)
            elif httpMethod == "PUT":
                response = fn_r.recipe_PUT(
                    util,
                    requestBody,
                    contentTypeHeader,
                )
                util.writeEventTiming("func", "fn_r.recipe_PUT()", startTime)

        elif resourcePath == "/recipe/new":
            if httpMethod not in ["GET"]:
                raise methodNotSupportedException
            response = fn_r.recipe_GET_ListNew(util)
            util.writeEventTiming("func", "fn_r.recipe_GET_ListNew()", startTime)

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

        elif resourcePath == "/recipe/map/search/{keyword}":
            if httpMethod not in ["GET"]:
                raise methodNotSupportedException
            response = fn_r.recipe_GET_ListMapSearch(util, pathParams)
            util.writeEventTiming("func", "fn_r.recipe_GET_ListMapSearch()", startTime)

        #### RECIPECONTENT
        elif resourcePath == "/recipecontent":
            if httpMethod not in ["POST", "PUT"]:
                raise methodNotSupportedException
            if httpMethod == "POST":
                response = fn_rc.recipeContent_POST(util, requestBody)
                util.writeEventTiming("func", "fn_rc.recipeContent_POST()", startTime)
            elif httpMethod == "PUT":
                response = fn_rc.recipeContent_PUT(util, requestBody)
                util.writeEventTiming("func", "fn_rc.recipeContent_PUT()", startTime)

        elif resourcePath == "/recipecontent/{recipeid}/{contentid}":
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


def getPathParams(resource: str, path: str):
    fields = resource.split("/")
    values = path.split("/")
    pathParams = {}
    for i in range(0, len(fields)):
        if fields[i] != values[i]:
            field = fields[i].replace("{", "").replace("}", "")
            pathParams[field] = values[i]
    return pathParams
