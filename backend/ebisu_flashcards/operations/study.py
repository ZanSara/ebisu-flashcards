from typing import Any, Mapping

from ebisu_flashcards.database import models, algorithms


class StudyOps:
    """
        Mixin for study related functions.
        Bridges the gap bewteen the API and the Database.
    """

    def get_next_card(self, user_id: str, deck_id: str) -> 'Card':
        """
            Gives the next card in the deck to be studied.
            FIXME will break if deck does not belong to user, but the
                exception is not well managed.

            :param deck_id: Deck to take the card from
            :param user_id: deck owner, for validation
            :returns: a database Card object.
        """
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        algorithm = algorithms.algorithm_engine(deck)
        next_card = algorithm.next_card_to_review()
        return next_card


    def process_test_results(self, user_id: str, deck_id: str, card_id: str, test_results: Mapping[str, Any]) -> None:
        """
            Saves the results of a test.

            :param user_id: deck owner, for validation
            :param deck_id: Deck to take the card from
            :param card_id: Card reviewed
            :param test_results: the content of the form of the user, as a dictionary.
                Passed to the algorihtm as a series of arg=value.
            :returns: Nothing.
            :raises models.Card.DoesNotExist if the card does not exist in this deck
            :raises models.Deck.DoesNotExist if the deck does not exist for this user
        """
        deck = models.Deck.objects.get(id=deck_id, author=user_id)
        card = models.Card.objects.get(id=card_id, deck=deck_id)
        algorithm = algorithms.algorithm_engine(deck)
        algorithm.process_result(**test_results, user_id=user_id)
