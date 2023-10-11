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
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_recipe_Get_List")
            rows = cursor.fetchall()
            if rows:
                response = []
                for row in rows:
                    recipeDto = dto.recipe_dto(row)
                    response.append(recipeDto.getDictionary())

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.recipe_GET_List()"
            )

    return response


def recipe_GET_ListSearch(util: u.Global_Utility, keyword) -> list:
    response = None
    args = [
        keyword
    ]
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_recipe_Get_ListSearch", args)
            rows = cursor.fetchall()
            if rows:
                response = []
                for row in rows:
                    recipeDto = dto.recipe_dto(row)
                    response.append(recipeDto.getDictionary())

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.recipe_GET_ListSearch()", paramarge=args
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
            e, source=f"{MODULE}.recipe_GET()", paramarge=args
        )

    return response


def recipe_DELETE(util: u.Global_Utility, recipeId) -> dict:
    response = None
    args = [
        recipeId
    ]
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_recipe_Delete", args)
            response = {
                "message": f"Recipe was deleted",
                "recipeId": recipeId
            }

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.recipe_DELETE()", paramarge=args
        )

    return response


def recipe_POST(util: u.Global_Utility, recipeDto:dto.recipe_dto) -> dict:
    response = None
    recipeId = None
    args=[
        recipeDto.Title,
        recipeDto.Description,
        recipeDto.Note,
        recipeDto.ImageFile,
        recipeDto.UrlRoute,
        recipeDto.IsFavorite,
        recipeId,
    ]
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_recipe_Post", args)
            cursor.execute('SELECT @_dbo.rcp_recipe_Post_6')
            recipeId = cursor.fetchone()[0]
            response = {
                "message": f"Recipe was created",
                "recipeId": recipeId
            }

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.recipe_POST()", paramarge=args
        )

    return response


def recipe_PUT(util: u.Global_Utility, recipeDto:dto.recipe_dto) -> dict:
    response = None
    args=[
        recipeDto.RecipeId,
        recipeDto.Title,
        recipeDto.Description,
        recipeDto.Note,
        recipeDto.ImageFile,
        recipeDto.UrlRoute,
        recipeDto.IsFavorite,
    ]
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_recipe_Put", args)
            response = {
                "message": f"Recipe was uupdated",
                "recipeId": recipeDto.RecipeId
            }

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.recipe_PUT()", paramarge=args
        )

    return response
