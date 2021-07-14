from typing import List, Union

from ebisu_flashcards.database import models



class TemplateOps:
    """
        Mixin for deck management related functions.
        Bridges the gap bewteen the API and the Database.
    """

    def get_template(self, template_id: str) -> Union['Template', List['Template']]:
        """
            Returns the deck entity requested by the user.
            if deck_id == 'all', returns the list of all the decks of the user.

            :param user_id: Id of the user to retrieve decks for.
            :param deck_id: Id of the requested deck. 
                If 'all', returns all the decks for the user
            :param name: "class" of template (question or answer)
            :returns: Deck or list of Deck objects from the database
            :raises models.Deck.DoesNotExist if the deck does not exist for this user
        """
        if template_id == 'all':
            return models.Template.objects().all()
        return models.Template.objects.get(id=template_id)
