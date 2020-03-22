from typing import List

from flask import Flask, session, render_template, redirect, request
from flask_session import Session

from ebisu_flashcards.model import Deck, Card

app = Flask(__name__)
# Check Configuration section for more details
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.route('/')
def home():
    deck = Deck("Test deck")
    session["deck"] = deck
    return render_template('home.html', navbar_title="Home")


@app.route('/study', methods=["GET", "POST"])
def study():
    
    # Update model, save and proceed
    if request.method == 'POST':
        current_card = session["current_card"]
        current_card.store_test_result(bool(request.form["test_result"]))

    # Save data
    deck = session["deck"]
    deck.save()

    # Load the card data
    session["current_card"] = deck.next_card_to_review()
    return render_template('study.html', 
                            navbar_title=deck.name, 
                            navbar_right="{} cards studied in this session".format(deck.cards_studied_count),
                            card=session["current_card"],
                            cards_count=deck.cards_studied_count
                        )

@app.route('/study/leave')
def study_leave():
    session["deck"].save()
    return redirect("/", deck_saved=True)


# TODO
@app.route('/settings')
def settings():
    return render_template('base.html', navbar_title="Settings")


#TODO
@app.route('/decks')
def decks():
    return render_template('base.html', navbar_title="Decks")