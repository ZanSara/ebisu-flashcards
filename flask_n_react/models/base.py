from typing import Any, Callable, List, Mapping, Optional, Tuple

import abc
import os
from datetime import datetime

from marshmallow import Schema, fields, post_load
from marshmallow_oneofschema import OneOfSchema
import mongoengine as mongo


BOOLEAN_WIDGET = 'boolean-fact.html'
TEXT_WIDGET = 'text-fact.html'
HTML_WIDGET = 'html-fact.html'
IMAGE_WIDGET = 'image-fact.html'


class User(mongo.Document):
    username = mongo.StringField(max_length=200, required=True, unique=True)
    email = mongo.EmailField(required=True, unique=True)
    password = mongo.BinaryField(required=True)
    icon = mongo.ImageField(blank=True)
    last_sign_in = mongo.DateTimeField(default=datetime.utcnow())
    date_created = mongo.DateTimeField(default=datetime.utcnow())

    class JsonSchema(Schema):
        name = fields.Str()
        email = fields.Email() 
        password = fields.Str()   # FIXME
        icon = fields.Str()  # URL to image
        last_sign_in = fields.DateTime()
        date_created = fields.DateTime()

        @post_load
        def make_user(self, data, **kwargs):
            return User(**data)

    def __str__(self):
        return self.name


class Tag(mongo.EmbeddedDocument):
    name = mongo.StringField(max_length=200, unique=True)
    
    class JsonSchema(Schema):
        name = fields.Str()

        @post_load
        def make_tag(self, data, **kwargs):
            return Tag(**data)

    def __str__(self):
        return self.name


class Renderer(mongo.Document):
    name = mongo.StringField(max_length=200, unique=True)
    description = mongo.StringField(max_length=2000)
    path = mongo.StringField()

    class JsonSchema(Schema):
        name = fields.Str()
        description = fields.Str()
        path = fields.Str()

        @post_load
        def make_renderer(self, data, **kwargs):
            return Renderer(**data)

    def __str__(self):
        return self.name


class Fact(mongo.Document):
    fact = mongo.StringField(max_length=200)
    renderer = mongo.ReferenceField(Renderer, reverse_delete_rule=mongo.CASCADE)
    is_file = mongo.BooleanField(default=False)

    class JsonSchema(Schema):
        fact = fields.Str()
        renderer = fields.Nested(Renderer.JsonSchema())
        is_file = fields.Bool()

        @post_load
        def make_fact(self, data, **kwargs):
            return Fact(**data)

    def __str__(self):
        return self.fact


class ReviewAlgorithmData(mongo.EmbeddedDocument):
        meta = {'allow_inheritance': True}

        class JsonSchema:
            @post_load
            def make_review_algorithm_data(self, data, **kwargs):
                return ReviewAlgorithmData(**data)    

class Review(mongo.EmbeddedDocument):

    user = mongo.ReferenceField(User)
    test_results = mongo.StringField()  # Can store more complex objects as JSON in case, I guess...
    review_time = mongo.DateTimeField(default=datetime.utcnow())
    algorithm_data = mongo.EmbeddedDocumentField(ReviewAlgorithmData)

    class JsonSchema(Schema):
        user = fields.Nested(User.JsonSchema())
        test_results = fields.Raw()
        review_time = fields.DateTime()
        algorithm_data = fields.Nested(ReviewAlgorithmData.JsonSchema())

        @post_load
        def make_review(self, data, **kwargs):
            return Review(**data)

    def __str__(self):
        return "{} ({}): {}".format(self.review_time, self.user, self.test_results)



class CardAlgorithmData(mongo.EmbeddedDocument):
        meta = {'allow_inheritance': True}

        class JsonSchema:
            @post_load
            def make_card_algorithm_data(self, data, **kwargs):
                return CardAlgorithmData(**data)    

class Card(mongo.Document):
    question = mongo.ReferenceField(Fact)
    answer = mongo.ReferenceField(Fact)
    tags = mongo.ListField(Tag, blank=True)
    marked = mongo.BooleanField(default=False)
    hidden = mongo.BooleanField(default=False)
    reviews = mongo.EmbeddedDocumentListField(Review)
    algorithm_data = mongo.EmbeddedDocumentField(CardAlgorithmData)

    @property
    def last_review(self) -> Optional[Review]:
        if len(self.reviews):
            return max(self.reviews, key=lambda r: r.review_time)
        return None

    class JsonSchema(Schema):
        question = fields.Nested(Fact.JsonSchema())
        answer = fields.Nested(Fact.JsonSchema())
        tags = fields.Nested(Tag.JsonSchema(), many=True)
        marked = fields.Bool()
        hidden = fields.Bool()
        reviews = fields.Nested(Review.JsonSchema(), many=True)
        last_review = fields.Nested(Review.JsonSchema())
        algorithm_data = fields.Nested(Card.AlgorithmData.JsonSchema())

        @post_load
        def make_card(self, data, **kwargs):
            return Card(**data)

    def __str__(self):
        return "{} -> {}".format(self.question.fact, self.answer.fact)


    @abc.abstractmethod
    def load_from_postdata(self, postdata: Mapping[str, Any]) -> None :
        """ Returns the card instance populated from the info contained into the POSTDATA dict. """
        # Renderer(name="HTML Renderer", description="A renderer for HTML", path="html-fact.html").save()
        # default_renderer = Renderer.objects.get(name="Text Renderer")

        question = Fact(fact=postdata.get('question'), 
                        renderer=Renderer.objects.get(id=postdata.get("question_renderer")))
        question.save()
        answer = Fact(fact=postdata.get('answer'),
                      renderer=Renderer.objects.get(id=postdata.get("answer_renderer")))
        answer.save()
        self.question = question.id
        self.answer = answer.id
        # process tags
        # self.tags = postdata.get('tags')
        self.marked = postdata.get('marked')
        self.hidden = postdata.get('hidden')



class DeckAlgorithmData(mongo.EmbeddedDocument):
        meta = {'allow_inheritance': True}

        class JsonSchema:
            @post_load
            def make_deck_algorithm_data(self, data, **kwargs):
                return DeckAlgorithmData(**data)    

class Deck(mongo.Document):
    name = mongo.StringField(max_length=200, unique=True)
    description = mongo.StringField(max_length=2000)
    cards =  mongo.ListField(mongo.ReferenceField(Card))
    tags = mongo.ListField(Tag, blank=True)
    last_reviewed_card =  mongo.ReferenceField(Card)
    currently_reviewing_card =  mongo.ReferenceField(Card)
    algorithm_data = mongo.EmbeddedDocumentField(DeckAlgorithmData)

    @property
    def cards(self):
        try:
            return Card.objects.filter(deck=self.id).all()
        except mongo.DoesNotExist:
            return []

    @property
    def id_raw(self):
        return str(self.id)
            
    @property
    @abc.abstractmethod
    def cards_to_review(self) -> int:
        """ Returns the number of cards to review according to some arbitrary rule set by the subclass """
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")

    @property
    @abc.abstractmethod
    def new_cards(self) -> int:
        """ Returns the number of new cards according to some arbitrary rule set by the subclass """
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")

    
    class JsonSchema(OneOfSchema):
        id_raw = fields.Str()  # FIXME Find better way to translate the ID into a string at marshal time
        name = fields.Str()
        description = fields.Str()
        tags = fields.Nested(Tag.JsonSchema(), many=True)
        cards_to_review = fields.Int()
        new_cards = fields.Int()
        algorithm_data = fields.Nested(DeckAlgorithmData.JsonSchema())

        @post_load
        def make_deck(self, data, **kwargs):
            return Deck(**data)


    @staticmethod
    def populate_fields_from_postdata(deck_instance: 'Deck', postdata: Mapping[str, Any]) -> 'Deck' :
        """ Returns the deck instance populated from the info contained into the POSTDATA dict. """
        deck_instance.name = postdata.get('deck_name')
        deck_instance.description = postdata.get('deck_description')
        # process tags
        # deck_subclass.tags = []
        return deck_instance

    @abc.abstractmethod
    def update_from_postdata(self, postdata: Mapping[str, Any]) -> None:
        """ Updates its own fields taking the values from a POST request """
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")

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
