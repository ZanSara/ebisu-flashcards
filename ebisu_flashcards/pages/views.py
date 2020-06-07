from flask import Blueprint, render_template, redirect, request, jsonify, url_for

from flask_bcrypt import Bcrypt
import flask_jwt_extended as jwt


from ebisu_flashcards.database.models import User, Deck
from ebisu_flashcards.app import app
from ebisu_flashcards.database import auth
from ebisu_flashcards.api import errors 
from ebisu_flashcards.pages import pages_blueprint


bcrypt = Bcrypt(app)
jwt_manager = jwt.JWTManager(app)


# Using the expired_token_loader decorator, we will now call
# this function whenever an expired but otherwise valid access
# token attempts to access an endpoint
@jwt_manager.expired_token_loader
def my_expired_token_callback(expired_token):
    return redirect("/login")  # TODO Add small explanatory tag somewhere in the frontend?






@pages_blueprint.route('/')
def frontpage():
    return render_template('landing-page.html')


@pages_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # TODO avoid asking people to login if they're logged in already

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            access_token, refresh_token = auth.login(username, password)

            # Set the JWT cookies in the response
            resp = redirect("/home")
            jwt.set_access_cookies(resp, access_token)
            jwt.set_refresh_cookies(resp, refresh_token)
            return resp
        
        except errors.UnauthorizedError:
            return render_template('login.html', feedback="User or password are incorrect")

    return render_template('login.html')


@pages_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        pass
        #TODO implement!!

    return render_template('register.html')


@pages_blueprint.route('/logout')
def logout():
    # Because the JWTs are stored in an httponly cookie now, we cannot
    # log the user out by simply deleting the cookie in the frontend.
    # We need the backend to send us a response to delete the cookies
    # in order to logout. unset_jwt_cookies is a helper function to
    # do just that.
    resp = resp = redirect(url_for('frontpage'))
    jwt.unset_jwt_cookies(resp)
    return resp, 200


@pages_blueprint.route('/home')
@jwt.jwt_optional
def home():
    if not jwt.get_jwt_identity():
        return redirect("/login")
    return render_template('home.html', navbar_title="Home")
    
    
@pages_blueprint.route('/study/<deck_id>')
@jwt.jwt_optional
def study(deck_id):
    if not jwt.get_jwt_identity():
        redirect("/login")

    user_id = jwt.get_jwt_identity()
    deck = Deck.objects.get(id=deck_id, author=user_id)
    return render_template('study.html', navbar_title=deck.name, navbar_home=True)


@pages_blueprint.route('/edit/<deck_id>')
@jwt.jwt_optional
def edit(deck_id):
    if not jwt.get_jwt_identity():
        redirect("/login")

    user_id = jwt.get_jwt_identity()
    deck = Deck.objects.get(id=deck_id, author=user_id)
    return render_template('edit.html', navbar_title="\"{}\" Cards List".format(deck.name), navbar_home=True)



@pages_blueprint.errorhandler(404)
def page_not_found(e):
    return render_template('not-found.html'), 404


@pages_blueprint.errorhandler(500)
def internal_error(e):
    return render_template('error.html'), 500


@pages_blueprint.errorhandler(401)
def unauthorized(e):
    return redirect("/login"), 401
