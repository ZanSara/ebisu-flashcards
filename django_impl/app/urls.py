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

    # Edit decks
    path('edit/new_deck', views.new_deck, name='new_deck'),
    path('edit/deck_<str:deck_id>/properties', views.edit_deck_properties, name='edit_deck_properties'),
    path('edit/deck_<str:deck_id>/cards', views.list_cards, name='list_cards'),
    path('edit/deck_<str:deck_id>/delete', views.delete_deck, name='delete_deck'),

    # Edit cards
    path('edit/deck_<str:deck_id>/new_card', views.new_card, name='new_card'),
    path('edit/deck_<str:deck_id>/card_<str:card_id>', views.edit_card, name='edit_card'),
    path('edit/deck_<str:deck_id>/card_<str:card_id>/delete', views.delete_card, name='delete_card'),

    # Edit renderers
    # path('edit/renderers', views.edit_renderers, name='edit_renderers'),
]