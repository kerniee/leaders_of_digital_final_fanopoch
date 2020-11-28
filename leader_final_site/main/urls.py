from django.urls import path

from . import views
from .views import CardsListView

urlpatterns = [
    path("", views.index, name="index"),
    path("cards", CardsListView.as_view(), name="cards"),
    path("requests/", views.requests, name="requests"),
    path("messages/", views.messages, name="messages"),
    path("missions/", views.missions, name="missions"),
]
