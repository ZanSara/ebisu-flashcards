from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader

from app.mappings import CARD_TYPE_BY_DECK, FORM_TYPE_BY_CARD
from app.models.abc import AbstractDeck, AbstractCard


def home(request):
    AbstractCard.objects.all().delete()


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
        'question': card.question.get_content(),
        'answer': card.answer.get_content(),
    }
    return render(request, 'app/study.html', context)


def edit_deck(request, deck_id):
    deck = get_object_or_404(AbstractDeck, id=deck_id)

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
    }
    return render(request, 'app/deck-edit.html', context)


def edit_card(request, deck_id, card_id):
    deck = get_object_or_404(AbstractDeck, id=deck_id)
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
    deck = get_object_or_404(AbstractDeck, id=deck_id)
    cardtype = CARD_TYPE_BY_DECK[deck.__class__]
    card_dict = None
    
    if request.method == 'POST':
        card_form = FORM_TYPE_BY_CARD[cardtype](request)
        question = request.POST.get("question")
        answer = request.POST.get("answer")
        new_card = cardtype.objects.create(question=question, answer=answer, deck_id=deck.id)

    return redirect("/deck_{}/edit".format(deck_id))


def delete_card(request, deck_id, card_id):
    card = get_object_or_404(AbstractCard, id=card_id, deck=deck_id)    
    card.delete()
    return redirect("/deck_{}/edit".format(deck_id))