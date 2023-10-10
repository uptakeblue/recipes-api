# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     10/9/2023
#
# Copyright 2023 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import utility as u
import recipe_dto as dto

MODULE = "functions_recipe"

def recipe_GET_List(util: u.Global_Utility) -> list:
    response = None
    keyword = None
    args = [
        keyword
    ]
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_recipe_Search", args)
            rows = cursor.fetchall()
            if rows:
                response = []
                for row in rows:
                    recipeDto = dto.recipe_dto(row)
                    response.append(recipeDto.getDictionary())

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.dateitem_GET_ListByDate()", paramarge=args
        )

    return response

def recipe_GET(util: u.Global_Utility, recipeId) -> dict:
    response = None
    args = [
        recipeId
    ]
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_recipe_Get", args)
            row = cursor.fetchone()
            if row:
                recipeDto = dto.recipe_dto(row)
                response = recipeDto.getDictionary()

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.dateitem_GET_ListByDate()", paramarge=args
        )

    return response

def content_GET_List(util: u.Global_Utility, recipeId) -> dict:
    response = None
    args = [
        recipeId
    ]
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_content_Get_ListByRecipe", args)
            rows = cursor.fetchall()
            if rows:
                response = []
                for row in rows:
                    contentDto = dto.content_dto(row)
                    response.append(contentDto.getDictionary())

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.dateitem_GET_ListByDate()", paramarge=args
        )

    return response
