from typing import Any, Type, Optional
from django.http import Http404
from django.shortcuts import render, redirect
from django.template import loader

from app.models import Deck, Card, Renderer, decks


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
    decks = Deck.objects.all()
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
        deck.update_from_postdata(request.POST)
        return redirect("edit_deck", deck_id)

    # Load the cards list as dicts & process where necessary
    cards = [card.to_widgets() for card in deck.cards]
    card_fields = deck.CARD_TYPE().to_widgets()

    # Render
    context = {
        'navbar_title': 'Edit "{}"'.format(deck.name),
        'algorithms': list(decks.DECK_CLASSES.keys()),
        'deck': deck,
        'renderers': list(Renderer.objects.all()),
        'card_fields': card_fields,
        'cards': cards,
    }
    return render(request, 'app/deck-edit.html', context)


def delete_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    deck.delete()
    return redirect("home")


def edit_card(request, deck_id, card_id=None):
    deck = get_object_or_404(Deck, id=deck_id)

    # Add new card
    if not card_id:

        # Save and return to same page
        if request.method == 'POST':
            deck.add_card(request.POST)
            return redirect("edit_deck", deck_id)
        
    card = get_object_or_404(Card, id=card_id)

    # New data already arrived
    if request.method == 'POST':
        # Update model and redirect back
        card.update_from_postdata(request.POST)
        return redirect("/edit/deck_{}".format(deck_id))

    # Load card data
    card_to_edit = card.to_widgets()

    # Load the cards list as dicts & process where necessary
    cards = [card.to_widgets() for card in deck.cards]
    card_fields = deck.CARD_TYPE().to_widgets()
    
    # Render
    context = {
        'navbar_title': 'Edit "{}"'.format(deck.name),
        'deck': deck,
        'cards': cards,
        'card_fields': card_fields,
        'card_to_edit': card_to_edit,
    }
    return render(request, 'app/deck-edit.html', context)



def delete_card(request, deck_id, card_id):
    deck = get_object_or_404(Deck, id=deck_id) 
    card = get_object_or_404(Card, id=card_id) 
    if card in deck.cards:
        deck.cards.pull(id=card.id)
        card.delete()
    else:
        raise ValueError("Card does not belong to deck")
    return redirect("edit/deck_{}".format(deck_id))


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


