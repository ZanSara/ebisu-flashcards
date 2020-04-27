from . import models as api_models
from . import auth as api_auth

def initialize_routes(api):
    api.add_resource(api_models.StudyApi, '/api/study/<deck_id>')

    api.add_resource(api_models.DecksApi, '/api/decks')
    api.add_resource(api_models.DeckApi, '/api/decks/<deck_id>')
    api.add_resource(api_models.CardsApi, '/api/decks/<deck_id>/cards')
    api.add_resource(api_models.CardApi, '/api/decks/<deck_id>/cards/<card_id>')
    
    api.add_resource(api_models.TemplatesApi, '/api/templates')
    api.add_resource(api_models.TemplateApi, '/api/templates/<template_id>')
    api.add_resource(api_models.AlgorithmsApi, '/api/algorithms')
    
    api.add_resource(api_auth.SignupApi, '/api/auth/signup')
    api.add_resource(api_auth.LoginApi, '/api/auth/login')
    api.add_resource(api_auth.ForgotPassword, '/api/auth/forgot')
    api.add_resource(api_auth.ResetPassword, '/api/auth/reset')
