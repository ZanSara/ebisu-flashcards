from typing import Any, Mapping
import abc
import mongoengine as mongo
from django.utils import timezone

from ..base import Tag, User, Fact, Renderer

BOOLEAN_WIDGET = 'boolean-fact.html'
TEXT_WIDGET = 'text-fact.html'
HTML_WIDGET = 'html-fact.html'
IMAGE_WIDGET = 'image-fact.html'


class Review(mongo.EmbeddedDocument):
    user = mongo.ReferenceField(User)
    test_results = mongo.StringField()  # Can store more complex objects as JSON in case, I guess...
    review_time = mongo.DateTimeField(default=timezone.now)

    meta = {'allow_inheritance': True}


class Card(mongo.Document):
    question = mongo.ReferenceField(Fact)
    answer = mongo.ReferenceField(Fact)
    tags = mongo.ListField(Tag, blank=True)
    marked = mongo.BooleanField(default=False)
    hidden = mongo.BooleanField(default=False)
    reviews = mongo.ListField(mongo.EmbeddedDocumentField(Review))

    meta = {'allow_inheritance': True}


    @abc.abstractmethod
    def populate_fields_from_postdata(self, postdata: Mapping[str, Any]) -> None :
        """ Returns the card instance populated from the info contained into the POSTDATA dict. """
        # question_renderer = None
        # try:
        #     # if postdata.get('question_renderer'): 
        #     #     raise mongo.DoesNotExist()
        #     question_renderer = Renderer.objects.get(name=postdata.get('question_renderer'))
        # except mongo.DoesNotExist:
        #     question_renderer = Renderer(name="Text Renderer", description="A renderer for text", renderer="text-fact.html")
        #     question_renderer.save()
            
        # answer_renderer = None
        # try:
        #     # if postdata.get('answer_renderer'): 
        #     #     raise mongo.DoesNotExist()
        #     answer_renderer = Renderer.objects.get(name=postdata.get('answer_renderer'))
        # except mongo.DoesNotExist:
        #     answer_renderer = Renderer("Text Renderer", "A renderer for text", "text-fact.html")
        #     answer_renderer.save()

        # Renderer(name="HTML Renderer", description="A renderer for HTML", path="html-fact.html").save()
        default_renderer = Renderer.objects.get(name="Text Renderer")

        question = Fact(fact=postdata.get('question'), renderer=default_renderer)
        question.save()
        answer = Fact(fact=postdata.get('answer'), renderer=default_renderer)
        answer.save()
        self.question = question.id
        self.answer = answer.id
        # process tags
        # self.tags = postdata.get('tags')
        self.marked = postdata.get('marked')
        self.hidden = postdata.get('hidden')


    @abc.abstractmethod
    def to_dict(self):
        question = Fact.objects.get(id=self.question)
        answer = Fact.objects.get(id=self.answer)
        own_dict = {
            'id': self.id,
            'question': question,
            'answer': answer,
            'tags': self.tags,
            'marked': self.marked,
            'hidden': self.hidden,
        }
        return own_dict

    @abc.abstractmethod
    def to_widgets(self):
        own_form = {
            'id': self.id,  # Won't be displayed
            'question': self.question,
            'answer': self.answer,
            'tags':  {
                'value': self.tags, 
                'widget': TEXT_WIDGET
            },
            'marked': {
                'value': self.marked, 
                'widget': BOOLEAN_WIDGET
            },
            'hidden': {
                'value': self.hidden, 
                'widget': BOOLEAN_WIDGET
            },
        }
        return own_form
