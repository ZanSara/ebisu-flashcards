from typing import Any, Type, Optional
from django.http import Http404
from django.shortcuts import render, redirect
from django.template import loader

from app.models import Deck, Card, Renderer, User, create_deck_from_postdata, DECK_CLASSES


def get_default_user_or_create() -> User:
    try:
        return User.objects.get(username="tester")
    except Exception as e:
        User(username="tester", password=b"fakepassword", email="me@email.com").save()


def get_object_or_404(model_class: Type, id: str) -> Optional[Any]:
    instance = model_class.objects.get(id=id)
    if not instance:
        raise Http404("Object not found")
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


def study(request, deck_id, card_id=None):
    deck = Deck.objects.get(id=deck_id)

    # Load next card
    if card_id is None:
        next_card_id = deck.next_card_to_review().id
        return redirect("study", deck_id=deck_id, card_id=next_card_id)

    # Update model, save and load next card
    if request.method == 'POST':
        card = Card.objects.get(id=card_id)
        deck.process_result(card=card, user=get_default_user_or_create(), test_results=request.POST.get("test_result"))
        next_card_id = deck.next_card_to_review().id
        return redirect("study", deck_id=deck_id, card_id=next_card_id)

    # Load the card data
    card = Card.objects.get(id=card_id)

    context = {
        'navbar_title': deck.name,
        'navbar_right': "## cards studied in this session",
        'card': card,
    }
    return render(request, 'app/study.html', context)


def new_deck(request):
    decks_list = Deck.objects.all()

    # Save new deck and go back to home
    if request.method == 'POST':
        deck_id = create_deck_from_postdata(request.POST)
        return redirect("home")

    # Just render the empty deck_edit page
    context = {
        'navbar_title': 'Home',
        'decks': decks_list,
        'edit': True,
        'algorithms': list(DECK_CLASSES.keys()),
    }
    return render(request, 'app/home.html', context)


def edit_deck_properties(request, deck_id):
    decks_list = Deck.objects.all()
    deck = get_object_or_404(Deck, id=deck_id)

    # Save deck data and go to edit page
    if request.method == 'POST':
        deck.update_from_postdata(request.POST)
        return redirect("home")

    # Render
    context = {
        'navbar_title': 'Home',
        'decks': decks_list,
        'edit': True,
        'algorithms': list(DECK_CLASSES.keys()),
        'deck_to_edit': deck,
    }
    return render(request, 'app/home.html', context)



def delete_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    deck.delete()
    return redirect("home")


def list_cards(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)

    # Render cards list
    cards = [card.to_widgets() for card in deck.cards]
    card_fields = deck.CARD_TYPE().to_widgets()

    context = {
        'navbar_title': 'Cards List of "{}"'.format(deck.name),
        'deck': deck,
        'renderers': list(Renderer.objects.all()),
        'card_fields': card_fields,
        'cards': cards,
    }
    return render(request, 'app/cards-list.html', context)


def new_card(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)

    # Save card
    if request.method == 'POST':
        new_card = deck.CARD_TYPE()
        new_card.load_from_postdata(request.POST)
        new_card.deck = deck
        new_card.save()

    # Render cards list
    cards = [card.to_widgets() for card in deck.cards]
    card_fields = deck.CARD_TYPE().to_widgets()

    context = {
        'navbar_title': 'Cards List of "{}"'.format(deck.name),
        'edit': True,
        'deck': deck,
        'renderers': list(Renderer.objects.all()),
        'card_fields': card_fields,
        'cards': cards,
    }
    return render(request, 'app/cards-list.html', context)
     

def edit_card(request, deck_id, card_id):
    deck = get_object_or_404(Deck, id=deck_id)
    card = get_object_or_404(Card, id=card_id)

    # New data already arrived
    if request.method == 'POST':
        # Update model and redirect back
        card.load_from_postdata(request.POST)
        card.save()
        return redirect("list_cards", deck_id)

    # Load card data
    card_to_edit = card.to_widgets()

    # Load the cards list as dicts & process where necessary
    cards = [card.to_widgets() for card in deck.cards]
    card_fields = deck.CARD_TYPE().to_widgets()
    
    # Render
    context = {
        'navbar_title': 'Edit "{}"'.format(deck.name),
        'edit': True,
        'deck': deck,
        'cards': cards,
        'renderers': list(Renderer.objects.all()),
        'card_fields': card_fields,
        'card_to_edit': card_to_edit,
    }
    return render(request, 'app/cards-list.html', context)


def delete_card(request, deck_id, card_id):
    card = get_object_or_404(Card, id=card_id)
    if str(card.deck.id) == deck_id:
        card.delete()
    else:
        raise Http404("Card does not belong to deck")
    return redirect("/edit/deck_{}/cards".format(deck_id))