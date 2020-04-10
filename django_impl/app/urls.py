from django.urls import path

from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Study cards
    path('deck_<int:deck_id>/study', views.study, name='study'),
    path('deck_<int:deck_id>/card_<int:card_id>/study', views.study, name='study'),

    # Edit decks and cards
    path('deck_<int:deck_id>/edit', views.edit_deck, name='edit_deck'),
    path('deck_<int:deck_id>/card_<int:card_id>/edit', views.edit_card, name='edit_card'),
    path('deck_<int:deck_id>/add', views.add_card, name='add_card'),
    path('deck_<int:deck_id>/card_<int:card_id>/delete', views.delete_card, name='delete_card'),
    
]