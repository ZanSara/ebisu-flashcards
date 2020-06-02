from flask import Blueprint
from flask_restful import Api

from ebisu_flashcards.api import errors, models, auth



api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)



api.add_resource(models.StudyApi, '/api/study/<deck_id>')

api.add_resource(models.DecksApi, '/api/decks')
api.add_resource(models.DeckApi, '/api/decks/<deck_id>')
api.add_resource(models.CardsApi, '/api/decks/<deck_id>/cards')
api.add_resource(models.CardApi, '/api/decks/<deck_id>/cards/<card_id>')

api.add_resource(models.TemplatesApi, '/api/templates')
api.add_resource(models.TemplateApi, '/api/templates/<template_id>')
api.add_resource(models.AlgorithmsApi, '/api/algorithms')

api.add_resource(auth.SignupApi, '/api/auth/signup')
# api.add_resource(auth.LoginApi, '/api/auth/login')
api.add_resource(auth.RefreshTokenApi, '/api/auth/refresh')
# api.add_resource(auth.LogoutApi, '/api/auth/logout')
api.add_resource(auth.ForgotPassword, '/api/auth/forgot')
api.add_resource(auth.ResetPassword, '/api/auth/reset')

