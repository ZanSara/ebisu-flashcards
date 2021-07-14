import os
import json

from flask import Response, request
from flask_restful import Resource
import flask_jwt_extended as jwt

from ebisu_flashcards.database.models import Card, Deck
from ebisu_flashcards.operations.cards import CardOps
from ebisu_flashcards.operations.serialization import Serializer


class CardsApi(CardOps, Serializer, Resource):

    @jwt.jwt_required
    def get(self, deck_id):
        user_id = jwt.get_jwt_identity()
        try:
            cards_list = self.get_card(user_id, deck_id, 'all')
            cards = self.serialize_list(cards_list)
            return Response(cards, mimetype="application/json", status=200)

        except (Card.DoesNotExist, Deck.DoesNotExist):
            return Response(json.dumps(None), mimetype="application/json", status=404)


    @jwt.jwt_required
    def post(self, deck_id):
        user_id = jwt.get_jwt_identity()
        try:
            data = request.get_json()
            db_card = self.create_card(user_id, deck_id, data)
            card = self.serialize_one(db_card)
            return Response(card, mimetype="application/json", status=200)

        except Deck.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=404)


class CardApi(CardOps, Serializer, Resource):

    @jwt.jwt_required
    def get(self, deck_id, card_id):
        user_id = jwt.get_jwt_identity()
        try:
            db_card = self.get_card(user_id, deck_id, card_id)
            card = self.serialize_one(db_card)
            return Response(card, mimetype="application/json", status=200)

        except (Card.DoesNotExist, Deck.DoesNotExist):
            return Response(json.dumps(None), mimetype="application/json", status=404)
            

    @jwt.jwt_required
    def put(self, deck_id, card_id):
        user_id = jwt.get_jwt_identity()
        data = request.get_json()
        try:
            db_card = self.update_card(user_id, deck_id, card_id, data)
            card = self.serialize_one(db_card)
            return Response(card, mimetype="application/json", status=200)

        except (Card.DoesNotExist, Deck.DoesNotExist):
            return Response(json.dumps(None), mimetype="application/json", status=404)
            
    
    @jwt.jwt_required
    def delete(self, deck_id, card_id):
        user_id = jwt.get_jwt_identity()
        try:
            self.delete_card(user_id, deck_id, card_id)
            return Response(json.dumps(None), mimetype="application/json", status= 200)

        except (Card.DoesNotExist, Deck.DoesNotExist):
            return Response(json.dumps(None), mimetype="application/json", status=404)
