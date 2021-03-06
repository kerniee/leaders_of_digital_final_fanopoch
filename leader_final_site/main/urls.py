from django.urls import path

from . import views
from .views import CardsCreateView, CardDetailView, MyCardsView, CardUpdateView

urlpatterns = [
    path("", views.index, name="index"),
    path("cards", MyCardsView.as_view(), name="cards"),
    path("requests/", views.requests, name="requests"),
    path("messages/", views.messages, name="messages"),
    path("missions/", views.missions, name="missions"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout_process, name="logout_process"),
    path("login/process", views.process_login, name="process_login"),
    path("cards/new", CardsCreateView.as_view(), name="new_card"),
    path("cards/<int:pk>", CardDetailView.as_view(), name="detail"),
    path("cards/reply", views.process_reply, name="reply"),
    path("cards/<int:pk>/edit", CardUpdateView.as_view(), name="edit_card")
]
