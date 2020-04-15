from django.urls import path

from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('reset-password', views.reset_password, name='reset_password'),

    # Study cards
    path('study/deck_<str:deck_id>', views.study, name='study'),
    path('study/deck_<str:deck_id>/card_<str:card_id>', views.study, name='study'),

    # Edit decks and cards
    path('edit/new_deck', views.edit_deck, name='edit_deck'),
    path('edit/deck_<str:deck_id>', views.edit_deck, name='edit_deck'),
    path('edit/deck_<str:deck_id>/delete', views.delete_deck, name='delete_deck'),
    path('edit/deck_<str:deck_id>/card_<str:card_id>', views.edit_card, name='edit_card'),
    path('edit/deck_<str:deck_id>/new_card', views.edit_card, name='edit_card'),
    path('edit/deck_<str:deck_id>/card_<str:card_id>/delete', views.delete_card, name='delete_card'),
    
]