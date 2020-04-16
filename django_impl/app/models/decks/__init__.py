from .base import Deck
from .random_order import RandomOrderDeck


DECK_CLASSES = {
    RandomOrderDeck.ALGORITHM_NAME: RandomOrderDeck,
}


def create_deck_from_postdata(postdata) -> int:
    deck_class = DECK_CLASSES[postdata.get("algorithm")]
    return deck_class.create_from_postdata(postdata)
