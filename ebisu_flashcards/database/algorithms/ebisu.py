from typing import List, Tuple

import logging
from datetime import datetime, timedelta

import ebisu
import mongoengine

from ebisu_flashcards import errors
from ebisu_flashcards.database import db
from ebisu_flashcards.database.models import User, Deck, Card, Review
from ebisu_flashcards.database.algorithms.algorithm import Algorithm


class Ebisu(Algorithm):

    DEFAULT_ALPHA = 3.0
    DEFAULT_BETA = 3.0
    DEFAULT_T = 3.0
    DEFAULT_HALF_LIFE_UNIT = timedelta(hours=1)

    dynamic_fields = ['initial_alpha', 'initial_beta', 'initial_t', 'half_life_unit']
    
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

        model, time_from_last_review = self.get_card_model(card)

        recall_probability = ebisu.predictRecall(prior=model,
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
        cards = Card.objects(deck=self.deck.id).all()
        return [card for card in cards if card.last_review and self.recall_probability(card) < 0.5]

    def new_cards(self) -> List["Card"]:
        """ 
        Returns the number of unseen cards 
        """
        cards = Card.objects(deck=self.deck.id).all()
        return [card for card in cards if not card.last_review]

    def process_result(self, user_id: int, results: bool) -> None:
        """ 
        Saves a review with the test results (for eventual statistics) 
        """
        if not isinstance(results, bool):
            raise ValueError("Invalid test result for Ebisu: {}".format(results))
        
        user = User.objects.get(id=user_id)

        # Compute the prior
        alpha, beta, t = None, None, None
        try:
            if self.deck.reviewing_card.last_review:
                previous_model, time_from_last_review = self.get_card_model(self.deck.reviewing_card)
                alpha, beta, t = ebisu.updateRecall(prior=previous_model, 
                                                    successes=int(results), 
                                                    total=1, 
                                                    tnow=time_from_last_review)
        
        except AssertionError as e:
            logging.error("Assertion Error on card "+ str(self.deck.reviewing_card) +": ", e)
            
        finally:
            if (alpha, beta, t) == (None, None, None):
                # Set defaults if this is the first review
                alpha = self.deck.initial_alpha
                beta = self.deck.initial_beta
                t = self.deck.initial_t

        # Save review
        new_review = Review(
            alpha=alpha, 
            beta=beta,
            t=t, 
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
        cards = Card.objects(deck=self.deck.id).all()
        try:
            next_card = min(cards, key=lambda card: self.recall_probability(card) )
        except ValueError:
            raise errors.NoCardsToReviewError("There are no cards in this deck")

        try:
            reviewing_card = self.deck.reviewing_card
            self.deck.update(last_reviewed_card=reviewing_card)
            
        except mongoengine.errors.DoesNotExist as e:
            # This is not very critical, just keep going
            logging.error(e)

        self.deck.update(reviewing_card=next_card)
        self.deck.save()

        return next_card


    def get_card_model(self, card: 'Card') -> Tuple[Tuple[float, float, float], float]:
        """
            Given a card, computes its Ebisu model.
            :param card: the card we need the model of
            :returns: a nested tuple ((alpha:float, beta:float, t:float), tnow:float)
            :raises ValueError if the card has never been reviewed before
        """
        half_life_timedelta = timedelta(minutes=float(self.deck.half_life_unit))

        if not card.last_review:
            raise ValueError("No Card Model: the card has no reviews")

        alpha = float(card.last_review.alpha)
        beta = float(card.last_review.beta), 
        t = float(card.last_review.t) #* float(self.deck.half_life_unit) 
        tnow = (datetime.now() - card.last_review.review_time) / half_life_timedelta
        
        return (alpha, beta, t), tnow
        


