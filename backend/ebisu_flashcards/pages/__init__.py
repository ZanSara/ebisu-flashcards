from flask import Blueprint, redirect, url_for
import flask_jwt_extended as jwt
from ebisu_flashcards.app import app

pages_blueprint = Blueprint('pages', __name__, template_folder="templates", static_folder='static')

from ebisu_flashcards.pages import errors
from ebisu_flashcards.pages import external
from ebisu_flashcards.pages import internal


jwt_manager = jwt.JWTManager(app)


# Using the expired_token_loader decorator, we will now call
# this function whenever an expired but otherwise valid access
# token attempts to access an endpoint
@jwt_manager.expired_token_loader
def my_expired_token_callback(expired_token):
    return external.login(feedback="Login expired. Please login again", feedback_type="positive") 
