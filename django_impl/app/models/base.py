from typing import Any, Callable

import abc
import os

import mongoengine as mongo
from django.utils import timezone


class User(mongo.Document):
    username = mongo.StringField(max_length=200, required=True, unique=True)
    email = mongo.EmailField(required=True, unique=True)
    password = mongo.BinaryField(required=True)
    icon = mongo.ImageField(blank=True)
    signed_in = mongo.BooleanField(default=False)
    last_sign_in = mongo.DateTimeField(default=timezone.now)
    date_created = mongo.DateTimeField(default=timezone.now)


class Tag(mongo.EmbeddedDocument):
    name = mongo.StringField(max_length=200, unique=True)
    description = mongo.StringField(max_length=2000)


class Renderer(mongo.Document):
    name = mongo.StringField(max_length=200, unique=True)
    description = mongo.StringField(max_length=2000)
    path = mongo.StringField()


class Fact(mongo.Document):
    fact = mongo.StringField(max_length=200)
    renderer = mongo.ReferenceField(Renderer, reverse_delete_rule=mongo.CASCADE)
    is_file = mongo.BooleanField(default=False)

    @property
    def value(self):
        return self.fact

    @property
    def widget(self):
        if self.renderer:
            return self.renderer.path
        else:
            return None

