from typing import Any, Callable

import mongoengine as mongo

from .base import Deck
from ..base import Tag, Card


class RandomOrderDeck(Deck):
    ALGORITHM_NAME = "Random Order"

    @staticmethod
    def create_from_request(postdata) -> int:
        new_deck = RandomOrderDeck()
        new_deck = Deck.populate_fields_from_postdata(new_deck, postdata)
        new_deck.save()
        return new_deck.id

    def update_from_request(self, postdata) -> None:
        Deck.populate_fields_from_postdata(self, postdata)
        self.save()
    
    def import_from_file(self, packaged_file, private=False):
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")

    def export_to_file(self):
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")
    
    def filter_cards(self, filter: Callable):
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")

    def to_dict(self):
        base_fields = super().to_dict()
        all_fields = {
            'algorithm': self.ALGORITHM_NAME,
            'cards_to_review': self.cards_to_review,
            'new_cards': self.new_cards,
        }
        all_fields.update(base_fields)
        return all_fields

    def process_result(self, card_id: int, user_id: int, test_results: Any) -> None:
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")


    def next_card_to_review(self) -> 'Card':
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")


    def last_reviewed_card(self) -> 'Card':
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")

    def filter_cards(self, filter: Callable):
        raise NotImplementedError("Can't use Deck base class: use one of the subclasses")

    @property
    def cards_to_review(self) -> int:
        return 0

    @property
    def new_cards(self) -> int:
        return 0
