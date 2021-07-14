from typing import Any
import abc


class _Algorithm:

    def __init__(self, deck: 'Deck'):
        self.deck = deck

    @abc.abstractmethod
    def next_card_to_review(self) -> 'Card':
        """ Computes which is the next card to be reviewed. """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")

    @abc.abstractmethod
    def process_result(self, card_id: int, user_id: int, results: Any) -> None:
        """ Calls the updated method of the card, enriching the input data if needed. """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")

    @abc.abstractmethod
    def add_fieds_to_deck(self, value):
        """ Adds algorithm related calculated fields to the deck's JSON representation. """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")

    @abc.abstractmethod
    def add_fieds_to_card(self, card, value):
        """ Adds algorithm related calculated fields to the deck's JSON representation. """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")

    @abc.abstractmethod
    def export_to_file(self) -> str:
        """ Returns the path to a zipped file containing all the information needed to recreate a deck. """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")
    
    @abc.abstractmethod
    def import_from_file(self) -> str:
        """ Creates a deck starting from the path to a zipped file containing all the information needed """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")
    