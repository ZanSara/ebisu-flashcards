import abc
from polymorphic.models import PolymorphicModel

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from .base import Tag, CardLayout

DEFAULT_CARD_LAYOUT = CardLayout.objects.get(id=1)


class AbstractModel(PolymorphicModel):
    class Meta(abc.ABCMeta):
        abstract = True


class AbstractDeck(AbstractModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    default_layout = models.ForeignKey(CardLayout, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    @abc.abstractmethod
    def import_from_file(self, packaged_file, private=False):
        """ Loads a new deck from a .zip file and adds it to the decks list. """
        pass

    @abc.abstractmethod
    def export_to_file(self):
        """ Returns a zipped file containing all the information needed to recreate a deck. """
        pass

    @abc.abstractmethod
    def to_dict(self):
        """ Returns a dictionary to be used in the views. """
        default_layout = DEFAULT_CARD_LAYOUT
        if self.default_layout:
            default_layout = self.default_layout
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'default_layout': default_layout.to_dict(),
            'tags': self.tags,
        }

    @abc.abstractmethod
    def update_card(self, card_id, test_results):
        """ Calls the updated method of the card, enriching the input data if needed. """
        card = get_object_or_404(AbstractCard, id=card_id)
        if card not in self.cards.all():
            raise ValueError("This card ({}) does not belong to this deck ({})!".format(card_id, self.id))

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

    @property
    @abc.abstractmethod
    def cards_to_review(self):
        """ Returns the number of cards to review according to some arbitrary rule set by the subclass """
        pass

    @property
    @abc.abstractmethod
    def new_cards(self):
        """ Returns the number of new cards according to some arbitrary rule set by the subclass """
        pass


class AbstractCard(AbstractModel):
    question = models.CharField(max_length=2000)
    answer = models.CharField(max_length=2000)
    deck = models.ForeignKey(AbstractDeck, on_delete=models.CASCADE, related_name='cards')
    layout = models.ForeignKey(CardLayout, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    marked = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    @abc.abstractmethod
    def to_dict(self):
        """ Returns a dictionary to be used in the views """
        if self.layout:
            default_layout = self.layout
        elif self.deck.default_layout:
            default_layout = self.deck.default_layout
        else:
            default_layout = DEFAULT_CARD_LAYOUT
        return {
            # No deck info for now
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'layout': default_layout.to_dict(),
            'tags': self.tags.all(),
            'marked': self.marked,
            'hidden': self.hidden,
        }

    @abc.abstractmethod
    def update_from_dict(self, new_values):
        """ 
            Updates the card's values by taking data from the dictionary. 
            Ignores extra keys. Right types are the caller's responsibility.
        """
        print(new_values)
        self.question = new_values.get("question", self.question)
        self.answer = new_values.get("answer", self.answer)
        try:
            self.layout = CardLayout.objects.get(name=new_values.get("layout"))
        except CardLayout.DoesNotExist:
            pass

        for tag in new_values.get("tags", []):
            try:
                self.tags.add(Tag.objects.get(name=tag))
            except Tag.DoesNotExist:
                pass
        
        self.marked = bool(new_values.get("marked", self.marked)) 
        self.hidden = bool(new_values.get("hidden", self.hidden))
        self.save()

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
    card = models.ForeignKey(AbstractCard, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    review_time = models.DateTimeField(default=timezone.now)

