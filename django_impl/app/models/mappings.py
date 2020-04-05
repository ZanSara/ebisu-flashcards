from .ebisu import EbisuDeck, EbisuCard, EbisuCardModel
from .random_order import RandomOrderDeck, RandomOrderCard, RandomOrderCardModel


CARD_TYPE_BY_DECK = {
    EbisuDeck: EbisuCard,
    RandomOrderDeck: RandomOrderCard,
}

CARD_MODEL_BY_CARD = {
    EbisuCard: EbisuCardModel,
    RandomOrderCard: RandomOrderCardModel,
}