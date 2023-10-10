# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     10/9/2023
#
# Copyright 2023 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
from flask import request

import functions_recipe as fn_r
import functions_utility as fn_u
import utility as u

MODULE = "functions_route"

app_settings = {}

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
        e = u.UptakeblueException(err, f"{MODULE}.dateitem_GET()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response

def recipe_GET(recipeId:int):
    util = u.Global_Utility(app_settings)
    response = None
    try:
        result = fn_r.recipe_GET(util, recipeId)
        result['contents'] = fn_r.content_GET_List(util, recipeId)       

        response = (result, u.RESPONSECODE_OK)
    
    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.dateitem_GET()")
        response = fn_u.exceptionResponse(e)
    finally:
        return response
