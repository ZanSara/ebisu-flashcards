from pathlib import Path
from flask import Flask
from ebisu_flashcards.config import Config

app = Flask(__name__, static_folder=None)


# FIXME Load different config depending on envvar
app.config.from_object('ebisu_flashcards.config.DevelopmentConfig')


# Now import all the stuff that requires `app`
import ebisu_flashcards.database


# Register blueprints
from ebisu_flashcards.api import api_blueprint
app.register_blueprint(api_blueprint)
