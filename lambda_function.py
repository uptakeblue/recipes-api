# Author:       Michael Rubin
# Created:      1/5/2024
# Modified:     1/10/2024
#
# This file is the starting point for the application
# lambda_handler( ) is the registered entry point
#
# Copyright 2023 - 2024 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import sys
import json

try:
    import global_utility as gu
except ModuleNotFoundError as e:
    print(
        'Module "global_utility" is missing.  \nThis module is located in it\'s own '
        + 'Github repo: "https://github.com/uptakeblue/global".\n'
    )
    sys.exit(0)
import app


def lambda_handler(event, context):
    isBase64Encoded = False
    headers = {
        "Content-Type": "application/json",
    }

    [response, statusCode] = app.parseEvent(event)

    if "headers" in response:
        headers = response["headers"]

    if "isBase64Encoded" in response:
        isBase64Encoded = response["isBase64Encoded"]

    if "responseBody" in response:
        response = response["responseBody"]

    returnDict = {
        "statusCode": statusCode,
        "headers": headers,
        "body": response,
        "isBase64Encoded": isBase64Encoded,
    }

    return returnDict
