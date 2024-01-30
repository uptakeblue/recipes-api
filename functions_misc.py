# Author:       Michael Rubin
# Created:      1/30/2024
# Modified:     1/30/2024
#
# Copyright 2023 - 2024 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import global_utility as gu

MODULE = "functions_misc"


#### AUTHENTICATE
def authenticate_POST(util: gu.Global_Utility, requestBody: dict):
    response = None
    try:
        result = util.cognitoClient.admin_initiate_auth(
            AuthFlow="ADMIN_NO_SRP_AUTH",
            AuthParameters={
                "USERNAME": requestBody["username"],
                "PASSWORD": requestBody["password"],
            },
            ClientId=util.settings["recipeAppClientId"],
            UserPoolId=util.settings["uptakeblueUserPoolId"],
        )
        if (
            "AuthenticationResult" in result
            and "IdToken" in result["AuthenticationResult"]
        ):
            result = {
                "newPasswordRequired": False,
                "token": result["AuthenticationResult"]["IdToken"],
                "accessToken": result["AuthenticationResult"]["AccessToken"],
            }

            response = (result, gu.RESPONSECODE_OK)

    except Exception as e:
        raise gu.UptakeblueException(
            e, source=f"{MODULE}.authenticate_POST()", paramargs=requestBody
        )

    return response
