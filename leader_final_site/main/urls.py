from django.urls import path

from . import views
from .views import CardsListView, CardsCreateView

urlpatterns = [
    path("", views.index, name="index"),
    path("cards", CardsListView.as_view(), name="cards"),
    path("requests/", views.requests, name="requests"),
    path("messages/", views.messages, name="messages"),
    path("missions/", views.missions, name="missions"),
    path("login/", views.login, name="login"),
    path("login/process", views.process_login, name="process_login"),
    path("cards/new", CardsCreateView.as_view(), name="new_card"),
    path("cards/new/process", views.process_new_card, name="process_new_card")
]
