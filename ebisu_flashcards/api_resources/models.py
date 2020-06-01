import os
import json 
import bson

from flask import Response, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
import mongoengine as mongo

from database import models, algorithms



class CardResource(Resource):

    def serialize(self, db_card):
        # Server Side question and answer blocks rendering
        question_path = os.path.join("card-templates", db_card.question_template.path)
        db_card.question_display = render_template(question_path, content=db_card.question)

        answer_path = os.path.join("card-templates", db_card.answer_template.path)
        db_card.answer_display = render_template(answer_path, content=db_card.answer)

        question_form_path = os.path.join("card-form-templates", db_card.question_template.path)
        db_card.question_form = render_template(question_form_path, name="question", content=db_card.question)

        answer_form_path = os.path.join("card-form-templates", db_card.answer_template.path)
        db_card.answer_form = render_template(answer_form_path, name="answer", content=db_card.answer)

        return db_card


    def serialize_cards(self, db_cards):
        json_cards = []
        for card in db_cards:
            card = self.serialize(card)
            card = card.to_mongo()
            json_cards.append(card)

        # Return serialized list
        return bson.json_util.dumps(json_cards)


    def serialize_card(self, db_card):
        card = self.serialize(db_card)
        return card.to_json()


    def deserialize(self, request):
        data = request.get_json()
        # Trasform template fields into references
        data["question_template"] = models.Template.objects.get(name=data["question_template"])
        data["answer_template"] = models.Template.objects.get(name=data["answer_template"])
        return data



class DeckResource(Resource):

    def serialize(self, db_deck):
        # Server Side extra form fields rendering
        template_path = os.path.join("deck-templates", db_deck.algorithm+".html")
        db_deck.extra_fields = render_template(template_path, deck=db_deck)
        return db_deck

    def serialize_decks(self, db_decks):
        json_decks = []
        for deck in db_decks:
            deck = self.serialize(deck)
            # Prepare for JSON serialization
            deck = deck.to_mongo()
            json_decks.append(deck)
        # Return serialized list
        return bson.json_util.dumps(json_decks)

    def serialize_deck(self, db_deck):
        deck = self.serialize(db_deck)
        return db_deck.to_json()


class StudyApi(CardResource):
    @jwt_required
    def get(self, deck_id):
        user_id = get_jwt_identity()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        
        algorithm = algorithms.algorithm_engine(deck)
        next_card = algorithm.next_card_to_review()

        next_card = self.serialize_card(next_card)
        return Response(next_card, mimetype="application/json", status=200)

    @jwt_required
    def post(self, deck_id):
        user_id = get_jwt_identity()
        body = request.get_json()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        algorithm = algorithms.algorithm_engine(deck)
        algorithm.process_result(**body, user_id=user_id)
        return '', 200



class DecksApi(DeckResource):

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        try:
            decks_list = models.Deck.objects(author=user_id).all()
            decks = self.serialize_decks(decks_list)
            return Response(decks, mimetype="application/json", status=200)
            
        except models.Deck.DoesNotExist:
            return Response("{}", mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        user = models.User.objects.get(id=user_id)
        
        data = request.get_json()
        deck = models.Deck(**data, author=user)
        deck.save()

        user.update(push__decks=deck)
        user.save()
        
        deck = self.serialize_deck(deck)
        return Response(deck, mimetype="application/json", status=200)


class DeckApi(DeckResource):
    @jwt_required
    def get(self, deck_id):
        user_id = get_jwt_identity()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        deck = self.serialize_deck(deck)
        return Response(deck, mimetype="application/json", status=200)
            
    @jwt_required
    def put(self, deck_id):
        user_id = get_jwt_identity()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        body = request.get_json()
        deck.update(**body)
        # Reload and serialize the new deck data
        deck = deck.reload()
        deck = self.serialize_deck(deck)
        return Response(deck, mimetype="application/json", status=200)
    
    @jwt_required
    def delete(self, deck_id):
        user_id = get_jwt_identity()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        deck.delete()
        return '', 200


class CardsApi(CardResource):
    @jwt_required
    def get(self, deck_id):
        user_id = get_jwt_identity()
        try:
            cards_list = models.Card.objects(deck=deck_id).all()
            cards = self.serialize_cards(cards_list)
            return Response(cards, mimetype="application/json", status=200)

        except models.Card.DoesNotExist:
            return Response("{}", mimetype="application/json", status=200)

    @jwt_required
    def post(self, deck_id):
        user_id = get_jwt_identity()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        data = self.deserialize(request)
        card = models.Card(**data, deck=deck)
        card.save()
        card.reload()
        card = self.serialize_card(card)
        return Response(card, mimetype="application/json", status=200)


class CardApi(CardResource):
    @jwt_required
    def get(self, deck_id, card_id):
        user_id = get_jwt_identity()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)  # Ensure the deck belongs to this user before proceeding
        db_card = models.Card.objects.get(id=card_id)
        card = self.serialize_card(db_card)
        return Response(card, mimetype="application/json", status=200)
            
    @jwt_required
    def put(self, deck_id, card_id):
        user_id = get_jwt_identity()
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        card = models.Card.objects.get(id=card_id)
        if deck.id == card.deck.id:
            data = self.deserialize(request)
            card.update(**data)
            card.save()
            card.reload()
            card = self.serialize_card(card)
            return Response(card, mimetype="application/json", status=200)
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
        return Response(template.reload().to_json(), mimetype="application/json", status=200)


class TemplateApi(Resource):
    @jwt_required
    def get(self, template_id):
        template = models.Template.objects.get(id=template_id).to_json()
        return Response(template.to_json(), mimetype="application/json", status=200)
            
    @jwt_required
    def put(self, template_id):
        body = request.get_json()
        template = models.Template.objects.get(id=template_id)
        template.update(**body)
        return Response(template.reload().to_json(), mimetype="application/json", status=200)
    
    @jwt_required
    def delete(self, template_id):
        card = models.Template.objects.get(id=template_id)
        card.delete()
        return '', 200


class AlgorithmsApi(Resource):
    @jwt_required
    def get(self):
        names = []
        for name, klass in algorithms.ALGORITHM_MAPPING.items():
            algorithm = {
                'name': name,
                'extra_fields': render_template(os.path.join("deck-templates", name+".html"), deck={})    
            }
            names.append(algorithm)
        return Response(json.dumps(names), mimetype="application/json", status=200)

