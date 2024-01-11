# Author:       Michael Rubin
# Created:      11/3/2023
# Modified:     1/10/2024
#
# Copyright 2023 - 2024 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import base64
import io

from PIL import Image

import global_utility as gu
import dto as dto


# module constants
MODULE = "functions_image"


# retrieves a single image file
def image_GET(
    util: gu.Global_Utility,
    folder: str,
    pathParams: dict,
):
    response = None
    try:
        if "filename" not in pathParams:
            raise Exception("filename not in pathParams")

        filename = pathParams["filename"]

        key = f"{folder}/{filename}"

        fileObject = util.s3Client.get_object(
            Bucket=util.settings["image_bucket"],
            Key=key,
        )

        fileContent = fileObject["Body"].read()
        result = {
            "responseBody": base64.b64encode(fileContent),
            "isBase64Encoded": True,
            "headers": {
                "Content-Type": "application/json",
                "Content-Disposition": f"attachment; filename={filename}",
            },
        }

        response = (result, gu.RESPONSECODE_OK)

    except Exception as err:
        e = gu.UptakeblueException(err, f"{MODULE}.image_GET()")
        e.StatusCode = err.code if err.code else gu.RESPONSECODE_SERVERERROR
        raise e

    return response


# uploads a single image file
def image_POST(
    util: gu.Global_Utility,
    fileBytes,
    filename,
):
    response = None
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    responseCode = None
    try:
        if not "." in filename:
            responseCode = gu.RESPONSECODE_NOTALLOWED
            raise Exception("Filename must have an extension")

        extension = filename.rsplit(".", 1)[1].lower()
        if not extension in ALLOWED_EXTENSIONS:
            responseCode = gu.RESPONSECODE_NOTALLOWED
            raise Exception("File must be .jpeg, .jpg or png")

        key = f"images/{filename}"

        # upload image to s3
        util.s3Client.put_object(
            Bucket=util.settings["image_bucket"],
            Body=fileBytes,
            Key=key,
        )

        # resize image to thumbnail
        image = Image.open(io.BytesIO(fileBytes))
        newWidth = 120
        ratio = newWidth / float(image.width)
        newHeight = int(float(image.height) * float(ratio))
        thumbnail = image.resize((newWidth, newHeight))

        # save image bytes
        fileBytes = io.BytesIO()
        thumbnail.save(fileBytes, image.format)
        fileBytes.seek(0, 0)

        key = f"thumbnail-images/{filename}"

        # upload image to s3
        util.s3Client.put_object(
            Bucket=util.settings["image_bucket"],
            Body=fileBytes,
            Key=key,
            ContentType=f"image/{image.format}",
        )

    except Exception as e:
        err = gu.UptakeblueException(e, f"{MODULE}.image_POST()")
        err.StatusCode = responseCode if responseCode else gu.RESPONSECODE_SERVERERROR
        raise err

    return response
