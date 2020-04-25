from typing import Any, Type, Optional

import json
from flask import request
from flask_restful import abort, Resource

from .models import Deck, Card, Renderer, User, create_deck_from_postdata, DECK_CLASSES
from .models.mongoengine_marshmallow_converter import mongo_to_marsh


def get_default_user_or_create() -> User:
    """ DEBUG METHOD """
    try:
        return User.objects.get(username="tester")
    except Exception as e:
        User(username="tester", password=b"fakepassword", email="me@email.com").save()
        return User.objects.get(username="tester")


def get_object_or_404(model_class: Type, id: str) -> Optional[Any]:
    """ Either gets the object from mongoengine or raises a 404"""
    instance = model_class.objects.get(id=id)
    if not instance:
        abort(404, message="Object of type '{}' with id '{}' doesn't exist".format(model_class, id))
    return instance


class AuthenticationApi(Resource):
    def put(self):
        # Login a user
        return {}

    def post(self):
        # Register new user
        return {}

    def get(self):
        # Recover password?
        return {}


class StudyApi(Resource):
    
    def get(self):
        # Return next card to study
        deck = Deck.objects.get(id=self.deck_id)
        card = Card.objects.get(id=self.card_id)
        return {
            'navbar_title': deck.name,
            # 'navbar_right': "## cards studied in this session",
            'card': card,
        }

    def put(self):
        # Update model and save 
        deck = Deck.objects.get(id=self.deck_id)
        card = Card.objects.get(id=self.card_id)
        deck.process_result(card=card, user=get_default_user_or_create(), test_results=request.POST.get("test_result"))
        return {}

class HomeApi(Resource):

    def get(self):
        # Get decks list    
        decks = Deck.objects.all()

        # make a decorator for this
        schema = Deck.JsonSchema(many=True)
        marshalled_decks = schema.dump(decks)
        return marshalled_decks


class DeckApi(Resource):

    def get(self, deck_id):
        deck = get_object_or_404(Deck, id=deck_id)

        schema = Deck.DeckSchema()
        marshalled_deck = schema.dump(deck)
        return marshalled_deck

    def post(self):
        # Save new deck and go back to home
        # parser = reqparse.RequestParser()
        # parser.add_argument('name', type=str, help="New deck's name")
        # parser.add_argument('description', type=str, help="New deck's description")
        # parser.add_argument('algorithm', type=str, help="New deck's algorithm")
        # args = parser.parse_args()  
        # create_deck_from_postdata(args)
        print(request.form)
        schema = Deck.DeckSchema()
        deck = schema.load(request.form)
        deck.save()
        return deck

    def put(self, deck_id):
        # Update deck information
        deck = get_object_or_404(Deck, id=deck_id)
        deck.update_from_postdata(request.POST)
        return {}

    def delete(self, deck_id):
        # Delete deck
        deck = get_object_or_404(Deck, id=deck_id)
        deck.delete()
        return {}


class CardApi(Resource):

    def get(self):
        deck = get_object_or_404(Deck, id=self.deck_id)
        renderers = Renderer.objects.all()
        return {
            'navbar_title': 'Cards List of "{}"'.format(deck.name),
            'deck': deck,
            'renderers': renderers,
            'cards': cards,
        }

    def post(self):
        deck = get_object_or_404(Deck, id=self.deck_id)
        new_card = deck.CARD_TYPE()
        new_card.load_from_postdata(request.POST)
        new_card.deck = deck
        new_card.save()
        return {}

    def put(self):
        deck = get_object_or_404(Deck, id=self.deck_id)
        card = get_object_or_404(Card, id=self.card_id)
        card.load_from_postdata(request.POST)
        card.save()
        return {}

    def delete(self):
        card = get_object_or_404(Card, id=self.card_id)
        if str(card.deck.id) == deck_id:
            card.delete()
            return {}
        abort(404, 'Card does not belong to deck')