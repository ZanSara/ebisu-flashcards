from django.forms import ModelForm
from app.models.base import Tag, CardLayout

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"

class CardLayoutForm(ModelForm):
    class Meta:
        model = CardLayout
        fields = "__all__"
