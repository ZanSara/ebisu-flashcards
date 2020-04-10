from app.models.ebisu import EbisuDeck, EbisuCard, EbisuCardModel
from app.models.random_order import RandomOrderDeck, RandomOrderCard, RandomOrderCardModel
from app.forms.ebisu import EbisuDeckForm, EbisuCardForm, EbisuCardModelForm
from app.forms.random_order import RandomOrderDeckForm, RandomOrderCardForm, RandomOrderCardModelForm


CARD_TYPE_BY_DECK = {
    EbisuDeck: EbisuCard,
    RandomOrderDeck: RandomOrderCard,
}

FORM_TYPE_BY_CARD = {
    EbisuCard: EbisuCardForm,
    RandomOrderCard: RandomOrderCardForm,
}

CARD_MODEL_BY_CARD = {
    EbisuCard: EbisuCardModel,
    RandomOrderCard: RandomOrderCardModel,
}