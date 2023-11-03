# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     11/2/2023
#
# Copyright 2023 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
from flask import request, send_file, send_from_directory
from werkzeug.utils import secure_filename

import functions_recipe as fn_r
import functions_utility as fn_u
import functions_content as fn_c
import functions_recipecontent as fn_rc
import recipe_dto as dto
import utility as u
import os

MODULE = "functions_route"

app_settings = {}

#### RECIPE
def recipe_GET_Map():
    util = u.Global_Utility(app_settings)
    response = None
    result = {
        "recipes":[],
        "recipetitles":[]
    }
    try:
        recipeDictArray = fn_r.recipe_GET_List(util)
        for recipe in recipeDictArray:
            result['recipes'].append(recipe)
            result['recipetitles'].append({
                "recipeId":recipe['recipeId'],
                "title":recipe['title'],
            })
        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.recipe_GET_Map()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response
    

def recipe_GET_ListSearch(keyword:str):
    util = u.Global_Utility(app_settings)
    response = None
    result = {
        "recipes":[],
        "recipetitles":[]
    }
    try:
        recipeDictArray = fn_r.recipe_GET_ListSearch(util, keyword)
        for recipe in recipeDictArray:
            result['recipes'].append(recipe)
            result['recipetitles'].append({
                "recipeId":recipe['recipeId'],
                "title":recipe['title'],
            })
        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.recipe_GET_ListSearch()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response


def recipe_GET(recipeId:int):
    util = u.Global_Utility(app_settings)
    response = None
    try:
        result = fn_r.recipe_GET(util, recipeId)
        result['contents'] = fn_c.content_GET_ListByRecipe(util, recipeId)       

        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.recipe_GET()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response


def recipe_GET_ByRoute(routeUrl:str):
    util = u.Global_Utility(app_settings)
    response = None
    try:
        result = fn_r.recipe_GET_ByRoute(util, routeUrl)
        result['contents'] = fn_c.content_GET_ListByRecipe(util, result['recipeId'])

        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.recipe_GET_ByRoute()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response


def recipe_DELETE(recipeId:int):
    util = u.Global_Utility(app_settings)
    response = None
    try:
        result = fn_r.recipe_DELETE(util, recipeId)
        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.recipe_DELETE()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response


def recipe_PUT():
    util = u.Global_Utility(app_settings)
    response = None
    try:
        recipeDto = dto.recipe_dto(request.json)
        result = fn_r.recipe_PUT(util, recipeDto)

        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.recipe_PUT()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response


def recipe_POST():
    util = u.Global_Utility(app_settings)
    response = None
    try:
        recipeDto = dto.recipe_dto(request.json)
        result = fn_r.recipe_POST(util, recipeDto)

        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.recipe_POST()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response



#### CONTENT
def content_GET_List():
    util = u.Global_Utility(app_settings)
    response = None
    try:
        result = fn_c.content_GET_List(util)

        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.content_GET_List()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response


def content_GET_ListSearch(keyword):
    util = u.Global_Utility(app_settings)
    response = None
    try:
        result = fn_c.content_GET_ListSearch(util, keyword)

        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.content_GET_ListSearch()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response


def content_GET(contentId):
    util = u.Global_Utility(app_settings)
    response = None
    try:
        result = fn_c.content_GET(util, contentId)

        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.content_GET()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response


def content_DELETE(contentId):
    util = u.Global_Utility(app_settings)
    response = None
    try:
        result = fn_c.content_DELETE(util, contentId)

        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.content_DELETE()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response


def content_PUT():
    util = u.Global_Utility(app_settings)
    response = None
    try:
        contentDto = dto.content_dto(request.json)
        result = fn_c.content_PUT(util, contentDto)

        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.content_PUT()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response


def content_POST():
    util = u.Global_Utility(app_settings)
    response = None
    try:
        contentDto = dto.content_dto(request.json)
        result = fn_c.content_POST(util, contentDto)

        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.recipe_POST()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response



#### RECIPECONTENT
def recipeContent_GET(recipeId:int, contentId:int):
    util = u.Global_Utility(app_settings)
    response = None
    try:
        result = fn_rc.recipeContent_GET(util, recipeId, contentId)

        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.recipeContent_GET()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response


def recipeContent_DELETE(recipeId:int, contentId:int):
    util = u.Global_Utility(app_settings)
    response = None
    try:
        result = fn_rc.recipeContent_DELETE(util, recipeId, contentId)

        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.recipeContent_DELETE()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response


def recipeContent_PUT():
    util = u.Global_Utility(app_settings)
    response = None
    try:
        recipeContentDto = dto.recipeContent_dto(request.json)
        result = fn_rc.recipeContent_PUT(util, recipeContentDto)

        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.recipeContent_PUT()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response


def recipeContent_POST():
    util = u.Global_Utility(app_settings)
    response = None
    try:
        recipeContentDto = dto.recipeContent_dto(request.json)
        result = fn_rc.recipeContent_POST(util, recipeContentDto)

        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.recipeContent_POST()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response


#### IMAGES
# retrieves a single image file
def image_GET(folder:str, filename:str):
    response = None
    try:
        filename = secure_filename(filename)
        response = send_from_directory(folder, filename)
    
    except Exception as err:
        if err.code==404:
            response = send_from_directory('images', 'default.png')
        else:
            e = u.UptakeblueException(err, f"{MODULE}.image_GET()")
            response = fn_u.exceptionResponse(e)

    finally:
        return response

# retrieves a single image file
def image_POST():
    response = None
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    responseCode = u.RESPONSECODE_OK
    
    try:
        
        if "file" in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename) 
            targetFilename = request.form['target'] if "target" in request.form else filename
            
            if not("." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS):
                responseCode = u.RESPONSECODE_NOTALLOWED
                raise Exception("File must be .jpeg, .jpg or png")
            
            file.save(os.path.join(app_settings['IMAGE_FOLDER'], targetFilename))
                
            response = {
                "message": "File uploaded successfully"
            }
        else:
            responseCode = u.RESPONSECODE_BADREQUEST
            raise Exception("No file was uploaded")

    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.image_POST()")
        e.ResponseCode = responseCode
        response = fn_u.exceptionResponse(e)

    finally:
        return response
