# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     10/10/2023
#
# Copyright 2023 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
from flask import request

import functions_recipe as fn_r
import functions_utility as fn_u
import functions_content as fn_c
import recipe_dto as dto
import utility as u

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
    try:
        result = fn_r.recipe_GET_ListSearch(util, keyword)
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
