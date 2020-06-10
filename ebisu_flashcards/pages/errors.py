
from flask import render_template, redirect

from ebisu_flashcards.app import app
from ebisu_flashcards.pages import external


@app.errorhandler(401)
def unauthorized(e):
    return external.login(feedback="Please login", feedback_type="negative") 


@app.errorhandler(404)
def page_not_found(e):
    return render_template('not-found.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html'), 500
