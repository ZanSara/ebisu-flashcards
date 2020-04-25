from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
import mongoengine as mongo

from database.models import Deck, User


class DecksApi(Resource):
    def get(self):
        query = Deck.objects()
        decks = Deck.objects().to_json()
        print(decks)
        return Response(decks, mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        body = request.get_json()
        user = User.objects.get(id=user_id)
        deck = Deck(**body, author=user)
        deck.save()
        user.update(push__decks=deck)
        user.save()
        id = deck.id
        return {'id': str(id)}, 200


class DeckApi(Resource):
    def get(self, id):
        deck = Deck.objects.get(id=id).to_json()
        return Response(deck, mimetype="application/json", status=200)
            
    @jwt_required
    def put(self, id):
        user_id = get_jwt_identity()
        deck = Deck.objects.get(id=id, author=user_id)
        body = request.get_json()
        Deck.objects.get(id=id).update(**body)
        return '', 200      
    
    @jwt_required
    def delete(self, id):
        user_id = get_jwt_identity()
        deck = Deck.objects.get(id=id, author=user_id)
        deck.delete()
        return '', 200
