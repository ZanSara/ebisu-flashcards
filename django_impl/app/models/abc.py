import abc

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from .base import Tag, CardLayout


class AbstractModel(models.Model):
    class Meta(abc.ABCMeta):
        abstract = True


class AbstractDeck(AbstractModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    default_layout = models.ForeignKey(CardLayout, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag)

    @abc.abstractmethod
    def import_from_file(self, packaged_file, private=False):
        """ Loads a new deck from a .zip file and adds it to the decks list. """
        pass

    @abc.abstractmethod
    def export_to_file(self):
        """ Returns a zipped file containing all the information needed to recreate a deck. """
        pass

    @abc.abstractmethod
    def next_card_to_review(self):
        """ Computes which is the next card to be reviewed. """
        pass

    @abc.abstractmethod
    def last_reviewed_card(self):
        """ Return the last card that has been reviewed. """
        pass

    @abc.abstractmethod
    def filter_cards(self, filter):
        """ Apply the filtering function to the cards list. """
        pass


class AbstractCard(AbstractModel):
    question = models.CharField(max_length=2000)
    answer = models.CharField(max_length=2000)
    deck_id = models.ForeignKey(AbstractDeck, on_delete=models.CASCADE)
    layout = models.ForeignKey(CardLayout, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    marked = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    @abc.abstractmethod
    def recall_index(self) -> float:
        """ Returns any value that can be compared to other cards to figure out which is the next card to review"""
        pass

    @abc.abstractmethod
    def update_model(self, tests_result) -> None:
        """ Creates or updates the card model. """
        pass
    
    @abc.abstractmethod
    def amend_last_update(self, amended_test_result) -> None:
        """ Replace the effect of the last update by replacing it with the new values. """


class AbstractCardModel(AbstractModel):
    card = models.ForeignKey(AbstractCard, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_time = models.DateTimeField(default=timezone.now)
