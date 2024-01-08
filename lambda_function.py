# Author:       Michael Rubin
# Created:      1/5/2024
# Modified:     1/8/2024
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
    [response, statusCode] = app.parseEvent(event)

    return {
        "statusCode": statusCode,
        "headers": {"Content-Type": "application/json"},
        "body": response,
        "isBase64Encoded": False,
    }
