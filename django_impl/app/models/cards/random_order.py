from typing import Any, Mapping
import abc
import mongoengine as mongo
from django.utils import timezone

from .base import Review, Card


class RandomOrderReview(Review):
    pass

class RandomOrderCard(Card):
    
    def populate_fields_from_postdata(self, postdata: Mapping[str, Any]) -> None:
        super().populate_fields_from_postdata(postdata)

    def update_from_postdata(self, postdata: Mapping[str, Any]) -> None :
        self.populate_fields_from_postdata(postdata)
        self.save()

    def to_dict(self):
        parent_dict = super().to_dict()
        own_dict = {}
        own_dict.update(parent_dict)
        return own_dict

    def to_widgets(self):
        parent_form = super().to_widgets()
        own_form = {}
        own_form.update(parent_form)
        return own_form