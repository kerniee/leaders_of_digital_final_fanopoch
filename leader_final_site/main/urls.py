from django.urls import path

from . import views
from .views import CardsListView

urlpatterns = [
    path("", views.index, name="index"),
    path("cards", CardsListView.as_view(), name="cards")
]
