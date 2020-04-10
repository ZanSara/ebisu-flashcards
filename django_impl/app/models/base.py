import os
from django.db import models


class FactLayout(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=2000)
    filename = models.FilePathField(max_length=500,
        path=os.path.join(os.getcwd(), 
                "app", 
                "templates",
                "app",
                "fact_templates"))

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return "Fact Layout #{}: '{}'".format(self.id, self.name)

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'filename': self.filename.split(os.path.sep)[-1]
        }


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=2000)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Tag #{}: '{}'".format(self.id, self.name)
