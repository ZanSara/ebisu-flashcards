from typing import Any, List, Mapping, Union

import os

from flask import render_template

from ebisu_flashcards.database import models
from ebisu_flashcards.operations.serialization import SerializationMixin
from ebisu_flashcards.operations.server_side_rendering import DeckRenderingMixin



class DeckMixin(DeckRenderingMixin, SerializationMixin):
    """
        Mixin for deck management related functions.
        Bridges the gap bewteen the API and the Database.
    """

    def get_deck(self, user_id: str, deck_id: str) -> Union['Deck', List['Deck']]:
        """
            Returns the deck entity requested by the user.
            if deck_id == 'all', returns the list of all the decks of the user.

            :param user_id: Id of the user to retrieve decks for.
            :param deck_id: Id of the requested deck. 
                If 'all', returns all the decks for the user
            :returns: Deck or list of Deck objects from the database
            :raises models.Deck.DoesNotExist if the deck does not exist for this user
        """
        if deck_id == 'all':
            return models.Deck.objects(author=user_id).all()
        return models.Deck.objects.get(author=user_id, id=deck_id)


    def create_deck(self, user_id: str, data: Mapping[str, Any]) -> 'Deck':
        """
            Creates a new deck with the input data from the user's form

            :param user_id: Id of the user to create the new deck for.
            :returns: the newly created Deck database entity
        """
        # Create deck
        user = models.User.objects.get(id=user_id)
        deck = models.Deck(**data, author=user)
        deck.save()
        # Update user's decks list
        user.update(push__decks=deck)
        user.save()
        return deck
        

    def update_deck(self, user_id: str, deck_id: str, data: Mapping[str, Any]) -> 'Deck':
        """
            Updates an existing deck with the input data from the user's form

            :param user_id: Id of the user the deck belongs to.
            :param deck_id: Id of the deck to update
            :param data: the data to update the deck with
            :returns: the updated Deck database entity
            :raises models.Deck.DoesNotExist if the deck does not exist for this user
        """
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        deck.update(**data)
        deck.reload()
        return deck


    def delete_deck(self, user_id: str, deck_id: str) -> None:
        """
            Deletes an existing deck

            :param user_id: Id of the user the deck belongs to
            :param deck_id: Id of the deck to update
            :returns: the updated Deck database entity
            :raises models.Deck.DoesNotExist if the deck does not exist for this user
        """
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        deck.delete()
