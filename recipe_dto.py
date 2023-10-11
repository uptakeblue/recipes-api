# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     10/10/2023
#
# Copyright 2023 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
from datetime import datetime, date
import utility as u

MODULE = "dto"

class recipe_dto:
    def __init__(self, initObject) -> None:
        if isinstance(initObject, tuple):
            dataRow:tuple = initObject
            self.RecipeId = dataRow[0]
            self.Title = dataRow[1]
            self.Description = dataRow[2]
            self.Note = dataRow[3]
            self.ImageFile = dataRow[4]
            self.UrlRoute = dataRow[5]
            self.IsFavorite = (dataRow[6]==1)
        elif isinstance(initObject, dict):
            recipeDict:dict = initObject
            self.RecipeId = recipeDict['recipeId'] if "recipeId" in recipeDict else None
            self.Title = recipeDict["title"]
            self.Description = recipeDict['description'] if "description" in recipeDict else None
            self.Note = recipeDict['note'] if "note" in recipeDict else None
            self.ImageFile = recipeDict['imageFile'] if "imageFile" in recipeDict else None
            self.UrlRoute = recipeDict['urlRoute'] if "urlRoute" in recipeDict else None
            self.IsFavorite = recipeDict['isFavorite'] if "isFavorite" in recipeDict else False
        else:
            raise u.UptakeblueException(Exception("initObject type not recognized"), f"{MODULE} recipe_dto.init()")

    def getDictionary(self) -> dict:
        return{
            "recipeId": self.RecipeId,
            "title": self.Title,
            "description": self.Description,
            "note": self.Note,
            "imageFile": self.ImageFile,
            "urlRoute": self.UrlRoute,
            "isFavorite": self.IsFavorite,
        }
    

class content_dto:
    def __init__(self, initObject) -> None:
        if isinstance(initObject, tuple):
            dataRow:tuple = initObject
            self.ContentId = dataRow[0]
            self.Title = dataRow[1]
            self.Ingredients = dataRow[2]
            self.Instructions = dataRow[3]
            self.OrderId = dataRow[4] if len(dataRow) > 4 else None
            self.RecipeCount = dataRow[5] if len(dataRow) > 5 else None
            self.RecipeId = None
        elif isinstance(initObject, dict):
            recipeDict:dict = initObject
            self.ContentId = recipeDict['contentId'] if "contentId" in recipeDict else None
            self.Title = recipeDict["title"]
            self.Ingredients = recipeDict['ingredients']
            self.Instructions = recipeDict['instructions']
            self.OrderId = recipeDict['orderId'] if "orderId" in recipeDict else None
            self.RecipeCount = recipeDict['recipeCount'] if "recipeCount" in recipeDict else False
            self.RecipeId = recipeDict['recipeId'] if "recipeId" in recipeDict else False
        else:
            raise u.UptakeblueException(Exception("initObject type not recognized"), f"{MODULE} content_dto.init()")

    def getDictionary(self) -> dict:
        return {
            "contentId": self.ContentId,
            "title": self.Title,
            "ingredients": self.Ingredients,
            "instructions": self.Instructions,
            "orderId": self.OrderId,
            "recipeCount": self.RecipeCount,
            "recipeId":self.RecipeId,
        }
                