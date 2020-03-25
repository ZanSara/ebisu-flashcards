from typing import List

from flask import Flask, session, render_template, redirect, request
from flask_session import Session

from ebisu_flashcards.model import load_decks_data, load_deck_by_id, Deck, Card

app = Flask(__name__)
# Check Configuration section for more details
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.route('/')
def home():
    decks = load_decks_data()
    return render_template( 'home.html', 
                            navbar_title="Home",
                            decks=decks,
                        )
    # deck = Deck("Test deck")
    #session["deck"] = deck
    #return render_template('home.html', navbar_title="Home")


@app.route('/deck_<int:deck_id>/study', methods=["GET", "POST"])
@app.route('/deck_<int:deck_id>/study/<int:card_id>', methods=["GET", "POST"])
def study(deck_id, card_id=None):
    deck = load_deck_by_id(deck_id)
    
    # Update model and save
    if request.method == 'POST':
        deck.update_card(card_id, bool(request.form["test_result"]))
        deck.save()

    # Load next card
    if request.method == 'POST' or card_id is None:
        next_card_id = deck.next_card_to_review().id
        return redirect("/deck_{}/study/{}".format(deck_id, next_card_id))

    # Load the card data
    card = deck.get_card_by_id(card_id)
    return render_template('study.html', 
                            navbar_title=deck.name, 
                            navbar_right="{} cards studied in this session".format(deck.cards_studied_count),
                            card=card,
                            cards_count=deck.cards_studied_count
                        )


# TODO
@app.route('/settings')
def settings():
    return render_template('base.html', navbar_title="Settings")
