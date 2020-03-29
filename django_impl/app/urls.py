from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('deck_<int:deck_id>/study', views.study, name='study'),
    path('deck_<int:deck_id>/card_<int:card_id>/study', views.study, name='study'),
]