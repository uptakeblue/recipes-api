# Author:       Michael Rubin
# Created:      10/30/2023
# Modified:     11/5/2023
#
# Copyright 2023 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import utility as u
import dto as dto

MODULE = "functions_recipecontent"

def recipeContent_GET(util: u.Global_Utility, recipeId:int, contentId:int) -> dict:
    response = None
    args = [
        recipeId,
        contentId,
    ]
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_recipe_content_Get", args)
            row = cursor.fetchone()
            if row:
                contentDto = dto.recipeContent_dto(row)
                response = contentDto.getDictionary()

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.recipecontent_GET()", paramarge=args
        )

    return response


def recipeContent_DELETE(util: u.Global_Utility, recipeId:int, contentId:int) -> dict:
    response = None
    args = [
        recipeId,
        contentId,
    ]
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_recipe_content_Delete", args)

            util.pymysqlConnection.commit()
            
            response = {
                "message": f"Recipe-Content relationship was deleted",
                "recipeId": recipeId,
                "contentId": contentId,
            }

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.recipeContent_DELETE()", paramarge=args
        )

    return response




def recipeContent_POST(util: u.Global_Utility, recipeContentDto:dto.recipeContent_dto) -> dict:
    response = None
    args=[
        recipeContentDto.RecipeId,
        recipeContentDto.ContentId,
    ]
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_recipe_content_Post", args)
            
            util.pymysqlConnection.commit()

            response = {
                "message": f"Recipe-Content relationship was created",
                "recipeId": recipeContentDto.RecipeId,
                "contentId": recipeContentDto.ContentId
            }

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.recipeContent_POST()", paramarge=args
        )

    return response


def recipeContent_PUT(util: u.Global_Utility, recipeContentDto:dto.recipeContent_dto) -> dict:
    response = None
    args=[
        recipeContentDto.RecipeId,
        recipeContentDto.ContentId,
        recipeContentDto.OrderID
    ]
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_recipe_content_Put", args)

            util.pymysqlConnection.commit()

            response = {
                "message": f"Recipe-Content relationship was updated",
                "recipeId": recipeContentDto.RecipeId,
                "contentId": recipeContentDto.ContentId
            }

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.recipeContent_PUT()", paramarge=args
        )

    return response
