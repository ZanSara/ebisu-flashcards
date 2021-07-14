from typing import Any, List, Mapping, Union

from ebisu_flashcards.database import models



class CardOps:
    """
        Mixin for card management related functions.
        Bridges the gap bewteen the API and the Database.
    """

    def get_card(self, user_id: str, deck_id: str, card_id: str) -> Union['Card', List['Card']]:
        """
            Returns the card entity requested by the user.
            if card_id == 'all', returns the list of all the cards of the given deck.

            :param user_id: the user to retrieve decks for.
            :param deck_id: Id of the requested deck.
            :param card_id: Id of the requested card. 
                If 'all', returns all the cards for the deck
            :returns: Card or list of Card objects from the database
            :raises models.Card.DoesNotExist if the card does not exist in this deck
            :raises models.Deck.DoesNotExist if the deck does not exist for this user
        """
        # Retrieves the deck to make sure it belongs to the user
        models.Deck.objects.get(id=deck_id, author=user_id)
        if card_id == 'all':
            return models.Card.objects(deck=deck_id).all()
        return models.Card.objects.get(id=card_id, deck=deck_id)


    def create_card(self, user_id: str, deck_id: str, data: Mapping[str, Any]) -> 'Card':
        """
            Creates a new card with the input data from the user's form

            :param user_id: the user to create the new card for.
            :param deck_id: the deck to add the new card to.
            :returns: the newly created Card database entity
            :raises models.Deck.DoesNotExist if the deck does not exist for this user
        """
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        card = models.Card(**data, deck=deck)
        card.save()
        card.reload()
        return card
        

    def update_card(self, user_id: str, deck_id: str, card_id: str, data: Mapping[str, Any]) -> 'Card':
        """
            Updates an existing card with the input data from the user's form

            :param user_id: the user the deck belongs to
            :param deck_id: the deck the card belongs to
            :param deck_id: Id of the card to update
            :param data: the data to update the card with
            :returns: the updated Card database entity
            :raises models.Deck.DoesNotExist if the deck does not exist for this user
            :raises models.Card.DoesNotExist if the card does not exist in this deck
        """
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        card = models.Card.objects.get(id=card_id)
        if deck.id != card.deck.id:
            raise models.Card.DoesNotExist("Card does not belong to deck") 
        card.update(**data)
        card.save().reload()
        return card
              

    def delete_card(self, user_id: str, deck_id: str, card_id: str) -> None:
        """
            Deletes an existing card

            :param user_id: ID of the user the deck belongs to
            :param deck_id: Id of the deck the card belongs to
            :param card_id: Id of the card to delete
            :returns: the updated Card database entity
            :raises models.Deck.DoesNotExist if the deck does not exist for this user
            :raises models.Card.DoesNotExist if the card does not exist in this deck
        """
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        card = models.Card.objects.get(id=card_id, deck=deck_id)
        card.delete()