# Author:       Michael Rubin
# Created:      10/10/2023
# Modified:     1/7/2024
#
# Copyright 2023 - 2024 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import global_utility as gu
import dto as dto

import time

MODULE = "functions_content"


def content_GET_List(
    util: gu.Global_Utility,
):
    response = None
    try:
        with util.pymysqlConnection.cursor() as cursor:
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_content_Get_List")
            rows = cursor.fetchall()
            util.writeEventTiming("dbproc", "dbo.rcp_content_Get_List()", startTime)
            if rows:
                result = []
                for row in rows:
                    contentDto = dto.content_dto(row)
                    result.append(
                        {
                            "contentId": contentDto.ContentId,
                            "title": contentDto.Title,
                        }
                    )

                response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(e, source=f"{MODULE}.content_GET_List()")

    return response


def content_GET_ListSearch(
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
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_content_Get_ListSearch", args)
            rows = cursor.fetchall()
            util.writeEventTiming(
                "dbproc", "dbo.rcp_content_Get_ListSearch()", startTime
            )
            if rows:
                result = []
                for row in rows:
                    result.append(dto.content_dto(row).getDictionary())

                response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.content_GET_ListSearch()", paramarge=pathParams
        )

    return response


def content_GET_ListByRecipe(
    util: gu.Global_Utility,
    pathParams: dict,
):
    response = None
    try:
        if "recipeid" not in pathParams:
            raise Exception("pathParams missing recipeid")

        with util.pymysqlConnection.cursor() as cursor:
            args = [pathParams["recipeid"]]
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_content_Get_ListByRecipe", args)
            rows = cursor.fetchall()
            util.writeEventTiming(
                "dbproc", "dbo.rcp_content_Get_ListByRecipe()", startTime
            )
            if rows:
                result = []
                for row in rows:
                    result.append(dto.content_dto(row).getDictionary())

                response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.content_GET_ListByRecipe()", paramarge=pathParams
        )

    return response


def content_GET(
    util: gu.Global_Utility,
    pathParams: dict,
):
    response = None
    try:
        if "contentid" not in pathParams:
            raise Exception("pathParams missing contentid")

        with util.pymysqlConnection.cursor() as cursor:
            args = [
                pathParams["contentid"],
            ]
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_content_Get", args)
            row = cursor.fetchone()
            util.writeEventTiming("dbproc", "dbo.rcp_content_Get()", startTime)
            if row:
                result = dto.content_dto(row).getDictionary()

                response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.content_GET()", paramarge=pathParams
        )

    return response


def content_DELETE(
    util: gu.Global_Utility,
    pathParams: dict,
):
    response = None
    try:
        if "contentid" not in pathParams:
            raise Exception("pathParams missing contentid")

        with util.pymysqlConnection.cursor() as cursor:
            contentId = pathParams["contentid"]
            args = [
                contentId,
            ]
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_content_Delete", args)
            util.pymysqlConnection.commit()
            util.writeEventTiming("dbproc", "dbo.rcp_content_Delete()", startTime)

            result = {
                "message": f"Content was deleted",
                "contentId": contentId,
            }
            response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.content_DELETE()", paramarge=args
        )

    return response


def content_POST(
    util: gu.Global_Utility,
    requestBody: dict,
):
    response = None

    try:
        with util.pymysqlConnection.cursor() as cursor:
            contentId = None
            contentDto = dto.content_dto(requestBody)
            args = [
                contentDto.Title,
                contentDto.Ingredients,
                contentDto.Instructions,
                contentDto.RecipeId,
                contentId,
            ]
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_content_Post", args)
            cursor.execute("SELECT @_dbo.rcp_content_Post_4")
            contentId = cursor.fetchone()[0]

            util.pymysqlConnection.commit()
            util.writeEventTiming("dbproc", "dbo.rcp_content_Post()", startTime)

            result = {
                "message": f"Content was created",
                "contentId": contentId,
            }
            response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.content_POST()", paramarge=requestBody
        )

    return response


def content_PUT(
    util: gu.Global_Utility,
    requestBody: dict,
):
    response = None

    try:
        with util.pymysqlConnection.cursor() as cursor:
            contentDto = dto.content_dto(requestBody)
            args = [
                contentDto.ContentId,
                contentDto.Title,
                contentDto.Ingredients,
                contentDto.Instructions,
            ]
            startTime = time.perf_counter()
            cursor.callproc("dbo.rcp_content_Put", args)

            util.pymysqlConnection.commit()
            util.writeEventTiming("dbproc", "dbo.rcp_content_Put()", startTime)

            result = {
                "message": f"Content was updated",
                "contentId": contentDto.ContentId,
            }
            response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.content_PUT()", paramarge=requestBody
        )

    return response
