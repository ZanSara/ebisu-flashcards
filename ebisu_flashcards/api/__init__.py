from flask import Blueprint
from flask_restful import Api

from ebisu_flashcards.api import resources


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


# Study API
api.add_resource(resources.StudyApi, '/api/study/<deck_id>')

# Decks CRUD API
api.add_resource(resources.DecksApi, '/api/decks')
api.add_resource(resources.DeckApi, '/api/decks/<deck_id>')

# Cards CRUD API
api.add_resource(resources.CardsApi, '/api/decks/<deck_id>/cards')
api.add_resource(resources.CardApi, '/api/decks/<deck_id>/cards/<card_id>')

# Templates CRUD API
api.add_resource(resources.TemplatesApi, '/api/templates')
api.add_resource(resources.TemplateApi, '/api/templates/<template_id>')

# Algorithms GET API
api.add_resource(resources.AlgorithmsApi, '/api/algorithms')

# Auth API
api.add_resource(resources.SignupApi, '/api/auth/signup')
api.add_resource(resources.LoginApi, '/api/auth/login')
# api.add_resource(resources.RefreshTokenApi, '/api/auth/refresh')
# api.add_resource(resources.LogoutApi, '/api/auth/logout')
# api.add_resource(resources.ForgotPassword, '/api/auth/forgot')
# api.add_resource(resources.ResetPassword, '/api/auth/reset')

