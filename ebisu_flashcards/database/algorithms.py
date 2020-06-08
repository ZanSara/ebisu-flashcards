from typing import Any, Callable, List, Mapping, Optional, Tuple

import abc
import os
import random
import ebisu
from datetime import datetime, timedelta

from ebisu_flashcards.database import db, models
from ebisu_flashcards import errors


class Algorithm:

    def __init__(self, deck: 'Deck'):
        self.deck = deck

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
    def cards_to_review(self) -> int:
        """ Returns the number of cards to review according to some arbitrary rule set by the subclass """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")

    @abc.abstractmethod
    def new_cards(self) -> int:
        """ Returns the number of new cards according to some arbitrary rule set by the subclass """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")

    @abc.abstractmethod
    def process_result(self, card_id: int, user_id: int, results: Any) -> None:
        """ Calls the updated method of the card, enriching the input data if needed. """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")

    @abc.abstractmethod
    def next_card_to_review(self) -> 'Card':
        """ Computes which is the next card to be reviewed. """
        raise NotImplementedError("Can't use Algorithm base class: use one of the subclasses")



class RandomOrder(Algorithm):

    dynamic_fields = ["prioritize_unseen", "consecutive_never_identical"]

    def __init__(self, deck: 'Deck'):
        # Validate
        if deck.algorithm != "Random Order":
            raise ValueError("Deck algorithm does not match Random Order: {}".format(deck.algorithm))

        for field in RandomOrder.dynamic_fields:
            if field not in deck._dynamic_fields:
                raise ValueError("Deck is missing Random Order's dynamic field: {}".format(field))

        super(Algorithm, self).__init__()
        self.deck = deck
        
    def add_fields_to_deck(self, value):
        value["cards_to_review"] = len(self.cards_to_review())
        value["new_cards"] = len(self.new_cards())
        return value

    def add_fields_to_card(self, card, value):
        return value
        
    def export_to_file(self) -> str:
        """ 
        Returns the path to a zipped file containing all the information needed to recreate a deck. 
        """
        raise NotImplementedError("TODO in Random Order")
    
    def cards_to_review(self) -> List['Card']:
        """ 
        Returns the list of cards that has been seen 
        """
        cards = models.Card.objects(deck=self.deck.id).all()
        return [card for card in cards if card.last_review]

    def new_cards(self) -> List['Card']:
        """ 
        Returns the list of unseen cards 
        """
        cards = models.Card.objects(deck=self.deck.id).all()
        return [card for card in cards if not card.last_review]

    def process_result(self, user_id: int, results: bool) -> None:
        """ 
        Saves a review with the test results (for eventual statistics) 
        """
        if not isinstance(results, bool):
            raise ValueError("Invalid test result for Random Order: {}".format(results))
       
        user = models.User.objects.get(id=user_id)
        review = models.Review(
            user=user, 
            test_results=results, 
            review_time=datetime.utcnow()
        )
        self.deck.reviewing_card.update(push__reviews=review)
        self.deck.reviewing_card.save()

    def next_card_to_review(self) -> 'Card':
        """ 
        Picks a random card. 
        Avoids repeating the same card twice if so required. 
        Gives priority to unseen cards if so required.
        """
        cards = models.Card.objects(deck=self.deck.id).all()
        
        if len(cards) == 0:
            raise errors.NoCardsToReviewError("No cards to review in this deck")
        
        try:
            self.deck.last_reviewed_card = self.deck.reviewing_card

            # Select random unseen card
            if self.deck.prioritize_unseen and len(self.new_cards()) > 0:
                self.deck.reviewing_card = random.choice(self.new_cards())

            # Avoid asking twice the same card in a row
            elif self.deck.consecutive_never_identical:
                while self.deck.reviewing_card == self.deck.last_reviewed_card:
                    self.deck.reviewing_card = random.choice(cards)
            
            # Select random card in deck
            else:
                self.deck.reviewing_card = random.choice(cards)

        except models.Card.DoesNotExist:
            # Maybe it was deleted in the meantine
            self.deck.reviewing_card = random.choice(cards)
        self.deck.save()

        return self.deck.reviewing_card



class Ebisu(Algorithm):

    # TODO make customizable
    INITIAL_ALPHA = 3.0
    INITIAL_BETA = 3.0
    INITIAL_T = 3.0
    HALF_LIFE_UNIT = timedelta(hours=1)

    dynamic_fields = []
    
    def __init__(self, deck: 'Deck'):
        # Validate
        if deck.algorithm != "Ebisu":
            raise ValueError("Deck algorithm does not match Ebisu: {}".format(deck.algorithm))

        for field in Ebisu.dynamic_fields:
            if field not in deck._dynamic_fields:
                raise ValueError("Deck is missing Ebisu's dynamic field: {}".format(field))

        super(Algorithm, self).__init__()
        self.deck = deck

    def add_fields_to_deck(self, value):
        value["cards_to_review"] = len(self.cards_to_review())
        value["new_cards"] = len(self.new_cards())
        return value

    def add_fields_to_card(self, card, value):
        value["recall_probability"] = self.recall_probability(card)
        return value
    
    def recall_probability(self, card, exact=True):
        if card.last_review is None:
            return 0
        time_from_last_review = datetime.now() - card.last_review.review_time
        recall_probability = ebisu.predictRecall(prior=(card.last_review.alpha, card.last_review.beta, card.last_review.t*self.HALF_LIFE_UNIT), 
                                                tnow=time_from_last_review, 
                                                exact=exact) # Normalizes the output to a real probability.
        return recall_probability*100

    def export_to_file(self) -> str:
        """ Returns the path to a zipped file containing all the information needed to recreate a deck. """
        raise NotImplementedError("TODO in Ebisu")
    
    def cards_to_review(self) -> List["Card"]:
        """ 
        Returns the number of cards with less than 50% recall and at least one review 
        """
        cards = models.Card.objects(deck=self.deck.id).all()
        return [card for card in cards if card.last_review and self.recall_probability(card) < 0.5]

    def new_cards(self) -> List["Card"]:
        """ 
        Returns the number of unseen cards 
        """
        cards = models.Card.objects(deck=self.deck.id).all()
        return [card for card in cards if not card.last_review]

    def process_result(self, user_id: int, results: bool) -> None:
        """ 
        Saves a review with the test results (for eventual statistics) 
        """
        if not isinstance(results, bool):
            raise ValueError("Invalid test result for Ebisu: {}".format(results))
        
        user = models.User.objects.get(id=user_id)

        # Compute the prior or set defaults
        try:
            previous_model = self.get_card_model(self.deck.reviewing_card)
            time_from_last_review = datetime.now() - self.deck.reviewing_card.review_time
            
            alpha, beta, t = ebisu.updateRecall(prior=previous_model, 
                                                successes=bool(int(results)), 
                                                total=1, 
                                                tnow=time_from_last_review)
        
        except AttributeError:
            alpha = self.INITIAL_ALPHA
            beta = self.INITIAL_BETA
            t = self.INITIAL_T*self.HALF_LIFE_UNIT

        # Save review
        new_review = models.Review(
            alpha=alpha, 
            beta=beta,
            t=t/self.HALF_LIFE_UNIT, 
            user=user, 
            test_results=results, 
            review_time=datetime.utcnow(),
        )
        self.deck.reviewing_card.update(push__reviews=new_review)
        self.deck.reviewing_card.save()


    def next_card_to_review(self) -> 'Card':
        """ 
        Returns the card with the lowest recall probability.
        Gives automatically precedence to unseen cards, which have
        a default recall index of 0.
        """
        cards = models.Card.objects(deck=self.deck.id).all()
        next_card = min(cards, key=lambda card: self.recall_probability(card) )
        self.deck.last_reviewed_card = self.deck.reviewing_card
        self.deck.reviewing_card = next_card
        self.deck.save()
        return self.deck.reviewing_card



ALGORITHM_MAPPING = {
    "Random Order": RandomOrder,
    "Ebisu": Ebisu,
}


def algorithm_engine(deck: 'Deck') -> 'Algorithm':
    """ Given the algorithm name, returns a suitable engine """
    try:
        return ALGORITHM_MAPPING[deck.algorithm](deck)
    except KeyError:
        raise ValueError("Algorithm name unknown: {}".format(deck.algorithm))


def import_from_file(file_path: str) -> 'Deck':
    """ Loads a new deck from a .zip file and adds it to the decks list. """
    raise NotImplementedError("TODO")
