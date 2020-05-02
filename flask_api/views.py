from flask import render_template, redirect, request
from app import app


@app.route('/')
def home():
    return render_template('home.html', navbar_title="Home")


@app.route('/study/<deck_id>')
def study(deck_id):
    return render_template('study.html', navbar_title="Study")


@app.route('/edit/<deck_id>')
def edit(deck_id):
    return render_template('edit.html', navbar_title="Edit")