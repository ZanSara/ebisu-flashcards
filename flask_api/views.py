from flask import render_template, redirect, request, jsonify, url_for
import flask_jwt_extended as jwt

from database.models import User
from api_resources import errors
from app import app



@app.route('/')
def frontpage():
    return render_template('landing-page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # Identify the user
        body = request.form
        user = User.objects.get(username=body.get('username'))
        authorized = user.check_password(body.get('password'))
        if not authorized:
            raise errors.UnauthorizedError

        # Create the tokens we will be sending back to the user
        access_token = jwt.create_access_token(identity=str(user.id))
        refresh_token = jwt.create_refresh_token(identity=str(user.id))

        # Set the JWT cookies in the response
        resp = redirect("/home")
        jwt.set_access_cookies(resp, access_token)
        jwt.set_refresh_cookies(resp, refresh_token)
        return resp

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        pass
        #TODO implement!!

    return render_template('register.html')


@app.route('/logout')
def logout():
    # Because the JWTs are stored in an httponly cookie now, we cannot
    # log the user out by simply deleting the cookie in the frontend.
    # We need the backend to send us a response to delete the cookies
    # in order to logout. unset_jwt_cookies is a helper function to
    # do just that.
    resp = resp = redirect(url_for('frontpage'))
    jwt.unset_jwt_cookies(resp)
    return resp, 200


@app.route('/home')
@jwt.jwt_required
def home():
    return render_template('home.html', 
                            navbar_title="Home")


@app.route('/study/<deck_id>')
@jwt.jwt_required
def study(deck_id):
    return render_template('study.html', navbar_title="Study")


@app.route('/edit/<deck_id>')
@jwt.jwt_required
def edit(deck_id):
    return render_template('edit.html', 
                            navbar_title="Edit")