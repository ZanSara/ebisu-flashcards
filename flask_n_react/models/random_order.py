from typing import Any, Callable, Mapping, Optional

import random
import mongoengine as mongo
from marshmallow import Schema, fields, post_load

from .base import Deck, Tag, User, Review, Card, BOOLEAN_WIDGET


class RandomOrderReview(Review):
    pass
    
    # class RandomOrderReviewSchema(Review.ReviewSchema):
        
    #     @post_load
    #     def make_random_order_review(self, data, **kwargs):
    #         return RandomOrderReview(**data)


class RandomOrderCard(Card):

    # class RandomOrderCardSchema(Card.CardSchema):
    #     reviews = fields.Nested(RandomOrderReview.RandomOrderReviewSchema, many=True)
    #     last_review = fields.Nested(RandomOrderReview.RandomOrderReviewSchema)

    #     @post_load
    #     def make_random_order_card(self, data, **kwargs):
    #         return RandomOrderCard(**data)

    def load_from_postdata(self, postdata: Mapping[str, Any]) -> None :
        super().load_from_postdata(postdata)


class RandomOrderDeck(Deck):
    ALGORITHM_NAME = "Random Order"
    CARD_TYPE = RandomOrderCard

    prioritize_unseen_cards = mongo.BooleanField(default=True)
    prevent_two_identical_questions = mongo.BooleanField(default=True)

    @property
    def cards_to_review(self) -> int:
        """ Return number of seen cards """
        return len([card for card in self.cards if card.last_review])

    @property
    def new_cards(self) -> int:
        """ Returns number of unseen cards """
        return len([card for card in self.cards if not card.last_review])


    # class RandomOrderDeckSchema(Deck.DeckSchema):
    #     last_reviewed_card = fields.Nested(RandomOrderCard.RandomOrderCardSchema)
    #     currently_reviewing_card = fields.Nested(RandomOrderCard.RandomOrderCardSchema)
    #     cards = fields.Nested(RandomOrderCard.RandomOrderCardSchema, many=True)
    #     propritize_unseen_cards = fields.Bool()
    #     prevent_two_identical_questions = fields.Bool()

    #     @post_load
    #     def make_random_order_deck(self, data, **kwargs):
    #         return RandomOrderDeck(**data)


    @staticmethod
    def create_from_postdata(postdata) -> int:
        new_deck = RandomOrderDeck()
        new_deck = Deck.populate_fields_from_postdata(new_deck, postdata)
        new_deck.save()
        return new_deck.id

    def update_from_postdata(self, postdata) -> None:
        Deck.populate_fields_from_postdata(self, postdata)
        self.save()
    
    def import_from_file(self, packaged_file, private=False):
        raise NotImplementedError("TODO in RandomOrderDeck")

    def export_to_file(self):
        raise NotImplementedError("TODO in RandomOrderDeck")
    
    def filter_cards(self, filter: Callable):
        raise NotImplementedError("TODO in RandomOrderDeck")

    def process_result(self, card: 'RandomOrderCard', user: User, test_results: Any) -> None:
        review = RandomOrderReview(
            user=user, 
            test_results=test_results, 
            review_time=timezone.now
        )
        card.reviews.append(review)
        card.save()

    def next_card_to_review(self) -> 'RandomOrderCard':
        try:
            self.last_card = self.current_card
            # To avoid asking twice the same card in a row
            while self.current_card == self.last_card:
                self.current_card = random.choice(self.cards)
        except mongo.DoesNotExist:
            # Maybe it was deleted in the meantime
            self.current_card = random.choice(self.cards)
        self.save()
        return self.current_card

    def filter_cards(self, filter: Callable):
        raise NotImplementedError("TODO in RandomOrderDeck")
