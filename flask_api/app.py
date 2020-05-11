from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_restful import Api

app = Flask(__name__)
#app.config.from_envvar('ENV_FILE_LOCATION')

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/ebisu-db'
}

app.config['MAIL_SERVER'] = "localhost"
app.config['MAIL_PORT'] = "1025"
app.config['MAIL_USERNAME'] = "support@movie-bag.com"
app.config['MAIL_PASSWORD'] = ""

# Configure application to store JWTs in cookies. Whenever you make
# a request to a protected endpoint, you will need to send in the
# access or refresh JWT via a cookie.
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token-cookie'
app.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token-cookie'

# Set the cookie paths, so that you are only sending your access token
# cookie to the access endpoints, and only sending your refresh token
# to the refresh endpoint. Technically this is optional, but it is in
# your best interest to not send additional cookies in the request if
# they aren't needed.
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'

# Enable csrf double submit protection. See this for a thorough
# explanation: http://www.redotheweb.com/2015/11/09/api-security.html
# By default, the CRSF cookies will be called csrf_access_token and
# csrf_refresh_token, and in protected endpoints we will look for the
# CSRF token in the 'X-CSRF-TOKEN' header. You can modify all of these
# with various app.config options. Check the options page for details.
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

# Set the secret key to sign the JWTs with
app.config['JWT_SECRET_KEY'] = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'  # Change this!


mail = Mail(app)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# imports requiring app and mail
import views
import database
import api_resources

api_resources.initialize_routes(api)
database.initialize_db(app)
