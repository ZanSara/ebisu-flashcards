import json 

from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
import mongoengine as mongo

from database import models, algorithms


class StudyApi(Resource):
    @jwt_required
    def get(self, deck_id):
        user_id = get_jwt_identity()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        algorithm = algorithms.algorithm_engine(deck)
        next_card = algorithm.next_card_to_review().to_json()
        return Response(next_card, mimetype="application/json", status=200)

    @jwt_required
    def post(self, deck_id):
        user_id = get_jwt_identity()
        body = request.get_json()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        algorithm = algorithms.algorithm_engine(deck)
        algorithm.process_result(**body, user_id=user_id)
        # Return directly the next card to review
        next_card = algorithm.next_card_to_review().to_json()
        return Response(next_card, mimetype="application/json", status=200)


class DecksApi(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        try:
            query = models.Deck.objects(author=user_id)
            decks = query.to_json()
            return Response(decks, mimetype="application/json", status=200)
        except models.Deck.DoesNotExist:
            return Response("{}", mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        body = request.get_json()
        user = models.User.objects.get(id=user_id)
        deck = models.Deck(**body, author=user)
        deck.save()
        user.update(push__decks=deck)
        user.save()
        return {'id': str(deck.id)}, 200


class DeckApi(Resource):
    @jwt_required
    def get(self, deck_id):
        user_id = get_jwt_identity()
        deck = models.Deck.objects.get(id=deck_id, author=user_id).to_json()
        return Response(deck, mimetype="application/json", status=200)
            
    @jwt_required
    def put(self, deck_id):
        user_id = get_jwt_identity()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        body = request.get_json()
        deck.update(**body)
        return '', 200      
    
    @jwt_required
    def delete(self, deck_id):
        user_id = get_jwt_identity()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        deck.delete()
        return '', 200


class CardsApi(Resource):
    @jwt_required
    def get(self, deck_id):
        user_id = get_jwt_identity()
        try:
            deck = models.Deck.objects.get(id=deck_id, author=user_id)
            cards = models.Card.objects(deck=deck_id).to_json()
            return Response(cards, mimetype="application/json", status=200)

        except models.Deck.DoesNotExist:
            return Response("{}", mimetype="application/json", status=200)

    @jwt_required
    def post(self, deck_id):
        user_id = get_jwt_identity()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        body = request.get_json()
        card = models.Card(**body, deck=deck.id)
        card.save()
        # deck.update(push__cards=card)
        # deck.save()
        return {'id': str(card.id)}, 200


class CardApi(Resource):
    @jwt_required
    def get(self, deck_id, card_id):
        user_id = get_jwt_identity()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)  # Ensure the deck belongs to this user before proceeding
        card = models.Card.objects.get(id=card_id).to_json()
        return Response(card, mimetype="application/json", status=200)
            
    @jwt_required
    def put(self, deck_id, card_id):
        user_id = get_jwt_identity()
        body = request.get_json()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        card = models.Card.objects.get(id=card_id)
        if deck.id == card.deck:
            card.update(**body)
            return '', 200   
        else:
            raise ValueError("Card does not belong to deck")   
    
    @jwt_required
    def delete(self, deck_id, card_id):
        user_id = get_jwt_identity()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        card = models.Card.objects.get(id=card_id, deck=deck_id)
        card.delete()
        return '', 200


class TemplatesApi(Resource):
    @jwt_required
    def get(self):
        try:
            templates = models.Template.objects().to_json()
            return Response(templates, mimetype="application/json", status=200)
        except models.Template.DoesNotExist:
            return Response("{}", mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        body = request.get_json()
        template = models.Template(**body)
        template.save()
        return {'id': str(template.id)}, 200


class TemplateApi(Resource):
    @jwt_required
    def get(self, template_id):
        template = models.Template.objects.get(id=template_id).to_json()
        return Response(template, mimetype="application/json", status=200)
            
    @jwt_required
    def put(self, template_id):
        body = request.get_json()
        template = models.Template.objects.get(id=template_id)
        template.update(**body)
        return '', 200   
    
    @jwt_required
    def delete(self, template_id):
        card = models.Template.objects.get(id=template_id)
        card.delete()
        return '', 200


class AlgorithmsApi(Resource):
    @jwt_required
    def get(self):
        names = json.dumps(list(algorithms.ALGORITHM_MAPPING.keys()))
        return Response(names, mimetype="application/json", status=200)

