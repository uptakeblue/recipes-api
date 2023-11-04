# Author:       Michael Rubin
# Created:      11/3/2023
# Modified:     11/3/2023
#
# Copyright 2023 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import os
from flask import request, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image

import utility as u
import functions_utility as fn_u

MODULE = "functions_image"
IMAGE_FOLDER = None
IMAGE_THUMBNAIL_FOLDER = None

# retrieves a single image file
def image_GET(folder:str, filename:str):
    response = None
    try:
        filename = secure_filename(filename)
        response = send_from_directory(folder, filename)
    
    except Exception as err:
        if err.code==404:
            response = send_from_directory('images', 'default.png')
        else:
            e = u.UptakeblueException(err, f"{MODULE}.image_GET()")
            response = fn_u.exceptionResponse(e)

    finally:
        return response

# retrieves a single image file
def image_POST(util:u.Global_Utility):
    response = None
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    responseCode = u.RESPONSECODE_OK
    
    try:
        
        if "file" in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename) 
            
            if not("." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS):
                responseCode = u.RESPONSECODE_NOTALLOWED
                raise Exception("File must be .jpeg, .jpg or png")
            
            extension = filename.split(".")[1]
            urlRoute = request.form['routeurl'] if "routeurl" in request.form else None

            targetFilename = f"{urlRoute}.{extension}" if urlRoute else filename
            
            targetFilepath = os.path.join(IMAGE_FOLDER, targetFilename)
            thumbnailFilepath = os.path.join(IMAGE_THUMBNAIL_FOLDER, targetFilename)

            file.save(targetFilepath)

            # resize and save in thumbnails folder
            image = Image.open(targetFilepath)
            newWidth = 120
            ratio = newWidth/float(image.width)
            newHeight = int(float(image.height)*float(ratio))
            thumbnail = image.resize((newWidth, newHeight))

            thumbnail.save(thumbnailFilepath)
                
            response = {
                "message": "File uploaded successfully"
            }
        else:
            responseCode = u.RESPONSECODE_BADREQUEST
            raise Exception("No file was uploaded")

    except Exception as err:
        e = u.UptakeblueException(err, f"{MODULE}.image_POST()")
        e.ResponseCode = responseCode
        response = fn_u.exceptionResponse(e)

    finally:
        return response
