import os

from django.db import models
from django.template import loader
from django.utils.html import strip_tags

from app.models.abc import AbstractCardFact


class TextCardFact(AbstractCardFact):
    content = models.CharField(max_length=2000)

    def get_content(self):
        return render_to_string(
            'app/fact_templates/default_fact_template.html', 
            {'content': content})
    
    def __str__(self):
        return self.content


class HtmlCardFact(AbstractCardFact):
    content = models.CharField(max_length=2000)

    def get_content(self):
        return render_to_string(
            'app/fact_templates/html_fact_template.html', 
            {'content': content})
    
    def __str__(self):
        return strip_tags(self.content)


class ImageCardFact(AbstractCardFact):
    content = models.FilePathField(
        max_length=500,
        path=os.path.join(os.getcwd(), 
                "app", 
                "uploads",
                "app",
                "image_facts"))

    def get_content(self):
        return render_to_string(
            'app/card_templates/image_card_template.html', 
            {'content': content})

    def __str__(self):
        return self.content.split(os.path.sep)[-1]