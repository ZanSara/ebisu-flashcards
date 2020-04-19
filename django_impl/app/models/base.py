from typing import Any, Callable, List, Mapping, Optional, Tuple

import abc
import os

import mongoengine as mongo
from django.utils import timezone


BOOLEAN_WIDGET = 'boolean-fact.html'
TEXT_WIDGET = 'text-fact.html'
HTML_WIDGET = 'html-fact.html'
IMAGE_WIDGET = 'image-fact.html'


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


class Review(mongo.EmbeddedDocument):
    user = mongo.ReferenceField(User)
    test_results = mongo.StringField()  # Can store more complex objects as JSON in case, I guess...
    review_time = mongo.DateTimeField(default=timezone.now)

    meta = {'allow_inheritance': True}


class Card(mongo.Document):
    deck = mongo.ReferenceField('Deck')
    question = mongo.ReferenceField(Fact)
    answer = mongo.ReferenceField(Fact)
    tags = mongo.ListField(Tag, blank=True)
    marked = mongo.BooleanField(default=False)
    hidden = mongo.BooleanField(default=False)
    reviews = mongo.EmbeddedDocumentListField(Review)

    meta = {'allow_inheritance': True}

    @property
    def last_review(self) -> Optional[Review]:
        if len(self.reviews):
            return max(self.reviews, key=lambda r: r.review_time)
        return None


    def __str__(self):
        if self.question and self.answer:
            return "Card: {} -> {}".format(self.question.fact, self.answer.fact)
        else:
            return "Card (unsaved)"


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

    @abc.abstractmethod
    def to_widgets(self):
        own_form = {
            'id': self.id,  # Won't be displayed
            'question': self.question,
            'answer': self.answer,
            'tags':  {
                'value': self.tags, 
                'widget': TEXT_WIDGET
            },
            'marked': {
                'value': self.marked, 
                'widget': BOOLEAN_WIDGET
            },
            'hidden': {
                'value': self.hidden, 
                'widget': BOOLEAN_WIDGET
            },
            'last_review': self.last_review, 
        }
        return own_form


class Deck(mongo.Document):
    name = mongo.StringField(max_length=200, unique=True)
    description = mongo.StringField(max_length=2000)
    tags = mongo.ListField(Tag, blank=True)

    last_reviewed_card =  mongo.ReferenceField(Card)
    currently_reviewing_card =  mongo.ReferenceField(Card)
    
    meta = {'allow_inheritance': True}

    @property
    def cards(self):
        try:
            return Card.objects.filter(deck=self.id).all()
        except mongo.DoesNotExist:
            return []

    @property
    @abc.abstractmethod
    def settings(self):
        """ Method for the subclasses' settings """
        return {}
            
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
    def to_dict(self):
        """ Returns a dictionary to be used in the views. """
        dict_form = {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'tags': self.tags,
        }
        return dict_form

    @abc.abstractmethod
    def process_result(self, card_id: int, user_id: int, test_results: Any) -> None:
        """ Calls the updated method of the card, enriching the input data if needed. """
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")


    @abc.abstractmethod
    def next_card_to_review(self) -> 'Card':
        """ Computes which is the next card to be reviewed. """
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")


    @abc.abstractmethod
    def last_reviewed_card(self) -> 'Card':
        """ Return the last card that has been reviewed. """
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")

    @abc.abstractmethod
    def filter_cards(self, filter: Callable):
        """ Apply the filtering function to the cards list. """
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")
