from datetime import datetime, timedelta
import ebisu

from django.db import models
from django.shortcuts import get_object_or_404

from app.models.abc import *

HALF_LIFE_UNIT = timedelta(hours=1)


class EbisuDeck(AbstractDeck):
    
    def import_from_file(self, packaged_file, private=False):
        """ Loads a new deck from a .zip file and adds it to the decks list. """
        pass

    def export_to_file(self):
        """ Returns a zipped file containing all the information needed to recreate a deck. """
        pass
    
    def update_card(self, card_id, test_results):
        super().update_card(card_id, test_results)
        card = get_object_or_404(EbisuCard, id=card_id)
        if not isinstance(test_results, bool):
            raise ValueError("Test results must be boolean (received {})".format(type(test_results)))
        card.update_model(test_results)


    def next_card_to_review(self) -> AbstractCard:
        """ Computes which is the next card to be reviewed. """
        next_card = min(self.cards.all(), key=lambda card: card.recall_index())
        return next_card

    def last_reviewed_card(self):
        """ Return the last card that has been reviewed. """
        pass

    def filter_cards(self, filter):
        """ Apply the filtering function to the cards list. """
        pass

    def to_dict(self):
        return super().to_dict()

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Ebisu Deck #{}: '{}'".format(self.id, self.name)


class EbisuCard(AbstractCard):

    def get_prior_data(self):
        """ Returns the data prepared for ebisu calls: the prior and the time from last review, scaled."""
        if len(self.reviews.all()) == 0:
            # FIXME deal with the case where the card is new!!!
            EbisuCardModel.objects.create(card=self, user=User.objects.get(id=1),  # FIXME get right user
                test_result=True, alpha=3.0, beta=3.0, t=3.0)

        last_model = max(self.reviews.all(), key=lambda model: model.review_time)
        time_from_last_review = (datetime.now(timezone.utc) - last_model.review_time) / HALF_LIFE_UNIT
        return last_model.to_ebisu_model(), time_from_last_review

    
    def recall_index(self) -> float:
        """ Returns any value that can be compared to other cards to figure out which is the next card to review"""
        last_model, review_time = self.get_prior_data()
         # The exact flag normalizes the output to a real probability
        recall_probability = ebisu.predictRecall(prior=last_model, 
                                                 tnow=review_time)
                                                 #exact=exact)
        return recall_probability

    def update_model(self, test_result) -> None:
        """ Creates or updates the card model. """
        last_model, review_time = self.get_prior_data()
        try:
            alpha, beta, t = ebisu.updateRecall(prior=last_model, 
                                                successes=test_result, 
                                                total=1, #reviews_in_this_session, 
                                                tnow=review_time)

            EbisuCardModel.objects.create(card=self, user=User.objects.get(id=1),  # FIXME get right user
                test_result=test_result, alpha=alpha, beta=beta, t=t)
            
        except AssertionError as ae:
            # FIXME find way to handle this, like popup, or silently ignore, or hide card...?
            print("Card was not updated: reached numerical instability!")

    
    def amend_last_update(self, amended_test_result) -> None:
        """ Replace the effect of the last update by replacing it with the new values. """

    def to_dict(self):
        return super().to_dict()

    def update_from_dict(self, new_values):
        values = {key: value for key, value in new_values.items()}
        del values["csrfmiddlewaretoken"]
        # FIXME do some checks?
        super().update_from_dict(values)

    def __str__(self):
        return "[{}] {}".format(self.deck.name, self.question)

    def __repr__(self):
        return "Ebisu Card #{}".format(self.id)


class EbisuCardModel(AbstractCardModel):
    test_result = models.BooleanField()
    alpha = models.FloatField()
    beta = models.FloatField()
    t = models.FloatField()

    def to_ebisu_model(self):
        return (self.alpha, self.beta, self.t)

    def __str__(self):
        return "{} @ {} [{}, {}]".format(self.user, self.review_time, self.card.deck.name, self.card.question)

    def __repr__(self):
        return "Ebisu Card Model #{}".format(self.id)

