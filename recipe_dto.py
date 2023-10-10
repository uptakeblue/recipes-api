# Author:       Michael Rubin
# Created:      10/9/2023
# Modified:     10/9/2023
#
# Copyright 2023 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
from datetime import datetime, date
import utility as u


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

    def getDictionary(self) -> dict:
        return {
            "contentId": self.ContentId,
            "title": self.Title,
            "ingredients": self.Ingredients,
            "instructions": self.Instructions,
            "orderId": self.OrderId,
            "recipeCount": self.RecipeCount,
        }
                