from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader

from app.models.mappings import CARD_TYPE_BY_DECK
from app.models.abc import AbstractDeck, AbstractCard


def home(request):
    decks = AbstractDeck.objects.all()
    context = {
        'navbar_title': "Home",
        'decks': decks,
    }
    return render(request, 'app/home.html', context)


def study(request, deck_id, card_id=None):
    deck = get_object_or_404(AbstractDeck, id=deck_id)
    
    # Update model and save
    if request.method == 'POST':
        deck.update_card(card_id, bool(int(request.POST.get("test_result"))))

    # Load next card
    if request.method == 'POST' or card_id is None:
        next_card_id = deck.next_card_to_review().id
        return redirect("study", deck_id=deck_id, card_id=next_card_id)

    # Load the card data
    card = get_object_or_404(AbstractCard, id=card_id)
    context = {
        'navbar_title': deck.name,
        'navbar_right': "## cards studied in this session",
        'card': card,
    }
    return render(request, 'app/study.html', context)


def edit(request, deck_id):
    deck = get_object_or_404(AbstractDeck, id=deck_id)
    cardtype = CARD_TYPE_BY_DECK[deck.__class__]
    card_dict = None
    
    if request.method == 'POST':
        card_id = int(request.POST.get("card_id"))
        if card_id == -1:
            # It's a new card
            question = request.POST.get("question")
            answer = request.POST.get("answer")
            new_card = cardtype.objects.create(question=question, answer=answer, deck_id=deck.id)
        else:
            # It's an edited card
            original_card = get_object_or_404(cardtype, id=card_id)
            if request.POST.get("question"):
                # New data already arrived
                original_card.update_from_dict(request.POST)
            else:
                # This is a loading request
                card_dict = original_card.to_dict()

    # Load the cards list as dicts & process where necessary
    cards = [card.to_dict() for card in deck.cards.all()]
    for card in cards:
        card["layout"] = "app/card_templates/{}".format(card["layout"]["name"])
        card["tags"] = [tag.name for tag in card["tags"]]

    # Render
    context = {
        'navbar_title': 'Edit "{}"'.format(deck.name),
        'deck_id': deck_id,
        'card_to_edit': card_dict,
        'cards': cards,
    }
    return render(request, 'app/deck-edit.html', context)
