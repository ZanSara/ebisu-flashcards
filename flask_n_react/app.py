from flask import Flask, request
from flask_restful import Api

from . import resources

app = Flask(__name__)
api = Api(app)

api.add_resource(resources.AuthenticationApi, '/login', '/register', '/reset-password')
api.add_resource(resources.HomeApi, '/', )
api.add_resource(resources.StudyApi, '/study/deck/<deck_id>/card/<card_id>')
api.add_resource(resources.DeckApi, '/edit/deck/<deck_id>', '/edit/new_deck')
api.add_resource(resources.CardApi, '/edit/deck/<deck_id>/card/<card_id>', '/edit/deck/<deck_id>/new_card')
# api.add_resource(RenderersApi, '/renderers')  # Coming soon
