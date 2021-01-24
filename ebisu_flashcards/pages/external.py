from flask import render_template, redirect, request, url_for, abort
import flask_jwt_extended as jwt

from ebisu_flashcards import errors 
from ebisu_flashcards.operations import auth
from ebisu_flashcards.pages import pages_blueprint



@pages_blueprint.route('/')
def frontpage():
    return render_template('landing-page.html')


@pages_blueprint.route('/login', methods=['GET', 'POST'])
def login(feedback=None, feedback_type=None):
    
    # TODO avoid asking people to login if they're logged in already

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            access_token, refresh_token = auth.login(username, password)

            # Set the JWT cookies in the response
            resp = redirect(url_for("pages.home"))
            jwt.set_access_cookies(resp, access_token)
            jwt.set_refresh_cookies(resp, refresh_token)
            return resp
        
        except errors.UnauthorizedError:
            return render_template('login.html', feedback="User or password are incorrect", feedback_type="negative")

    return render_template('login.html', feedback=feedback, feedback_type=feedback_type)


@pages_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    return abort(404)  # FIXME remove when opening the site

    if request.method == "POST":
        
        username = request.form.get('username')
        email = request.form.get("email")
        password = request.form.get('password')
        try:
            auth.signup(request.form)
            return login(feedback="Registered successfully! Please login again", feedback_type="positive")

        except Exception as e:
            print(e)
            return render_template('register.html', feedback="Registration failed! Please try again", feedback_type="negative")

    return render_template('register.html')



@pages_blueprint.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    return abort(404)  # TODO implement me!



@pages_blueprint.route('/logout')
def logout():
    # Because the JWTs are stored in an httponly cookie now, we cannot
    # log the user out by simply deleting the cookie in the frontend.
    # We need the backend to send us a response to delete the cookies
    # in order to logout. unset_jwt_cookies is a helper function to
    # do just that.
    resp = resp = redirect(url_for('pages.frontpage'))
    jwt.unset_jwt_cookies(resp)
    return resp, 200
