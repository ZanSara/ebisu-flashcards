from typing import List

import logging
import random
from datetime import datetime, timedelta

import mongoengine

from ebisu_flashcards import errors
from ebisu_flashcards.database import db
from ebisu_flashcards.database.models import User, Deck, Card, Review
from ebisu_flashcards.database.algorithms.algorithm import Algorithm


class RandomOrder(Algorithm):

    dynamic_fields = ["prioritize_unseen", "consecutive_never_identical"]

    def __init__(self, deck: 'Deck'):
        logging.debug("Instantiating RandomOrder Algorithm")

        # Validate
        if deck.algorithm != "Random Order":
            raise ValueError("Deck algorithm does not match Random Order: {}".format(deck.algorithm))

        for field in RandomOrder.dynamic_fields:
            if field not in deck._dynamic_fields:
                raise ValueError("Deck is missing Random Order's dynamic field: {}".format(field))

        super(Algorithm, self).__init__()
        self.deck = deck
        

    def add_fields_to_deck(self, value):
        """
            Add the new cards count to the deck
        """
        logging.debug("Adding New Cards count to the deck values")
        value["new_cards"] = len(self.new_cards())
        return value


    def add_fields_to_card(self, card, value):
        """
            No extra metadata is required for cards
        """
        logging.debug("No extra metadata is required for cards - return value unmodified")
        return value
        

    def export_to_file(self) -> str:
        """ 
            Returns the path to a zipped file containing all the information needed to recreate a deck. 
        """
        raise NotImplementedError("TODO in Random Order")
    

    def process_result(self, user_id: int, results: bool) -> None:
        """ 
            Saves a review with the test results (for statistics) 
        """
        if not isinstance(results, bool):
            raise ValueError("Invalid test result for Random Order: {}".format(results))
       
        try:
            logging.debug("Saving new Review for card ", self.deck.reviewing_card,
                          " with result ", results, " for user ", user_id, 
                          " at time ", datetime.utcnow())

            user = User.objects.get(id=user_id)
            review = Review(
                user=user, 
                test_results=results, 
                review_time=datetime.utcnow()
            )
            self.deck.reviewing_card.update(push__reviews=review)
            self.deck.reviewing_card.save()
        
        except mongoengine.errors.DoesNotExist as e:
            # Logs the issue, but it's not critical - just return
            logging.error("MongoEngine threw an exception!", e)
            logging.warning("Exception can be ignored, going ahead")
            pass


    def next_card_to_review(self) -> 'Card':
        """ 
            Picks a random card. 
            Avoids repeating the same card twice if so required and possible (i.e there is more than 1 card). 
            Gives priority to unseen cards if so required.
        """
        logging.debug("Finding next card to review")

        cards = Card.objects(deck=self.deck.id).all()
        if len(cards) == 0:
            raise errors.NoCardsToReviewError("No cards present in this deck")
        
        # Update last reviewed card field
        reviewing_card = self.deck.reviewing_card
        self.deck.update(last_reviewed_card=reviewing_card)
        
        # Select random unseen card, if unseen cards have priority
        new_cards = self.new_cards()
        if self.deck.prioritize_unseen and len(new_cards) > 0:
            reviewing_card = random.choice(new_cards)

        # Avoid asking twice the same card in a row if required and possible
        elif self.deck.consecutive_never_identical and len(cards) > 1:
            while reviewing_card == self.deck.last_reviewed_card:
                reviewing_card = random.choice(cards)

        # Last check to make sure we return a card in any case
        if not reviewing_card:
            reviewing_card = random.choice(cards)

        # Save and return
        self.deck.update(reviewing_card=reviewing_card)
        self.deck.save()
        self.deck.reload()
        return self.deck.reviewing_card


    def new_cards(self) -> List['Card']:
        """ 
            Returns the list of unseen cards 
        """
        cards = Card.objects(deck=self.deck.id).all()
        return [card for card in cards if not card.last_review]
