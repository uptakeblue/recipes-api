# Author:       Michael Rubin
# Created:      10/30/2023
# Modified:     1/8/2024
#
# Copyright 2023 - 2024 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import global_utility as gu
import dto as dto
import time

MODULE = "functions_recipecontent"


def recipeContent_GET(
    util: gu.Global_Utility,
    pathParams: dict,
):
    response = None
    try:
        if "recipeid" not in pathParams:
            raise Exception("pathParams missing recipeid")
        if "content" not in pathParams:
            raise Exception("pathParams missing content")

        args = [
            pathParams["recipeId"],
            pathParams["contentId"],
        ]

        with util.pymysqlConnection.cursor() as cursor:
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_content_Get", args)
            row = cursor.fetchone()
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_content_Get()", startTime)

            if row:
                result = dto.recipeContent_dto(row).getDictionary()

                response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.recipecontent_GET()", paramargs=args
        )

    return response


def recipeContent_DELETE(
    util: gu.Global_Utility,
    pathParams: dict,
):
    response = None
    try:
        if "recipeid" not in pathParams:
            raise Exception("pathParams missing recipeid")
        if "content" not in pathParams:
            raise Exception("pathParams missing content")

        recipeId = pathParams["recipeId"]
        contentId = pathParams["contentId"]

        args = [
            recipeId,
            contentId,
        ]

        with util.pymysqlConnection.cursor() as cursor:
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_content_Delete", args)

            util.pymysqlConnection.commit()
            util.writeEventTiming(
                "dbproc", "dbo.rcp_recipe_content_Delete()", startTime
            )

            result = {
                "message": f"Recipe-Content relationship was deleted",
                "recipeId": recipeId,
                "contentId": contentId,
            }

        response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.recipeContent_DELETE()", paramargs=args
        )

    return response


def recipeContent_POST(
    util: gu.Global_Utility,
    requestBody: dict,
):
    response = None
    try:
        recipeContentDto = dto.recipeContent_dto(requestBody)
        args = [
            recipeContentDto.RecipeId,
            recipeContentDto.ContentId,
        ]
        with util.pymysqlConnection.cursor() as cursor:
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_content_Post", args)

            util.pymysqlConnection.commit()
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_content_Post()", startTime)

            response = {
                "message": f"Recipe-Content relationship was created",
                "recipeId": recipeContentDto.RecipeId,
                "contentId": recipeContentDto.ContentId,
            }

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.recipeContent_POST()", paramargs=args
        )

    return response


def recipeContent_PUT(
    util: gu.Global_Utility,
    requestBody: dict,
):
    response = None
    try:
        recipeContentDto = dto.recipeContent_dto(requestBody)
        args = [
            recipeContentDto.RecipeId,
            recipeContentDto.ContentId,
            recipeContentDto.OrderID,
        ]
        with util.pymysqlConnection.cursor() as cursor:
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_content_Put", args)

            util.pymysqlConnection.commit()
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_content_Put()", startTime)

            response = {
                "message": f"Recipe-Content relationship was updated",
                "recipeId": recipeContentDto.RecipeId,
                "contentId": recipeContentDto.ContentId,
            }

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.recipeContent_PUT()", paramargs=args
        )

    return response
