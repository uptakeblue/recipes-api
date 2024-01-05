# Author:       Michael Rubin
# Created:      11/3/2023
# Modified:     1/5/2024
#
# Copyright 2023 - 2024 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import os
from flask import request, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image

import utility as u
import dto as dto
import functions_utility as fn_u
import functions_recipe as fn_r


# module constants
MODULE = "functions_image"
IMAGE_FOLDER = None
IMAGE_THUMBNAIL_FOLDER = None


# retrieves a single image file
def image_GET(folder: str, filename: str):
    response = None
    try:
        filename = secure_filename(filename)
        response = send_from_directory(folder, filename)

    except Exception as err:
        if err.code == 404:
            response = send_from_directory("images", "default.png")
        else:
            e = u.UptakeblueException(err, f"{MODULE}.image_GET()")
            response = fn_u.exceptionResponse(e)

    finally:
        return response


# uploads a single image file
def image_POST(recipeRoute):
    response = None
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

    try:
        requestFile = request.files["file"]
        filename = secure_filename(requestFile.filename)

        if not (
            "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        ):
            responseCode = u.RESPONSECODE_NOTALLOWED
            raise Exception("File must be .jpeg, .jpg or png")

        extension = filename.split(".")[1]
        targetFilename = f"{recipeRoute}.{extension}" if recipeRoute else filename

        targetFilepath = os.path.join(IMAGE_FOLDER, targetFilename)
        thumbnailFilepath = os.path.join(IMAGE_THUMBNAIL_FOLDER, targetFilename)

        requestFile.save(targetFilepath)

        # resize and save in thumbnails folder
        image = Image.open(targetFilepath)
        newWidth = 120
        ratio = newWidth / float(image.width)
        newHeight = int(float(image.height) * float(ratio))
        thumbnail = image.resize((newWidth, newHeight))

        thumbnail.save(thumbnailFilepath)

        response = {
            "message": "File uploaded successfully",
            "filename": targetFilename,
            "responseCode": u.RESPONSECODE_OK,
        }

    except Exception as err:
        # swallow the error
        e = u.UptakeblueException(err, f"{MODULE}.image_POST()")
        response = {
            "message": e.Message,
            "filename": targetFilename,
            "responseCode": u.RESPONSECODE_SERVERERROR,
        }

    finally:
        return response
