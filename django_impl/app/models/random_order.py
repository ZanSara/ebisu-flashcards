from typing import Any, Callable, Mapping

import random
import mongoengine as mongo
from django.utils import timezone

from .base import Deck, Tag, User, Review, Card


class RandomOrderReview(Review):
    pass


class RandomOrderCard(Card):

    def load_from_postdata(self, postdata: Mapping[str, Any]) -> None :
        super().load_from_postdata(postdata)

    def to_dict(self):
        parent_dict = super().to_dict()
        own_dict = {}
        own_dict.update(parent_dict)
        return own_dict

    def to_widgets(self):
        parent_form = super().to_widgets()
        own_form = {}
        own_form.update(parent_form)
        return own_form


class RandomOrderDeck(Deck):
    ALGORITHM_NAME = "Random Order"
    CARD_TYPE = RandomOrderCard

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

    def to_dict(self):
        base_fields = super().to_dict()
        all_fields = {
            'algorithm': self.ALGORITHM_NAME,
            'cards_to_review': self.cards_to_review,
            'new_cards': self.new_cards,
        }
        all_fields.update(base_fields)
        return all_fields

    def process_result(self, card: 'RandomOrderCard', user: User, test_results: Any) -> None:
        card.reviews.create(
            user=user, 
            test_results=test_results, 
            review_time=timezone.now
        )

    def next_card_to_review(self) -> 'Card':
        return random.choice(self.cards)


    def last_reviewed_card(self) -> 'Card':
        raise NotImplementedError("TODO in RandomOrderDeck")

    def filter_cards(self, filter: Callable):
        raise NotImplementedError("TODO in RandomOrderDeck")

    @property
    def cards_to_review(self) -> int:
        return 0

    @property
    def new_cards(self) -> int:
        return 0
