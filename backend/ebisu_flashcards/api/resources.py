import os
import time
import json
from functools import partial

from flask import Response, request, jsonify, render_template
from flask_restful import Resource
import flask_jwt_extended as jwt

from ebisu_flashcards.database import algorithms, models
from ebisu_flashcards.operations import auth, serialization, study, decks, cards, templates


class SignupApi(Resource):
    
    def post(self):
        body = request.get_json()
        idx = auth.signup(body)
        return {'id': str(idx)}, 200


class LoginApi(Resource):

    def post(self):
        # Create the tokens we will be sending back to the user
        body = request.get_json()
        access_token, refresh_token = auth.login(body.get('username'), body.get("password"))

        # Set the JWT cookies in the response
        resp = jsonify({'login': True})
        jwt.set_access_cookies(resp, access_token)
        jwt.set_refresh_cookies(resp, refresh_token)
        return resp, 200


# class LogoutApi(Resource):
#     # Because the JWTs are stored in an httponly cookie now, we cannot
#     # log the user out by simply deleting the cookie in the frontend.
#     # We need the backend to send us a response to delete the cookies
#     # in order to logout. unset_jwt_cookies is a helper function to
#     # do just that.
#     def get(self):
#         resp = jsonify()
#         jwt.unset_jwt_cookies(resp)
#         return {'logout': True}


# class RefreshTokenApi(Resource):
#     # Same thing as login here, except we are only setting a new cookie
#     # for the access token.
#     @jwt.jwt_refresh_token_required
#     def post(self):
#         # Create the new access token
#         current_user = jwt.get_jwt_identity()
#         access_token = jwt.create_access_token(identity=current_user)

#         # Set the JWT access cookie in the response
#         resp = jsonify({'refresh': True})
#         jwt.set_access_cookies(resp, access_token)
#         return resp, 200


# class ForgotPassword(Resource):
#     def post(self):
#         url = request.host_url + 'reset/'
#         body = request.get_json()
#         email = body.get('email')
#         if not email:
#             raise errors.SchemaValidationError

#         user = User.objects.get(email=email)
#         if not user:
#             raise errors.EmailDoesnotExistsError

#         expires = datetime.timedelta(hours=24)
#         reset_token = jwt.create_access_token(str(user.id), expires_delta=expires)

#         return send_email('[Ebisu-Flashcards] Reset Your Password',
#                             sender='test@test.com',
#                             recipients=[user.email],
#                             text_body=render_template('email/reset_password.txt',
#                                                     url=url + reset_token),
#                             html_body=render_template('email/reset_password.html',
#                                                     url=url + reset_token))


# class ResetPassword(Resource):
#     def post(self):
#         url = request.host_url + 'reset/'
#         body = request.get_json()
#         reset_token = body.get('reset_token')
#         password = body.get('password')

#         if not reset_token or not password:
#             raise errors.SchemaValidationError

#         user_id = jwt.decode_token(reset_token)['identity']

#         user = User.objects.get(id=user_id)

#         user.modify(password=password)
#         user.hash_password()
#         user.save()

#         return send_email('[Ebisu-Flashcards] Password reset successful',
#                             sender='support@movie-bag.com',
#                             recipients=[user.email],
#                             text_body='Password reset was successful',
#                             html_body='<p>Password reset was successful</p>')



class StudyApi(study.StudyMixin, cards.CardMixin, Resource):

    @jwt.jwt_required
    def get(self, deck_id):
        user_id = jwt.get_jwt_identity()
        try:
            db_next_card = self.get_next_card(user_id, deck_id)
            next_card = self.serialize_one(db_next_card, self.server_side_rendering)
            return Response(next_card, mimetype="application/json", status=200)
        
        except models.Deck.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=404)


    @jwt.jwt_required
    def post(self, deck_id):
        user_id = jwt.get_jwt_identity()
        body = request.get_json()
        self.process_test_results(**body, user_id=user_id, deck_id=deck_id)
        return Response(json.dumps(None), mimetype="application/json", status=200)



class DecksApi(decks.DeckMixin, Resource):

    @jwt.jwt_required
    def get(self):
        user_id = jwt.get_jwt_identity()
        try:
            decks_list = self.get_deck(user_id, 'all')
            decks = self.serialize_list(decks_list, self.server_side_rendering)
            return Response(decks, mimetype="application/json", status=200)
            
        except models.Deck.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=404)


    @jwt.jwt_required
    def post(self):
        user_id = jwt.get_jwt_identity()
        data = request.get_json()
        db_deck = self.create_deck(user_id, data)
        deck = self.serialize_one(db_deck, self.server_side_rendering)
        return Response(deck, mimetype="application/json", status=200)


class DeckApi(decks.DeckMixin, Resource):

    @jwt.jwt_required
    def get(self, deck_id):
        user_id = jwt.get_jwt_identity()
        try:
            db_deck = self.get_deck(user_id, deck_id)
            deck = self.serialize_one(db_deck, self.server_side_rendering)
            return Response(deck, mimetype="application/json", status=200)

        except models.Deck.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=404)
            

    @jwt.jwt_required
    def put(self, deck_id):
        user_id = jwt.get_jwt_identity()
        data = request.get_json()
        try:
            db_deck = self.update_deck(user_id, deck_id, data)
            deck = self.serialize_one(db_deck, self.server_side_rendering)
            return Response(deck, mimetype="application/json", status=200)

        except models.Deck.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=404)


    @jwt.jwt_required
    def delete(self, deck_id):
        user_id = jwt.get_jwt_identity()
        try:
            self.delete_deck(user_id, deck_id)
            return Response(json.dumps(None), mimetype="application/json", status=200)

        except models.Deck.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=404)



class CardsApi(cards.CardMixin, Resource):

    @jwt.jwt_required
    def get(self, deck_id):
        user_id = jwt.get_jwt_identity()
        try:
            cards_list = self.get_card(user_id, deck_id, 'all')
            cards = self.serialize_list(cards_list, self.server_side_rendering)
            return Response(cards, mimetype="application/json", status=200)

        except (models.Card.DoesNotExist, models.Deck.DoesNotExist):
            return Response(json.dumps(None), mimetype="application/json", status=404)


    @jwt.jwt_required
    def post(self, deck_id):
        user_id = jwt.get_jwt_identity()
        try:
            data = self.server_side_parsing(request.get_json())
            db_card = self.create_card(user_id, deck_id, data)
            card = self.serialize_one(db_card, self.server_side_rendering)
            return Response(card, mimetype="application/json", status=200)

        except models.Deck.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=404)


class CardApi(cards.CardMixin, Resource):

    @jwt.jwt_required
    def get(self, deck_id, card_id):
        user_id = jwt.get_jwt_identity()
        try:
            db_card = self.get_card(user_id, deck_id, card_id)
            card = self.serialize_one(db_card, self.server_side_rendering)
            return Response(card, mimetype="application/json", status=200)

        except (models.Card.DoesNotExist, models.Deck.DoesNotExist):
            return Response(json.dumps(None), mimetype="application/json", status=404)
            

    @jwt.jwt_required
    def put(self, deck_id, card_id):
        user_id = jwt.get_jwt_identity()
        data = self.server_side_parsing(request.get_json())
        try:
            db_card = self.update_card(user_id, deck_id, card_id, data)
            card = self.serialize_one(db_card, self.server_side_rendering)
            return Response(card, mimetype="application/json", status=200)

        except (models.Card.DoesNotExist, models.Deck.DoesNotExist):
            return Response(json.dumps(None), mimetype="application/json", status=404)
            
    
    @jwt.jwt_required
    def delete(self, deck_id, card_id):
        user_id = jwt.get_jwt_identity()
        try:
            self.delete_card(user_id, deck_id, card_id)
            return Response(json.dumps(None), mimetype="application/json", status= 200)

        except (models.Card.DoesNotExist, models.Deck.DoesNotExist):
            return Response(json.dumps(None), mimetype="application/json", status=404)


class _TemplatesApi:
    def get(self, name: str):
        try:
            db_templates = self.get_template('all')
            templates = self.serialize_list(db_templates, partial(self.server_side_rendering, name=name))
            return Response(templates, mimetype="application/json", status=200)
        except models.Template.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=200)

class QuestionTemplatesApi(_TemplatesApi, templates.TemplateMixin, Resource):
    @jwt.jwt_required
    def get(self):
        return super().get(name="question")

class AnswerTemplatesApi(_TemplatesApi, templates.TemplateMixin, Resource):
    @jwt.jwt_required
    def get(self):
        return super().get(name="answer")


class TemplateApi(templates.TemplateMixin, Resource):
    
    @jwt.jwt_required
    def get(self, template_id):
        try:
            db_template = self.get_template(template_id)
            template = self.serialize_one(db_template, self.server_side_rendering)
            return Response(template.to_json(), mimetype="application/json", status=200)
        except models.Template.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=200)


class AlgorithmsApi(Resource):
    
    @jwt.jwt_required
    def get(self):
        names = []
        for name, klass in algorithms.ALGORITHM_MAPPING.items():
            algorithm = {
                'name': name,
                'extra_fields': render_template(os.path.join("components", "decks", name+".html"), deck={})    
            }
            names.append(algorithm)
        return Response(json.dumps(names), mimetype="application/json", status=200)
