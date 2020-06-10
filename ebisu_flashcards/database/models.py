from typing import Any, Callable, List, Mapping, Optional, Tuple

import abc
import os
from datetime import datetime

import mongoengine
from flask_bcrypt import generate_password_hash, check_password_hash

from ebisu_flashcards.database import db, algorithms


class Tag(db.EmbeddedDocument):
    name = db.StringField(max_length=200, required=True, unique=True)
    
    def __str__(self):
        return self.name


class Template(db.Document):
    name = db.StringField(max_length=200, required=True, unique=True)
    description = db.StringField(max_length=2000, required=True)
    path = db.StringField(required=True)

    def __str__(self):
        return self.name


class Review(db.DynamicEmbeddedDocument):
    user = db.ReferenceField('User', required=True)
    test_results = db.DynamicField(required=True)
    review_time = db.DateTimeField(default=datetime.utcnow(), required=True)

    def __str__(self):
        return "{} ({}): {}".format(self.review_time, self.user, self.test_results)


class Card(db.DynamicDocument):
    deck = db.ReferenceField('Deck', required=True)
    question = db.StringField(required=True, unique=False)
    question_template = db.ReferenceField(Template, required=True)
    answer = db.StringField(required=True, unique=False)
    answer_template = db.ReferenceField(Template, required=True)
    tags = db.ListField(Tag, blank=True)
    marked = db.BooleanField(default=False)
    hidden = db.BooleanField(default=False)
    reviews = db.EmbeddedDocumentListField(Review)

    @property
    def last_review(self) -> Optional[Review]:
        if len(self.reviews):
            return max(self.reviews, key=lambda r: r.review_time)
        return None

    def to_mongo(self, *args, **kwargs):
        value = super().to_mongo(*args, **kwargs)
        engine = algorithms.algorithm_engine(self.deck)
        value = engine.add_fields_to_card(self, value)
        return value

    def __str__(self):
        return "{} -> {}".format(self.question, self.answer)


class Deck(db.DynamicDocument):
    name = db.StringField(max_length=200, unique=True)
    description = db.StringField(max_length=2000, required=True)
    algorithm = db.StringField(max_length=50, required=True)  # FIXME make this a Choice field at least
    author = db.ReferenceField('User', required=True)
    tags = db.ListField(Tag, blank=True)

    last_reviewed_card =  db.ReferenceField(Card, reverse_delete_rule=mongoengine.NULLIFY)
    reviewing_card =  db.ReferenceField(Card, reverse_delete_rule=mongoengine.NULLIFY)

    def to_mongo(self, *args, **kwargs):
        value = super().to_mongo(*args, **kwargs)
        engine = algorithms.algorithm_engine(self)
        value = engine.add_fields_to_deck(value)
        return value


class User(db.Document):
    username = db.StringField(max_length=200, required=True, unique=True)
    icon = db.ImageField(blank=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    last_sign_in = db.DateTimeField(default=datetime.utcnow())
    date_created = db.DateTimeField(default=datetime.utcnow())
    
    decks = db.ListField(db.ReferenceField('Deck', reverse_delete_rule=db.PULL))

    def __str__(self):
        return "{} ({})".format(self.username, self.email)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Register delete rules
User.register_delete_rule(Deck, 'added_by', db.CASCADE)
Template.register_delete_rule(Card, 'question_template', db.DENY)
Template.register_delete_rule(Card, 'answer_template', db.DENY)
