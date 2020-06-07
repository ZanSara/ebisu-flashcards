
from flask import render_template, redirect

from ebisu_flashcards.pages import pages_blueprint
from ebisu_flashcards.pages import external


@pages_blueprint.errorhandler(401)
def unauthorized(e):
    return external.login(feedback="Please login", feedback_type="negative") 


@pages_blueprint.errorhandler(404)
def page_not_found(e):
    return render_template('not-found.html'), 404


@pages_blueprint.errorhandler(500)
def internal_error(e):
    return render_template('error.html'), 500
