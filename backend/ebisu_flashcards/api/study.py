import os
import json

from flask import Response, request
from flask_restful import Resource
import flask_jwt_extended as jwt

from ebisu_flashcards.database.models import Deck
from ebisu_flashcards.operations.study import StudyOps
from ebisu_flashcards.operations.serialization import Serializer



class StudyApi(StudyOps, Serializer, Resource):

    @jwt.jwt_required
    def get(self, deck_id):
        user_id = jwt.get_jwt_identity()
        try:
            db_next_card = self.get_next_card(user_id, deck_id)
            next_card = self.serialize_one(db_next_card)
            return Response(next_card, mimetype="application/json", status=200)
        
        except Deck.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=404)


    @jwt.jwt_required
    def post(self, deck_id):
        user_id = jwt.get_jwt_identity()
        body = request.get_json()
        self.process_test_results(**body, user_id=user_id, deck_id=deck_id)
        return Response(json.dumps(None), mimetype="application/json", status=200)
