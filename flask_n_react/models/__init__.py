from .base import *
from .random_order import *
from .ebisu import *


DECK_CLASSES = {
    RandomOrderDeck.ALGORITHM_NAME: RandomOrderDeck,
    EbisuDeck.ALGORITHM_NAME: EbisuDeck,
}


def create_deck_from_postdata(postdata) -> int:
    deck_class = DECK_CLASSES[postdata.get("algorithm")]
    return deck_class.create_from_postdata(postdata)