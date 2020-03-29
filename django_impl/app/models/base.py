import os
from django.db import models


class CardLayout(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    filename = models.FilePathField(
        path=os.path.join(os.getcwd(), 
                "app", 
                "templates",
                "app",
                "card_templates"))

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Card Layout #{}: '{}'".format(self.id, self.name)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Tag #{}: '{}'".format(self.id, self.name)
