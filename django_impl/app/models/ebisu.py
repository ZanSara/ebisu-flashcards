from typing import Any, Callable, Mapping, Optional

import random
import ebisu
from datetime import datetime, timedelta
import mongoengine as mongo
from django.utils import timezone

from .base import Deck, Tag, User, Review, Card, BOOLEAN_WIDGET


HALF_LIFE_UNIT = timedelta(hours=1)


class EbisuReview(Review):
    alpha = mongo.DecimalField(default=3.0)
    beta = mongo.DecimalField(default=3.0)
    t = mongo.DecimalField(default=3.0)

    def to_ebisu_model(self):
        return (float(self.alpha), float(self.beta), float(self.t)*HALF_LIFE_UNIT)


class EbisuCard(Card):

    @property
    def extra_info(self):
        return {
            "Recall Index": "{}%".format(self.recall_index()*100)
        }

    def load_from_postdata(self, postdata: Mapping[str, Any]) -> None :
        super().load_from_postdata(postdata)

    def to_widgets(self):
        parent_form = super().to_widgets()
        own_form = {}
        own_form.update(parent_form)
        return own_form

    def process_result(self, user, test_results):
        if not self.last_review:
            new_review = EbisuReview(
                alpha=3.0, 
                beta=3.0,
                t=3.0, 
                user=user, 
                test_results=test_results, 
                review_time=timezone.now,
            )
            self.reviews.append(new_review)
            self.save()
            return

        time_from_last_review = datetime.now() - self.last_review.review_time
        # try:
        alpha, beta, t = ebisu.updateRecall(prior=self.last_review.to_ebisu_model(), 
                                            successes=bool(int(test_results)), 
                                            total=1, 
                                            tnow=time_from_last_review)
        new_review = EbisuReview(
            alpha=alpha, 
            beta=beta,
            t=t/HALF_LIFE_UNIT, 
            user=user, 
            test_results=test_results, 
            review_time=timezone.now,
        )
        self.reviews.append(new_review)
        self.save()
        # except AssertionError as ae:
        #     raise AssertionError("Card was not updated: {}".format(ae))

    def recall_index(self):
        if not self.last_review:
            return 0
        time_from_last_review = datetime.now() - self.last_review.review_time
         # The exact flag normalizes the output to a real probability.
        recall_probability = ebisu.predictRecall(prior=self.last_review.to_ebisu_model(), 
                                                 tnow=time_from_last_review, 
                                                 exact=True)
        return recall_probability


class EbisuDeck(Deck):
    ALGORITHM_NAME = "Ebisu"
    CARD_TYPE = EbisuCard

    current_card = mongo.ReferenceField('EbisuCard')
    last_card = mongo.ReferenceField('EbisuCard')

    @property
    def settings(self):
        return {}

    @staticmethod
    def create_from_postdata(postdata) -> int:
        new_deck = EbisuDeck()
        new_deck = Deck.populate_fields_from_postdata(new_deck, postdata)
        new_deck.save()
        return new_deck.id

    def update_from_postdata(self, postdata) -> None:
        Deck.populate_fields_from_postdata(self, postdata)
        self.save()
    
    def import_from_file(self, packaged_file, private=False):
        raise NotImplementedError("TODO in EbisuDeck")

    def export_to_file(self):
        raise NotImplementedError("TODO in EbisuDeck")
    
    def filter_cards(self, filter: Callable):
        raise NotImplementedError("TODO in EbisuDeck")

    def process_result(self, card: 'EbisuCard', user: User, test_results: Any) -> None:
        card.process_result(user, test_results)

    def next_card_to_review(self) -> 'EbisuCard':
        next_card = min(self.cards, key=lambda card: card.recall_index() )
        self.last_card = self.current_card
        self.current_card = next_card
        return self.current_card

    def last_reviewed_card(self) -> 'EbisuCard':
        raise NotImplementedError("TODO in EbisuDeck")

    def filter_cards(self, filter: Callable):
        raise NotImplementedError("TODO in EbisuDeck")

    @property
    def cards_to_review(self) -> int:
        """ Return number of seen cards """
        return len([card for card in self.cards if card.recall_index() < 0.5])

    @property
    def new_cards(self) -> int:
        """ Returns number of unseen cards """
        return len([card for card in self.cards if not card.last_review])
