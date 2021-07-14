import os
import json

from flask import Response, request
from flask_restful import Resource
import flask_jwt_extended as jwt

from ebisu_flashcards.database.models import Deck
from ebisu_flashcards.operations.decks import DeckOps
from ebisu_flashcards.operations.serialization import Serializer


class DecksApi(DeckOps, Serializer, Resource):

    @jwt.jwt_required
    def get(self):
        user_id = jwt.get_jwt_identity()
        try:
            decks_list = self.get_deck(user_id, 'all')
            decks = self.serialize_list(decks_list)
            return Response(decks, mimetype="application/json", status=200)
            
        except Deck.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=404)


    @jwt.jwt_required
    def post(self):
        user_id = jwt.get_jwt_identity()
        data = request.get_json()
        db_deck = self.create_deck(user_id, data)
        deck = self.serialize_one(db_deck)
        return Response(deck, mimetype="application/json", status=200)


class DeckApi(DeckOps, Serializer, Resource):

    @jwt.jwt_required
    def get(self, deck_id):
        user_id = jwt.get_jwt_identity()
        try:
            db_deck = self.get_deck(user_id, deck_id)
            deck = self.serialize_one(db_deck)
            return Response(deck, mimetype="application/json", status=200)

        except Deck.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=404)
            

    @jwt.jwt_required
    def put(self, deck_id):
        user_id = jwt.get_jwt_identity()
        data = request.get_json()
        try:
            db_deck = self.update_deck(user_id, deck_id, data)
            deck = self.serialize_one(db_deck)
            return Response(deck, mimetype="application/json", status=200)

        except Deck.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=404)


    @jwt.jwt_required
    def delete(self, deck_id):
        user_id = jwt.get_jwt_identity()
        try:
            self.delete_deck(user_id, deck_id)
            return Response(json.dumps(None), mimetype="application/json", status=200)

        except Deck.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=404)
