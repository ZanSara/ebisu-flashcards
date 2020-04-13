from typing import Any, Callable

import abc
import os

import mongoengine as mongo
from django.utils import timezone


class User(mongo.Document):
    username = mongo.StringField(max_length=200, required=True, unique=True)
    email = mongo.EmailField(required=True, unique=True)
    password = mongo.BinaryField(required=True)
    icon = mongo.ImageField()
    signed_in = mongo.BooleanField(default=False)
    last_sign_in = mongo.DateTimeField()
    date_created = mongo.DateTimeField(default=timezone.now)


class Tag(mongo.EmbeddedDocument):
    name = mongo.StringField(max_length=200, unique=True)
    description = mongo.StringField(max_length=2000)


class Renderer(mongo.Document):
    name = mongo.StringField(max_length=200, unique=True)
    description = mongo.StringField(max_length=2000)
    filename = mongo.StringField()


class Fact(mongo.Document):
    # fact = mongo.StringField(max_length=200, unique=True)  # Defined by the subclasses 
    renderer = mongo.ReferenceField(Renderer, reverse_delete_rule=mongo.CASCADE)

    meta = {'allow_inheritance': True}

class Review(mongo.EmbeddedDocument):
    user = mongo.ReferenceField(User)
    test_results = mongo.StringField()  # Can store more complex objects as JSON in case, I guess...
    review_time = mongo.DateTimeField(default=timezone.now)

    meta = {'allow_inheritance': True}


class Card(mongo.Document):
    question = mongo.ReferenceField(Fact)
    answer = mongo.ReferenceField(Fact)
    tags = mongo.ListField(Tag, blank=True)
    marked = mongo.BooleanField(default=False)
    hidden = mongo.BooleanField(default=False)
    reviews = mongo.ListField(mongo.EmbeddedDocumentField(Review))

    meta = {'allow_inheritance': True}
