from flask import Flask

app = Flask(__name__, static_folder=None)

# FIXME Load different config depending on envvar
app.config.from_object('ebisu_flashcards.config.DevelopmentConfig')

# imports requiring app
import ebisu_flashcards.database

# Register blueprints
from ebisu_flashcards.api import api_blueprint
from ebisu_flashcards.pages import pages_blueprint

app.register_blueprint(api_blueprint)
app.register_blueprint(pages_blueprint)