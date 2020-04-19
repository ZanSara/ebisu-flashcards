from typing import Any, Callable, Mapping, Optional

import random
import mongoengine as mongo
from django.utils import timezone

from .base import Deck, Tag, User, Review, Card, BOOLEAN_WIDGET


class RandomOrderReview(Review):
    pass


class RandomOrderCard(Card):

    def load_from_postdata(self, postdata: Mapping[str, Any]) -> None :
        super().load_from_postdata(postdata)

    def to_widgets(self):
        parent_form = super().to_widgets()
        own_form = {}
        own_form.update(parent_form)
        return own_form


class RandomOrderDeck(Deck):
    ALGORITHM_NAME = "Random Order"
    CARD_TYPE = RandomOrderCard

    current_card = mongo.ReferenceField('RandomOrderCard')
    last_card = mongo.ReferenceField('RandomOrderCard')

    prioritize_unseen_cards = mongo.BooleanField(default=True)
    prevent_two_identical_cards = mongo.BooleanField(default=True)

    @property
    def settings(self):
        return {
            'prioritize_unseen_cards': {
                'value': self.prioritize_unseen_cards,
                'widget': BOOLEAN_WIDGET,
            },
            'prevent_two_identical_cards': {
                'value': self.prevent_two_identical_cards,
                'widget': BOOLEAN_WIDGET,
            },
        }

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

    def next_card_to_review(self) -> 'Card':
        try:
            self.last_card = self.current_card
            # To avoid asking twice the same card in a row
            while self.current_card == self.last_card:
                self.current_card = random.choice(self.cards)
        except mongo.DoesNotExist:
            # Maybe it was deleted in the meantine
            self.current_card = random.choice(self.cards)
        self.save()
        return self.current_card

    def last_reviewed_card(self) -> 'Card':
        raise NotImplementedError("TODO in RandomOrderDeck")

    def filter_cards(self, filter: Callable):
        raise NotImplementedError("TODO in RandomOrderDeck")

    @property
    def cards_to_review(self) -> int:
        """ Return number of seen cards """
        return len([card for card in self.cards if card.last_review])

    @property
    def new_cards(self) -> int:
        """ Returns number of unseen cards """
        return len([card for card in self.cards if not card.last_review])
