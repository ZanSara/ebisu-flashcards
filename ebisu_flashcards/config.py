class Config(object):

    # Configure application to store JWTs in cookies. Whenever you make
    # a request to a protected endpoint, you will need to send in the
    # access or refresh JWT via a cookie.
    JWT_TOKEN_LOCATION = ['cookies', 'json']

    JWT_ACCESS_COOKIE_NAME = 'access_token-cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token-cookie'

    # Set the cookie paths, so that you are only sending your access token
    # cookie to the access endpoints, and only sending your refresh token
    # to the refresh endpoint. Technically this is optional, but it is in
    # your best interest to not send additional cookies in the request if
    # they aren't needed.
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/token/refresh'

    # Enable csrf double submit protection. See this for a thorough
    # explanation: http://www.redotheweb.com/2015/11/09/api-security.html
    # By default, the CRSF cookies will be called csrf_access_token and
    # csrf_refresh_token, and in protected endpoints we will look for the
    # CSRF token in the 'X-CSRF-TOKEN' header. You can modify all of these
    # with various app.config options. Check the options page for details.
    JWT_COOKIE_CSRF_PROTECT = True



class ProductionConfig(Config):
    DEBUG = False
    TESTING = False



class DevelopmentConfig(Config):
    DEBUG = True

    # DB Settings
    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost/ebisu-db'
    }

    # Mail - unused
    MAIL_SERVER = "localhost"
    MAIL_PORT = "1025"
    MAIL_USERNAME = "support@ebisu-flashcards.com"
    MAIL_PASSWORD = ""

    # The secret key to sign the JWTs with
    JWT_SECRET_KEY = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'



class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    # DB Settings
    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost/ebisu-db'
    }

    # Mail - unused
    MAIL_SERVER = "localhost"
    MAIL_PORT = "1025"
    MAIL_USERNAME = "support@ebisu-flashcards.com"
    MAIL_PASSWORD = ""

    # The secret key to sign the JWTs with
    JWT_SECRET_KEY = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'