from typing import Any, Callable, List, Mapping, Tuple

import abc
import mongoengine as mongo

from ..base import Tag
from ..cards import Card


class Deck(mongo.Document):
    name = mongo.StringField(max_length=200, unique=True)
    description = mongo.StringField(max_length=2000)
    tags = mongo.ListField(Tag, blank=True)
    cards =  mongo.ListField(mongo.ReferenceField(Card))

    last_reviewed_card =  mongo.ReferenceField(Card)
    currently_reviewing_card =  mongo.ReferenceField(Card)
    
    meta = {'allow_inheritance': True}

    @staticmethod
    def populate_fields_from_postdata(deck_instance: 'Deck', postdata: Mapping[str, Any]) -> 'Deck' :
        """ Returns the deck instance populated from the info contained into the POSTDATA dict. """
        deck_instance.name = postdata.get('deck_name')
        deck_instance.description = postdata.get('deck_description')
        # process tags
        # deck_subclass.tags = []
        return deck_instance

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
    def add_card(self, postdata: Mapping[str, Any]):
        """ Creates a new card of the right type and adds it to its own collection. """
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")

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
