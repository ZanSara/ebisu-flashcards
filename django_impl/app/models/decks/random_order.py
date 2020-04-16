from typing import Any, Callable, Mapping

import mongoengine as mongo

from .base import Deck
from ..base import Tag
from ..cards import RandomOrderCard


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

    def add_card(self, postdata: Mapping[str, Any]):
        new_card = self.CARD_TYPE()
        new_card.populate_fields_from_postdata(postdata)
        new_card.save()
        self.update(add_to_set__cards=[new_card])

    def process_result(self, card_id: int, user_id: int, test_results: Any) -> None:
        raise NotImplementedError("TODO in RandomOrderDeck")


    def next_card_to_review(self) -> 'Card':
        raise NotImplementedError("TODO in RandomOrderDeck")


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
