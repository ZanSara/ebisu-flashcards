from typing import Any, Type, Optional
from django.http import Http404
from django.shortcuts import render, redirect
from django.template import loader

from app.models import Deck, Card, decks


def get_object_or_404(model_class: Type, id: str) -> Optional[Any]:
    instance = model_class.objects.get(id=id)
    if not instance:
        raise Http404
    else:
        return instance


def login(request):
    return render(request, 'app/login.html', {})


def register(request):
    return render(request, 'app/register.html', {})


def reset_password(request):
    return render(request, 'app/reset-password.html', {})


def home(request):
    decks = [deck.to_dict() for deck in Deck.objects.all()]
    print(decks)
    context = {
        'navbar_title': "Home",
        'decks': decks,
    }
    return render(request, 'app/home.html', context)


def edit_deck(request, deck_id=None):
    # Deck creation
    if not deck_id:
    
        # Save new deck and go to edit page
        if request.method == 'POST':
            deck_id = decks.create_deck_from_request(request.POST)
            return redirect("edit_deck", deck_id)
        
        # Just render the empty deck_edit page
        context = {
            'navbar_title': 'Create Deck',
            'algorithms': list(decks.DECK_CLASSES.keys()),
        }
        return render(request, 'app/deck-edit.html', context)

    # Deck editing
    deck = get_object_or_404(Deck, id=deck_id)

    # Save deck data and go to edit page
    if request.method == 'POST':
        deck.update_from_request(request.POST)
        return redirect("edit_deck", deck_id)

    # Load the cards list as dicts & process where necessary
    cards = [card.to_dict() for card in deck.cards]
    print(cards)
    for card in cards:
        card["layout"] = "app/card_templates/{}".format(card["layout"]["name"])
        card["tags"] = [tag.name for tag in card["tags"]]

    # Render
    context = {
        'navbar_title': 'Edit "{}"'.format(deck.name),
        'algorithms': list(decks.DECK_CLASSES.keys()),
        'deck': deck.to_dict(),
        'cards': cards,
    }
    return render(request, 'app/deck-edit.html', context)


def delete_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    deck.delete()
    return redirect("home")


def edit_card(request, deck_id, card_id):
    deck = get_object_or_404(Deck, id=deck_id)
    cardtype = CARD_TYPE_BY_DECK[deck.__class__]
    original_card = get_object_or_404(cardtype, id=card_id)

    # New data already arrived
    if request.method == 'POST':
        # Update model and redirect back
        original_card.update_from_dict(request.POST)
        return redirect("/deck_{}/edit".format(deck_id))

    # Load card data
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
        'cards': cards,
        'card_to_edit': card_dict,
    }
    return render(request, 'app/deck-edit.html', context)


def add_card(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    cardtype = CARD_TYPE_BY_DECK[deck.__class__]
    card_dict = None
    
    if request.method == 'POST':
        card_form = FORM_TYPE_BY_CARD[cardtype](request)
        question = request.POST.get("question")
        answer = request.POST.get("answer")
        new_card = cardtype.objects.create(question=question, answer=answer, deck_id=deck.id)

    return redirect("/deck_{}/edit".format(deck_id))


def delete_card(request, deck_id, card_id):
    card = get_object_or_404(Card, id=card_id, deck=deck_id)    
    card.delete()
    return redirect("/deck_{}/edit".format(deck_id))



def study(request, deck_id, card_id=None):
    deck = Deck.objects.get(id=deck_id)
    algorithm = Algorithm.resolve(deck.algorithm)

    # Load next card
    if card_id is None:
        next_card_id = algorithm.next_card_to_review().id
        return redirect("study", deck_id=deck_id, card_id=next_card_id)

    # Update model, save and load next card
    if request.method == 'POST':
        card = Card.objects.get(id=card_id)
        algorithm.process_result(deck, card, DUMMY_USER, bool(int(request.POST.get("test_result"))))
        next_card_id = algorithm.next_card_to_review().id
        return redirect("study", deck_id=deck_id, card_id=next_card_id)

    # Load the card data
    card = Card.objects.get(id=card_id)

    context = {
        'navbar_title': deck.name,
        'navbar_right': "## cards studied in this session",
        'question': card.question.get_content(),
        'answer': card.answer.get_content(),
    }
    return render(request, 'app/study.html', context)


