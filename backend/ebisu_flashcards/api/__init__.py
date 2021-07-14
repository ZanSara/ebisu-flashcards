from flask import Blueprint
from flask_restful import Api

from ebisu_flashcards.api import auth, study, decks, cards, templates, algorithms
from ebisu_flashcards.errors import errors


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, errors=errors)


# Auth API
api.add_resource(auth.SignupApi, '/api/auth/signup')
api.add_resource(auth.LoginApi, '/api/auth/login')
# api.add_resource(resources.RefreshTokenApi, '/api/auth/refresh')
# api.add_resource(resources.LogoutApi, '/api/auth/logout')
# api.add_resource(resources.ForgotPassword, '/api/auth/forgot')
# api.add_resource(resources.ResetPassword, '/api/auth/reset')

# Study API
api.add_resource(study.StudyApi, '/api/study/<deck_id>')

# Decks API
api.add_resource(decks.DecksApi, '/api/decks')
api.add_resource(decks.DeckApi, '/api/decks/<deck_id>')

# Cards API
api.add_resource(cards.CardsApi, '/api/decks/<deck_id>/cards')
api.add_resource(cards.CardApi, '/api/decks/<deck_id>/cards/<card_id>')

# Templates API
api.add_resource(templates.QuestionTemplatesApi, '/api/question-templates')
api.add_resource(templates.AnswerTemplatesApi, '/api/answer-templates')
api.add_resource(templates.TemplateApi, '/api/templates/<template_id>')

# Algorithms API
api.add_resource(algorithms.AlgorithmsApi, '/api/algorithms')
