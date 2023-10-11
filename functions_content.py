# Author:       Michael Rubin
# Created:      10/10/2023
# Modified:     10/10/2023
#
# Copyright 2023 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import utility as u
import recipe_dto as dto

MODULE = "functions_content"

def content_GET_List(util: u.Global_Utility) -> list:
    response = None
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_content_Get_List")
            rows = cursor.fetchall()
            if rows:
                response = []
                for row in rows:
                    contentDto = dto.content_dto(row)
                    response.append(contentDto.getDictionary())

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.content_GET_List()"
        )

    return response


def content_GET_ListSearch(util: u.Global_Utility, keyword:str) -> list:
    response = None
    args = [
        keyword
    ]
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_content_Get_ListSearch", args)
            rows = cursor.fetchall()
            if rows:
                response = []
                for row in rows:
                    contentDto = dto.content_dto(row)
                    response.append(contentDto.getDictionary())

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.content_GET_ListSearch()", paramarge=args
        )

    return response


def content_GET_ListByRecipe(util: u.Global_Utility, recipeId) -> dict:
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
            e, source=f"{MODULE}.content_GET_ListByRecipe()", paramarge=args
        )

    return response


def content_GET(util: u.Global_Utility, contentId) -> dict:
    response = None
    args = [
        contentId
    ]
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_content_Get", args)
            row = cursor.fetchone()
            if row:
                contentDto = dto.content_dto(row)
                response = contentDto.getDictionary()

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.content_GET()", paramarge=args
        )

    return response


def content_DELETE(util: u.Global_Utility, contentId) -> dict:
    response = None
    args = [
        contentId
    ]
    try:
        with util.pymysqlConnection.cursor() as cursor:
            cursor.callproc("dbo.rcp_content_Delete", args)
            response = {
                "message": f"Content was deleted",
                "contentId": contentId
            }

    except Exception as e:
        raise u.UptakeblueException(
            e, source=f"{MODULE}.content_DELETE()", paramarge=args
        )

    return response


