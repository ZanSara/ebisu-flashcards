from django.forms import ModelForm
from app.models.ebisu import EbisuCardModel, EbisuCard, EbisuDeck


class EbisuCardModelForm(ModelForm):
    class Meta:
        model = EbisuCardModel
        fields = "__all__"

class EbisuDeckForm(ModelForm):
    class Meta:
        model = EbisuDeck
        fields = "__all__"


class EbisuCardForm(ModelForm):
    class Meta:
        model = EbisuCard
        fields = "__all__"
