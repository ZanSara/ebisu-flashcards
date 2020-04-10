from django.forms import ModelForm
from app.models.random_order import RandomOrderCardModel, RandomOrderCard, RandomOrderDeck


class RandomOrderCardModelForm(ModelForm):
    class Meta:
        model = RandomOrderCardModel
        fields = "__all__"

class RandomOrderDeckForm(ModelForm):
    class Meta:
        model = RandomOrderDeck
        fields = "__all__"


class RandomOrderCardForm(ModelForm):
    class Meta:
        model = RandomOrderCard
        fields = "__all__"
