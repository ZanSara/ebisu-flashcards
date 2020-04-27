from typing import Any, Callable, List, Mapping, Optional, Tuple

import abc
import os
import random
from datetime import datetime

from . import db, models


class Algorithm:

    def __init__(self, deck: models.Deck):
        # FIXME Make sure deck and cards contain the right extra fields
        self.deck = deck

    @abc.abstractmethod
    def export_to_file(self) -> str:
        """ Returns the path to a zipped file containing all the information needed to recreate a deck. """
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
    def process_result(self, card_id: int, user_id: int, test_results: Any) -> None:
        """ Calls the updated method of the card, enriching the input data if needed. """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")

    @abc.abstractmethod
    def next_card_to_review(self) -> 'Card':
        """ Computes which is the next card to be reviewed. """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")



class RandomOrder(Algorithm):
    
    def __init__(self, deck: models.Deck):
        super(Algorithm, self).__init__()
        self.deck = deck

    def export_to_file(self) -> str:
        """ Returns the path to a zipped file containing all the information needed to recreate a deck. """
        raise NotImplementedError("TODO in Random Order")
    
    def cards_to_review(self) -> int:
        """ Returns the number of cards that has been seen """
        return len([card for card in self.cards if card.last_review])

    def new_cards(self) -> int:
        """ Returns the number of unseen cards """
        return len([card for card in self.cards if not card.last_review])

    def process_result(self, user_id: int, test_results: str) -> None:
        """ 
        Saves a review with the test results (for eventual statistics) 
        """
        if not str(test_results).lower() == "true" and not str(test_results).lower() == "false":
            raise ValueError("Invalid test result for Random Order: {}".format(rest_results))
        #cards = models.Card.objects.get(id=card_id)
        user = models.User.objects.get(id=user_id)
        review = models.Review(
            user=user, 
            test_results=test_results.lower(), 
            review_time=datetime.utcnow()
        )
        self.deck.reviewing_card.update(push__reviews=review)
        self.deck.reviewing_card.save()

    def next_card_to_review(self) -> 'Card':
        """ 
        Picks a random card. 
        Avoids repeating the same card twice if so required. 
        """
        cards = models.Card.objects(deck=self.deck.id).all()
        
        try:
            self.deck.last_reviewed_card = self.deck.reviewing_card

            # To avoid asking twice the same card in a row
            while self.deck.reviewing_card == self.deck.last_reviewed_card:
                self.deck.reviewing_card = random.choice(cards)

        except models.Card.DoesNotExist:
            # Maybe it was deleted in the meantine
            self.deck.reviewing_card = random.choice(cards)
        self.deck.save()

        return self.deck.reviewing_card



class Ebisu(Algorithm):
    
    def __init__(self, deck: models.Deck):
        super(Algorithm, self).__init__()
        self.deck = deck

    def export_to_file(self) -> str:
        """ Returns the path to a zipped file containing all the information needed to recreate a deck. """
        raise NotImplementedError("TODO in Ebisu")
    
    def cards_to_review(self) -> int:
        """ Returns the number of cards that has been seen """
        return len([card for card in self.cards if card.last_review])

    def new_cards(self) -> int:
        """ Returns the number of unseen cards """
        return len([card for card in self.cards if not card.last_review])

    def process_result(self, user_id: int, test_results: str) -> None:
        """ 
        Saves a review with the test results (for eventual statistics) 
        """
        if not str(test_results).lower() == "true" and not str(test_results).lower() == "false":
            raise ValueError("Invalid test result for Random Order: {}".format(rest_results))
        #cards = models.Card.objects.get(id=card_id)
        user = models.User.objects.get(id=user_id)
        review = models.Review(
            user=user, 
            test_results=test_results.lower(), 
            review_time=datetime.utcnow()
        )
        self.deck.reviewing_card.update(push__reviews=review)
        self.deck.reviewing_card.save()

    def next_card_to_review(self) -> 'Card':
        """ 
        Picks a random card. 
        Avoids repeating the same card twice if so required. 
        """
        cards = models.Card.objects(deck=self.deck.id).all()
        
        try:
            self.deck.last_reviewed_card = self.deck.reviewing_card

            # To avoid asking twice the same card in a row
            while self.deck.reviewing_card == self.deck.last_reviewed_card:
                self.deck.reviewing_card = random.choice(cards)

        except models.Card.DoesNotExist:
            # Maybe it was deleted in the meantine
            self.deck.reviewing_card = random.choice(cards)
        self.deck.save()

        return self.deck.reviewing_card





ALGORITHM_MAPPING = {
    "Random Order": RandomOrder,
    "Ebisu": Ebisu,
}


def algorithm_engine(deck: 'Deck') -> Algorithm:
    """ Given the algorithm name, returns a suitable engine """
    try:
        return ALGORITHM_MAPPING[deck.algorithm](deck)
    except KeyError:
        raise ValueError("Algorithm name unknown: {}".format(deck.algorithm))


def import_from_file(file_path: str) -> 'Deck':
    """ Loads a new deck from a .zip file and adds it to the decks list. """
    raise NotImplementedError("TODO")
