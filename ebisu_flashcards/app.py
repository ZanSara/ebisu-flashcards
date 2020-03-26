from typing import List

from collections import OrderedDict

from flask import Flask, session, render_template, redirect, request
from flask_session import Session

from ebisu_flashcards.model import load_decks_data, load_deck_by_id, Deck, Card

app = Flask(__name__)
# Check Configuration section for more details
# SESSION_TYPE = 'filesystem'
# app.config.from_object(__name__)
# Session(app)


@app.route('/')
def home():
    decks = load_decks_data()
    return render_template( 'home.html', 
                            navbar_title="Home",
                            decks=decks,
                        )

@app.route('/deck_<int:deck_id>/study', methods=["GET", "POST"])
@app.route('/deck_<int:deck_id>/study/<int:card_id>', methods=["GET", "POST"])
def study(deck_id, card_id=None):
    deck = load_deck_by_id(deck_id)
    
    # Update model and save
    if request.method == 'POST':
        print("####################################### TEST RESULT: ", bool(int(request.form["test_result"])))
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

@app.route('/decks')
def decks():
    decks = load_decks_data()
    return render_template( 'decks.html', 
                            navbar_title="Decks",
                            decks=decks,
                        )

@app.route('/deck_<int:deck_id>/edit', methods=["GET", "POST"])
def edit(deck_id):
    deck = load_deck_by_id(deck_id)
    card_to_edit = None
    
    if request.method == 'POST':
        card_id = int(request.form["card_id"])
        if card_id == -1:
            # It's a new card
            new_id = deck.cards[-1].id  + 1
            question = request.form["question"]
            answer = request.form["answer"]
            new_card = Card(OrderedDict({"id":new_id, "question":question, "answer":answer}))
            deck.cards.append(new_card)
            deck.save()
        else:
            # It's an edited card
            original_card = deck.get_card_by_id(card_id)
            if "question" in request.form.keys() and request.form["question"] != "":
                # New data already arrived
                original_card.update_from_dict(request.form)
                deck.save()
            else:
                # This is a loading request:
                card_to_edit = deck.get_card_by_id(card_id).to_dict()

    cards = [card.to_dict() for card in deck.cards]
    return render_template('deck-edit.html',
                            navbar_title='Edit "{}"'.format(deck.name),
                            deck_id=deck_id,
                            card_to_edit=card_to_edit,
                            cards=cards)

# TODO
@app.route('/settings')
def settings():
    return render_template('base.html', navbar_title="Settings")
