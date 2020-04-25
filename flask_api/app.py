from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_restful import Api

app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/ebisu-db'
}

mail = Mail(app)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# imports requiring app and mail
import database
import resources

resources.initialize_routes(api)
database.initialize_db(app)
