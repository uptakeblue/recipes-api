# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     1/8/2024
#
# Copyright 2023 - 2024 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import base64
import re
import time
import json

from requests_toolbelt.multipart import decoder
import functions_image as fn_i
import global_utility as gu
import dto as dto

# module constants
MODULE = "functions_recipe"


def recipe_GET_ListSearch(
    util: gu.Global_Utility,
    pathParams: dict,
):
    response = None
    try:
        if "keyword" not in pathParams:
            raise Exception("pathParams missing keyword")

        with util.pymysqlConnection.cursor() as cursor:
            args = [
                pathParams["keyword"],
            ]
        with util.pymysqlConnection.cursor() as cursor:
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_Get_ListSearch", args)
            rows = cursor.fetchall()
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_Get_List()", startTime)
            if rows:
                result = []
                for row in rows:
                    result.append(dto.recipe_dto(row).getDictionary())

                response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.recipe_GET_ListSearch()", paramargs=pathParams
        )

    return response


def recipe_GET(
    util: gu.Global_Utility,
    pathParams: dict,
):
    response = None
    try:
        if "recipeid" not in pathParams:
            raise Exception("pathParams missing recipeid")

        with util.pymysqlConnection.cursor() as cursor:
            args = [
                pathParams["recipeid"],
            ]
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_Get", args)
            row = cursor.fetchone()
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_Get()", startTime)
            if row:
                recipeDto = dto.recipe_dto(row)
                startTime = time.perf_counter()
                args = [
                    recipeDto.RecipeId,
                ]
                cursor.callproc("dbo.rcp_content_Get_ListByRecipe", args)
                rows = cursor.fetchall()
                util.writeEventTiming("dbproc", "dbo.rcp_recipe_GetByUrl()", startTime)
                if rows:
                    for row in rows:
                        recipeDto.Content.append(dto.content_dto(row))

                result = recipeDto.getDictionary()

                response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.recipe_GET()", paramargs=pathParams
        )

    return response


def recipe_GET_ByRoute(
    util: gu.Global_Utility,
    pathParams: dict,
):
    response = None
    try:
        if "routeurl" not in pathParams:
            raise Exception("pathParams missing routeurl")

        with util.pymysqlConnection.cursor() as cursor:
            args = [pathParams["routeurl"]]
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_GetByUrl", args)
            row = cursor.fetchone()
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_GetByUrl()", startTime)
            if row:
                recipeDto = dto.recipe_dto(row)
                startTime = time.perf_counter()
                args = [
                    recipeDto.RecipeId,
                ]
                cursor.callproc("dbo.rcp_content_Get_ListByRecipe", args)
                rows = cursor.fetchall()
                util.writeEventTiming("dbproc", "dbo.rcp_recipe_GetByUrl()", startTime)
                if rows:
                    for row in rows:
                        recipeDto.Content.append(dto.content_dto(row))

                result = recipeDto.getDictionary()

                response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.recipe_GET_ByRoute()", paramargs=pathParams
        )

    return response


def recipe_DELETE(
    util: gu.Global_Utility,
    pathParams: dict,
):
    response = None
    try:
        if "recipeid" not in pathParams:
            raise Exception("pathParams missing recipeid")

        with util.pymysqlConnection.cursor() as cursor:
            recipeId = pathParams["recipeid"]
            args = [
                recipeId,
            ]
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_Delete", args)
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_Delete()", startTime)
            response = {
                "message": f"Recipe was deleted",
                "recipeId": recipeId,
            }

            util.pymysqlConnection.commit()

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.recipe_DELETE()", paramargs=args
        )

    return response


def recipe_POST_multipartFormdata(
    util: gu.Global_Utility,
    requestBody,
    contentTypeHeader,
):
    response = None
    try:
        fileBytes = None
        formData = base64.b64decode(requestBody)
        result = {}
        for part in decoder.MultipartDecoder(formData, contentTypeHeader).parts:
            decoded_header = part.headers[b"Content-Disposition"].decode("utf-8")
            tokens = decoded_header.split(";")
            key = tokens[1].split("=")[1].replace('"', "")
            if len(tokens) > 2:
                fileBytes = part.content
                result[key] = tokens[2].split("=")[1].replace('"', "")
            else:
                result[key] = part.content.decode("utf-8")

        recipeDto = dto.recipe_dto(result)

        util.writeEventDebug("Recipe POST data", recipeDto.getDictionary())

        # add recipe record to database
        recipeId = None
        args = [
            recipeDto.Title,
            recipeDto.Description,
            recipeDto.Note,
            recipeDto.ImageFile,
            recipeDto.Route,
            recipeDto.IsFavorite,
            recipeDto.Ingredients,
            recipeDto.Instructions,
            recipeId,
        ]
        with util.pymysqlConnection.cursor() as cursor:
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_Post", args)
            cursor.execute("SELECT @_dbo.rcp_recipe_Post_8")
            recipeId = cursor.fetchone()[0]
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_Post()", startTime)

            util.pymysqlConnection.commit()

            result = {
                "message": f"Recipe was created",
                "recipeId": recipeId,
            }

            response = (result, gu.RESPONSECODE_OK)

        # upload image and thumbnail to s3
        fn_i.image_POST(
            util,
            fileBytes,
            recipeDto.ImageFile,
        )

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.recipe_POST_multipartFormdata()"
        )

    return response


def recipe_POST(
    util: gu.Global_Utility,
    requestBody: dict,
):
    response = None

    try:
        recipeId = None
        recipeDto = dto.recipe_dto(requestBody)

        args = [
            recipeDto.Title,
            recipeDto.Description,
            recipeDto.Note,
            recipeDto.ImageFile,
            recipeDto.Route,
            recipeDto.IsFavorite,
            recipeDto.Ingredients,
            recipeDto.Instructions,
            recipeId,
        ]
        with util.pymysqlConnection.cursor() as cursor:
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_Post", args)
            cursor.execute("SELECT @_dbo.rcp_recipe_Post_8")
            recipeId = cursor.fetchone()[0]
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_Post()", startTime)

            util.pymysqlConnection.commit()

            result = {
                "message": f"Recipe was created",
                "recipeId": recipeId,
            }

            response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.recipe_POST()", paramargs=args
        )

    return response


def recipe_PUT(
    util: gu.Global_Utility,
    requestBody: dict,
):
    response = None

    try:
        recipeDto = dto.recipe_dto(requestBody)
        args = [
            recipeDto.RecipeId,
            recipeDto.Title,
            recipeDto.Description,
            recipeDto.Note,
            recipeDto.ImageFile,
            recipeDto.Route,
            recipeDto.IsFavorite,
        ]
        with util.pymysqlConnection.cursor() as cursor:
            startTime = time.perf_counter()

            cursor.callproc("dbo.rcp_recipe_Put", args)
            util.pymysqlConnection.commit()
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_Put()", startTime)

            result = {
                "message": f"Recipe was updated",
                "recipeId": recipeDto.RecipeId,
            }

            response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(e, source=f"{MODULE}.recipe_PUT()", paramargs=args)

    return response


def recipe_GET_ListMap(
    util: gu.Global_Utility,
):
    response = None

    try:
        result = {
            "recipes": [],
            "contentTitles": [],
        }
        with util.pymysqlConnection.cursor() as cursor:
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_Get_List")
            rows = cursor.fetchall()
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_Get_List()", startTime)
            if rows:
                for row in rows:
                    result["recipes"].append(dto.recipe_dto(row).getDictionary())

            response = (result, gu.RESPONSECODE_OK)

            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_content_Get_List")
            rows = cursor.fetchall()
            util.writeEventTiming("dbproc", "dbo.rcp_content_Get_List()", startTime)
            if rows:
                for row in rows:
                    contentDto = dto.content_dto(row)
                    result["contentTitles"].append(
                        {
                            "contentId": contentDto.ContentId,
                            "title": contentDto.Title,
                        }
                    )

        response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(e, f"{MODULE}.recipe_GET_ListMap()")

    return response


def routeFromTitle(title: str) -> str:
    return (
        re.sub("[^0-9a-zA-Z]+", "-", title)
        .replace("--", "-")
        .replace("--", "-")
        .strip("-")
    )
