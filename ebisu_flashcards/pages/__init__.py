from flask import Blueprint

pages_blueprint = Blueprint('pages', __name__, template_folder="templates", static_folder='static')

from ebisu_flashcards.pages import views