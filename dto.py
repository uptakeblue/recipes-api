# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     1/20/2024
#
# Copyright 2023 - 2024 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
from datetime import datetime, date
import global_utility as gu

MODULE = "dto"


class recipe_dto:
    def __init__(self, initObject) -> None:
        self.Ingredients = None
        self.Instructions = None
        self.RetainImageFile = None
        self.Content = []
        if isinstance(initObject, tuple):
            dataRow: tuple = initObject
            self.RecipeId = dataRow[0]
            self.Title = dataRow[1]
            self.Description = dataRow[2]
            self.Note = dataRow[3]
            self.ImageFile: str = str(dataRow[4]) if dataRow[4] else None
            self.PhotoCredit: str = str(dataRow[5]) if dataRow[5] else None
            self.Route = str(dataRow[6]).lower()
            self.IsFavorite = dataRow[7] == 1
            self.ModifiedDate: datetime = dataRow[8]
        elif isinstance(initObject, dict):
            recipeDict: dict = initObject
            self.RecipeId = (
                int(recipeDict["recipeId"]) if "recipeId" in recipeDict else None
            )
            self.Title = recipeDict["title"]
            self.Description = (
                recipeDict["description"] if "description" in recipeDict else None
            )
            self.Note = recipeDict["note"] if "note" in recipeDict else None
            self.ImageFile = (
                recipeDict["imageFile"] if "imageFile" in recipeDict else None
            )
            self.PhotoCredit = (
                recipeDict["photoCredit"] if "photoCredit" in recipeDict else None
            )
            self.Route = recipeDict["route"] if "route" in recipeDict else None
            self.IsFavorite = (
                recipeDict["isfavorite"] == "true"
                if "isfavorite" in recipeDict
                else False
            )
            self.Ingredients = (
                recipeDict["ingredients"] if "ingredients" in recipeDict else None
            )
            self.Instructions = (
                recipeDict["instructions"] if "instructions" in recipeDict else None
            )
            self.RetainImageFile = (
                recipeDict["retainImageFile"] in ["true", "1"]
                if "retainImageFile" in recipeDict
                else None
            )
            self.ModifiedDate: datetime = (
                datetime.strptime(recipeDict["modifiedDate"], gu.DATETIMEFORMAT)
                if "modifiedDate" in recipeDict
                else None
            )
        else:
            raise gu.UptakeblueException(
                Exception("initObject type not recognized"),
                f"{MODULE} recipe_dto.init()",
            )

    def getDictionary(self) -> dict:
        recipeDict = {
            "recipeId": self.RecipeId,
            "title": self.Title,
            "description": self.Description,
            "note": self.Note,
            "imageFile": self.ImageFile,
            "photoCredit": self.PhotoCredit,
            "route": self.Route,
            "isFavorite": self.IsFavorite,
            "modifiedDate": self.ModifiedDate.strftime(gu.DATETIMEFORMAT)
            if self.ModifiedDate
            else None,
        }
        if self.Ingredients:
            recipeDict["ingredients"] = self.Ingredients
        if self.Instructions:
            recipeDict["instructions"] = self.Instructions
        if self.RetainImageFile is not None:
            recipeDict["retainImageFile"] = self.RetainImageFile
        if self.Content:
            recipeDict["content"] = []
            for content in self.Content:
                recipeDict["content"].append(content.getDictionary())

        return recipeDict


class content_dto:
    def __init__(self, initObject) -> None:
        if isinstance(initObject, tuple):
            dataRow: tuple = initObject
            self.ContentId = dataRow[0]
            self.Title = dataRow[1]
            self.Ingredients = dataRow[2]
            self.Instructions = dataRow[3]
            self.OrderId = dataRow[4] if len(dataRow) > 4 else None
            self.RecipeCount = dataRow[5] if len(dataRow) > 5 else None
            self.RecipeId = None
        elif isinstance(initObject, dict):
            recipeDict: dict = initObject
            self.ContentId = (
                recipeDict["contentId"] if "contentId" in recipeDict else None
            )
            self.Title = recipeDict["title"]
            self.Ingredients = recipeDict["ingredients"]
            self.Instructions = recipeDict["instructions"]
            self.OrderId = recipeDict["orderId"] if "orderId" in recipeDict else None
            self.RecipeCount = (
                recipeDict["recipeCount"] if "recipeCount" in recipeDict else False
            )
            self.RecipeId = (
                recipeDict["recipeId"] if "recipeId" in recipeDict else False
            )
        else:
            raise gu.UptakeblueException(
                Exception("initObject type not recognized"),
                f"{MODULE} content_dto.init()",
            )

    def getDictionary(self) -> dict:
        return {
            "contentId": self.ContentId,
            "title": self.Title,
            "ingredients": self.Ingredients.replace("\r", ""),
            "instructions": self.Instructions.replace("\r", ""),
            "orderId": self.OrderId,
            "recipeCount": self.RecipeCount,
            "recipeId": self.RecipeId,
        }


class recipeContent_dto:
    def __init__(self, initObject) -> None:
        if isinstance(initObject, tuple):
            dataRow: tuple = initObject
            self.RecipeId = dataRow[0]
            self.ContentId = dataRow[1]
            self.OrderID = dataRow[2]
        elif isinstance(initObject, dict):
            rcDict = initObject
            self.RecipeId = rcDict["recipeId"] if "recipeId" in rcDict else None
            self.ContentId = rcDict["contentId"] if "contentId" in rcDict else None
            self.OrderID = rcDict["orderId"] if "orderId" in rcDict else None

    def getDictionary(self) -> dict:
        return {
            "recipeId": self.RecipeId,
            "contentId": self.ContentId,
            "orderId": self.OrderID,
        }


class formData_dto:
    def __init__(self, initObject) -> None:
        self.Name = None
        self.Data = None
        self.DataType = "string"
        self.FileName = None
        metaDataTokens = initObject.split(b"\r\n\r\n")
        [metaData, self.Data] = metaDataTokens
        tokens = metaData.split(b"; ")

        self.Name = str(tokens[1].split(b"=")[1])
        if len(tokens) > 2:
            self.FileName = (
                str(tokens[2].split(b"=")[1]).replace("\n", "").replace("\r", "")
            )
            self.DataType = "bytes"

    def getDictionary(self) -> dict:
        formdataDict = {
            "name": self.Name,
            "data": self.Data.decode("utf-8"),
            "dataType": self.DataType,
        }
        if self.FileName:
            formdataDict["filename"] = self.FileName

        return formdataDict
