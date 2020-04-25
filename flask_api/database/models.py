from typing import Any, Callable, List, Mapping, Optional, Tuple

import abc
import os
from datetime import datetime

from . import db
from flask_bcrypt import generate_password_hash, check_password_hash


class Tag(db.EmbeddedDocument):
    name = db.StringField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name


class Template(db.Document):
    name = db.StringField(max_length=200, unique=True)
    description = db.StringField(max_length=2000)
    path = db.StringField()

    def __str__(self):
        return self.name


class Fact(db.Document):
    fact = db.StringField(max_length=200)
    template = db.ReferenceField(Template)
    is_file = db.BooleanField(default=False)

    def __str__(self):
        return self.fact


class Review(db.EmbeddedDocument):
    user = db.ReferenceField('User')
    test_results = db.StringField()  # Can store more complex objects as JSON in case, I guess...
    review_time = db.DateTimeField(default=datetime.utcnow())

    def __str__(self):
        return "{} ({}): {}".format(self.review_time, self.user, self.test_results)


class Card(db.Document):
    question = db.ReferenceField(Fact)
    answer = db.ReferenceField(Fact)
    tags = db.ListField(Tag, blank=True)
    marked = db.BooleanField(default=False)
    hidden = db.BooleanField(default=False)
    reviews = db.EmbeddedDocumentListField(Review)

    @property
    def last_review(self) -> Optional[Review]:
        if len(self.reviews):
            return max(self.reviews, key=lambda r: r.review_time)
        return None

    def __str__(self):
        return "{} -> {}".format(self.question.fact, self.answer.fact)


class Deck(db.Document):
    name = db.StringField(max_length=200, unique=True)
    description = db.StringField(max_length=2000)
    algorithm = db.StringField(max_length=50)  # FIXME make this a Choice field at least
    author = db.ReferenceField('User')
    cards = db.ListField(db.ReferenceField(Card))
    tags = db.ListField(Tag, blank=True)
    last_reviewed_card =  db.ReferenceField(Card)
    currently_reviewing_card =  db.ReferenceField(Card)

    @property
    def cards(self):
        try:
            return Card.objects.filter(deck=self.id).all()
        except db.DoesNotExist:
            return []
            
    @property
    @abc.abstractmethod
    def cards_to_review(self) -> int:
        """ Returns the number of cards to review according to some arbitrary rule set by the subclass """
        return 0
        #raise NotImplementedError("Can't use Deck base class: use one of the subclasses")

    @property
    @abc.abstractmethod
    def new_cards(self) -> int:
        """ Returns the number of new cards according to some arbitrary rule set by the subclass """
        return 0
        #raise NotImplementedError("Can't use Deck base class: use one of the subclasses")

    @abc.abstractmethod
    def import_from_file(self, packaged_file, private=False):
        """ Loads a new deck from a .zip file and adds it to the decks list. """
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")

    @abc.abstractmethod
    def export_to_file(self):
        """ Returns a zipped file containing all the information needed to recreate a deck. """
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")
    
    @abc.abstractmethod
    def filter_cards(self, filter: Callable):
        """ Returns a filtered list of card by applying filter on the returned list """
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")

    @abc.abstractmethod
    def process_result(self, card_id: int, user_id: int, test_results: Any) -> None:
        """ Calls the updated method of the card, enriching the input data if needed. """
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")

    @abc.abstractmethod
    def next_card_to_review(self) -> 'Card':
        """ Computes which is the next card to be reviewed. """
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")



class User(db.Document):
    username = db.StringField(max_length=200, required=True, unique=True)
    icon = db.ImageField(blank=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    last_sign_in = db.DateTimeField(default=datetime.utcnow())
    date_created = db.DateTimeField(default=datetime.utcnow())
    
    decks = db.ListField(db.ReferenceField('Deck', reverse_delete_rule=db.PULL))

    def __str__(self):
        return self.name

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Register delete rules
User.register_delete_rule(Deck, 'added_by', db.CASCADE)
Template.register_delete_rule(Fact, 'template', db.DENY)
