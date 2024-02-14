# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     2/13/2024
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
            result = {
                "message": f"Recipe was deleted",
                "recipeId": recipeId,
            }

            util.pymysqlConnection.commit()

            response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.recipe_DELETE()", paramargs=args
        )

    return response


def recipe_POST(
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

        if "route" in result and "imageFile" in result and "." in result['imageFile']:
            result['imageFile'] = f"{result['route']}.{result['imageFile'].split(".")[0]}"

        recipeDto = dto.recipe_dto(result)

        util.writeEventDebug("Recipe POST data", recipeDto.getDictionary())

        # add recipe record to database
        recipeId = None
        args = [
            recipeDto.Title,
            recipeDto.Description,
            recipeDto.Note,
            recipeDto.ImageFile,
            recipeDto.PhotoCredit,
            recipeDto.Route,
            recipeDto.IsFavorite,
            recipeDto.Ingredients,
            recipeDto.Instructions,
            recipeId,
        ]
        with util.pymysqlConnection.cursor() as cursor:
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_Post", args)
            cursor.execute("SELECT @_dbo.rcp_recipe_Post_9")
            recipeId = cursor.fetchone()[0]
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_Post()", startTime)

            util.pymysqlConnection.commit()

            result = {
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                "responseBody": f"Recipe {recipeId} was created",
            }

            response = (result, gu.RESPONSECODE_OK)

        # upload image and thumbnail to s3
        if fileBytes:
            fn_i.image_POST(
                util,
                fileBytes,
                recipeDto.ImageFile,
            )

    except Exception as e:
        raise gu.UptakeblueException(e, source=f"{MODULE}.recipe_POST()")

    return response


def recipe_PUT(
    util: gu.Global_Utility,
    requestBody: dict,
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

        if "route" in result and "imageFile" in result and "." in result['imageFile']:
            result['imageFile'] = f"{result['route']}.{result['imageFile'].split(".")[0]}"

        recipeDto = dto.recipe_dto(result)

        util.writeEventDebug("Recipe PUT data", recipeDto.getDictionary())

        with util.pymysqlConnection.cursor() as cursor:
            # get previous
            args = [
                recipeDto.RecipeId,
            ]
            cursor.callproc("dbo.rcp_recipe_Get", args)
            row = cursor.fetchone()
            if row:
                previousRecipeDto = dto.recipe_dto(row)

            if recipeDto.RetainImageFile:
                recipeDto.ImageFile = previousRecipeDto.ImageFile

            # update the recipe record
            args = [
                recipeDto.RecipeId,
                recipeDto.Title,
                recipeDto.Description,
                recipeDto.Note,
                recipeDto.ImageFile,
                recipeDto.PhotoCredit,
                recipeDto.Route,
                recipeDto.IsFavorite,
            ]

            startTime = time.perf_counter()

            cursor.callproc("dbo.rcp_recipe_Put", args)
            util.pymysqlConnection.commit()
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_Put()", startTime)

            result = {
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                "responseBody": f"Recipe {recipeDto.RecipeId} was updated",
            }

            if fileBytes and (previousRecipeDto.ImageFile != recipeDto.ImageFile):
                fn_i.image_POST(
                    util,
                    fileBytes,
                    recipeDto.ImageFile,
                )

            response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(e, source=f"{MODULE}.recipe_PUT()", paramargs=args)

    return response


def recipe_GET_ListNew(
    util: gu.Global_Utility,
):
    response = None

    try:
        result = []
        with util.pymysqlConnection.cursor() as cursor:
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_Get_ListNew")
            rows = cursor.fetchall()
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_Get_ListNew()", startTime)
            if rows:
                for row in rows:
                    recipeDto = dto.recipe_dto(row)
                    result.append(
                        {
                            "recipeId": recipeDto.RecipeId,
                            "title": recipeDto.Title,
                            "route": recipeDto.Route,
                        }
                    )

        response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(e, f"{MODULE}.recipe_GET_ListNew()")

    return response


def recipe_GET_ListMap(
    util: gu.Global_Utility,
):
    response = None

    try:
        result = {"recipes": [], "contentTitles": [], "newRecipes": []}
        with util.pymysqlConnection.cursor() as cursor:
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_Get_List")
            rows = cursor.fetchall()
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_Get_List()", startTime)
            if rows:
                for row in rows:
                    result["recipes"].append(dto.recipe_dto(row).getDictionary())

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

            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_Get_ListNew")
            rows = cursor.fetchall()
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_Get_ListNew()", startTime)
            if rows:
                for row in rows:
                    recipeDto = dto.recipe_dto(row)
                    result["newRecipes"].append(
                        {
                            "recipeId": recipeDto.RecipeId,
                            "title": recipeDto.Title,
                            "route": recipeDto.Route,
                        }
                    )

        response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(e, f"{MODULE}.recipe_GET_ListMap()")

    return response


def recipe_GET_ListMapSearch(
    util: gu.Global_Utility,
    pathParams: dict,
):
    response = None
    try:
        if "keyword" not in pathParams:
            raise Exception("pathParams missing keyword")

        result = {
            "recipes": [],
            "contentTitles": [],
        }

        with util.pymysqlConnection.cursor() as cursor:
            args = [
                pathParams["keyword"],
            ]
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_recipe_Get_ListSearch", args)
            rows = cursor.fetchall()
            util.writeEventTiming("dbproc", "dbo.rcp_recipe_Get_List()", startTime)
            if rows:
                for row in rows:
                    result["recipes"].append(dto.recipe_dto(row).getDictionary())

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
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.recipe_GET_ListMapSearch()", paramargs=pathParams
        )

    return response


def recipeMeta_GET(
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


# utility functions


def routeFromTitle(title: str) -> str:
    return (
        re.sub("[^0-9a-zA-Z]+", "-", title)
        .replace("--", "-")
        .replace("--", "-")
        .strip("-")
    )
