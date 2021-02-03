from pathlib import Path
from flask import Flask
from ebisu_flashcards.config import Config

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

# DISGUSTING HACK!
javascript_core = Path(__file__).parent / "pages" / "static" / "js" / "base.js"
with open(str(javascript_core), 'r') as file :
  filedata = file.read()
filedata = filedata.replace("$$_URL_PREFIX_$$", Config.URL_PREFIX)
with open(str(javascript_core), 'w') as file:
  file.write(filedata)