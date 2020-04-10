from django import forms
from django.contrib import admin

from app.models.base import FactLayout, Tag
from app.models.facts import TextCardFact, HtmlCardFact, ImageCardFact
from app.models.ebisu import EbisuDeck, EbisuCard, EbisuCardModel
from app.models.random_order import RandomOrderDeck, RandomOrderCard, RandomOrderCardModel

admin.site.site_header = "Ebisu Flashcards Admin"
admin.site.site_title = "Ebisu Flashcards Admin Page"
admin.site.index_title = "Database Management Page"

admin.site.register(FactLayout)
admin.site.register(Tag)

admin.site.register(TextCardFact)
admin.site.register(HtmlCardFact)
admin.site.register(ImageCardFact)


class EbisuCardAdmin(admin.ModelAdmin):

    class CustomModelChoiceField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return obj.name

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'deck_id':
            return self.CustomModelChoiceField(queryset=EbisuDeck.objects)

        return super(EbisuCardAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class EbisuCardModelAdmin(admin.ModelAdmin):

    class CustomModelChoiceField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return str(obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'card_id':
            return self.CustomModelChoiceField(queryset=EbisuCard.objects)

        return super(EbisuCardModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(EbisuDeck)
admin.site.register(EbisuCard, EbisuCardAdmin)
admin.site.register(EbisuCardModel, EbisuCardModelAdmin)


# FIXME Can I remove this duplication?

class RandomOrderCardAdmin(admin.ModelAdmin):

    class CustomModelChoiceField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return obj.name

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'deck_id':
            return self.CustomModelChoiceField(queryset=RandomOrderDeck.objects)

        return super(RandomOrderCardAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class RandomOrderCardModelAdmin(admin.ModelAdmin):

    class CustomModelChoiceField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return str(obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'card_id':
            return self.CustomModelChoiceField(queryset=RandomOrderCard.objects)

        return super(RandomOrderCardModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(RandomOrderDeck)
admin.site.register(RandomOrderCard, RandomOrderCardAdmin)
admin.site.register(RandomOrderCardModel, RandomOrderCardModelAdmin)