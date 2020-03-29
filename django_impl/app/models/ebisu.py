from django.db import models

from app.models.abc import *


class EbisuDeck(AbstractDeck):
    
    def import_from_file(self, packaged_file, private=False):
        """ Loads a new deck from a .zip file and adds it to the decks list. """
        pass

    def export_to_file(self):
        """ Returns a zipped file containing all the information needed to recreate a deck. """
        pass

    def next_card_to_review(self):
        """ Computes which is the next card to be reviewed. """
        pass

    def last_reviewed_card(self):
        """ Return the last card that has been reviewed. """
        pass

    def filter_cards(self, filter):
        """ Apply the filtering function to the cards list. """
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Ebisu Deck #{}: '{}'".format(self.id, self.name)


class EbisuCard(AbstractCard):
    
    def recall_index(self) -> float:
        """ Returns any value that can be compared to other cards to figure out which is the next card to review"""
        pass

    def update_model(self, tests_result) -> None:
        """ Creates or updates the card model. """
        pass
    
    def amend_last_update(self, amended_test_result) -> None:
        """ Replace the effect of the last update by replacing it with the new values. """

    def __str__(self):
        return "{}: {}".format(self.id, self.question)

    def __repr__(self):
        return "Ebisu Card #{}".format(self.id)


class EbisuCardModel(AbstractModel):
    test_result = models.BooleanField()
    alpha = models.FloatField()
    beta = models.FloatField()
    t = models.FloatField()

    def __str__(self):
        return "Card #{}: User {} at {}".format(self.id, self.user, self.review_time)

    def __repr__(self):
        return "Ebisu Card Model #{}".format(self.id)

