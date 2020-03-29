from django.contrib import admin

from app.models.base import CardLayout, Tag
from app.models.ebisu import EbisuDeck, EbisuCard, EbisuCardModel

admin.site.register(CardLayout)
admin.site.register(Tag)

admin.site.register(EbisuDeck)
admin.site.register(EbisuCard)
admin.site.register(EbisuCardModel)