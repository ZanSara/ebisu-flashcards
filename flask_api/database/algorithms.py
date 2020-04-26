from typing import Any, Callable, List, Mapping, Optional, Tuple

import abc
import os
from datetime import datetime

from . import models


class Algorithm:

    def __init__(self, deck: models.Deck):
        # FIXME Make sure deck and cards contain the right extra fields
        self.deck = deck

    @abc.abstractmethod
    def card_recall_index(card: models.Card) -> float:
        """ Computes the recall index for the card """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")
    
    @abc.abstractmethod
    def cards_to_review(self) -> int:
        """ Returns the number of cards to review according to some arbitrary rule set by the subclass """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")

    @abc.abstractmethod
    def new_cards(self) -> int:
        """ Returns the number of new cards according to some arbitrary rule set by the subclass """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")

    @abc.abstractmethod
    def export_to_file(self) -> str:
        """ Returns the path to a zipped file containing all the information needed to recreate a deck. """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")
    
    @abc.abstractmethod
    def filter_cards(self, filter: Callable):
        """ Returns a filtered list of card by applying filter on the returned list """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")

    @abc.abstractmethod
    def process_result(self, card_id: int, user_id: int, test_results: Any) -> None:
        """ Calls the updated method of the card, enriching the input data if needed. """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")

    @abc.abstractmethod
    def next_card_to_review(self) -> 'Card':
        """ Computes which is the next card to be reviewed. """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")


class Ebisu(Algorithm):
    pass


class RandomOrder(Algorithm):
    pass
