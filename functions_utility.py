# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     10/9/2023
#
# Copyright 2023 - 2024 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import utility as u
from pymysql import err

from datetime import datetime

MODULE = "functions_utility"


def datetimeFromString(dateStr):
    response: datetime = None
    if dateStr and isinstance(dateStr, str):
        format = u.DATETIMEFORMAT if " " in dateStr else u.DATEFORMAT
        response = datetime.strptime(dateStr, format)
    return response


def dateFromDataItem(dateItem):
    response: datetime = None
    if dateItem:
        if isinstance(dateItem, tuple):
            dateString = str(dateItem[0])
        else:
            dateString = str(dateItem)
        dateObject = datetimeFromString(dateString)
        response = dateObject.date()
    return response


def datetimeFromDataItem(dateItem):
    response: datetime = None
    if dateItem:
        if isinstance(dateItem, tuple):
            dateString = str(dateItem[0])
        else:
            dateString = str(dateItem)
        response = datetimeFromString(dateString)
    return response


## EXCEPTION HANDLER


def exceptionResponse(e: Exception):
    responseCode = 400
    responseMessage = None
    try:
        if isinstance(e, u.UptakeblueException):
            err: u.UptakeblueException = e
            responseMessage = err.Message
            responseCode = err.ResponseCode
        elif e.args and (isinstance(e.args, tuple) or isinstance(e.args, list)):
            responseMessage = str(e.args)
        else:
            responseMessage = str(e)
    except Exception as e:
        raise e
    return (responseMessage, responseCode)
