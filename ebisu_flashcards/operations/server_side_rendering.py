from typing import Any, List, Mapping, Union

import os

from flask import render_template

from ebisu_flashcards.database import models



class DeckRenderingMixin:
    """
        Mixin for the Server Side Rendering of the Decks.
    """

    def server_side_rendering(self, deck: 'Deck') -> 'Deck':
        """
            Perform server-side rendering of the templated fields of a Deck.

            :param db_deck: the Deck object which fields will be pre-rendered.
            :returns: a partially pre-rendered Deck object.
        """
        template_path = os.path.join("deck-templates", deck.algorithm+".html")
        deck.extra_fields = render_template(template_path, deck=deck)

        return deck


class CardRenderingMixin:
    """
        Mixin for the Server Side rendering functions of a Card object.
    """

    def server_side_rendering(self, card: 'Card') -> 'Card':
        """
            Perform server-side rendering of the templated fields of a Card.

            :param card: the Card object which fields will be pre-rendered.
            :returns: a partially pre-rendered Card object.
        """
        # Static view of question
        question_path = os.path.join("card-templates", card.question_template.path)
        card.question_display = render_template(question_path, content=card.question)

        # Static view of answer
        answer_path = os.path.join("card-templates", card.answer_template.path)
        card.answer_display = render_template(answer_path, content=card.answer)

        # Form view of question
        question_form_path = os.path.join("card-form-templates", card.question_template.path)
        card.question_form = render_template(question_form_path, name="question", content=card.question)

        # Form view of answer
        answer_form_path = os.path.join("card-form-templates", card.answer_template.path)
        card.answer_form = render_template(answer_form_path, name="answer", content=card.answer)

        return card


    def server_side_parsing(self, data: Mapping[str, Any]) -> Mapping[str, Any]:
        """
            Resolves the fields of a Card that are supposed to be references in the DB.

            :param data: the information coming from the webpage, as a dictionary
            :returns: the data with References instead of strings where appropriate.
        """
        # Trasform template fields into references
        data["question_template"] = models.Template.objects.get(name=data["question_template"])
        data["answer_template"] = models.Template.objects.get(name=data["answer_template"])
        return data
