from flask import Blueprint, render_template, redirect, request, jsonify, url_for, abort

import flask_jwt_extended as jwt

from ebisu_flashcards.app import app
from ebisu_flashcards.pages import pages_blueprint
from ebisu_flashcards.operations.auth import unauth_goes_to_login
from ebisu_flashcards.database.models import User, Deck


jwt_manager = jwt.JWTManager(app)


@pages_blueprint.route('/home')
@jwt.jwt_optional
@unauth_goes_to_login
def home():
    return render_template('home.html', navbar_title="Home")
    
    
@pages_blueprint.route('/study/<deck_id>')
@jwt.jwt_optional
@unauth_goes_to_login
def study(deck_id):
    user_id = jwt.get_jwt_identity()
    deck = Deck.objects.only("name").get(id=deck_id, author=user_id)
    return render_template('study.html', navbar_title=deck.name, navbar_home=True)


@pages_blueprint.route('/edit/<deck_id>')
@jwt.jwt_optional
@unauth_goes_to_login
def edit(deck_id):
    user_id = jwt.get_jwt_identity()
    deck = Deck.objects.only("name").get(id=deck_id, author=user_id)
    return render_template('edit.html', navbar_title="\"{}\" Cards List".format(deck.name), navbar_home=True)
