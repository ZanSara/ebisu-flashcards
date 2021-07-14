from flask_mongoengine import MongoEngine
from ebisu_flashcards.app import app

db = MongoEngine()
db.init_app(app)

from ebisu_flashcards.database.models import *