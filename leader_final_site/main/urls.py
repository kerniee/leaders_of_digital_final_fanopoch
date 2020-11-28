from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("requests/", views.requests, name="requests"),
    path("messages/", views.messages, name="messages"),
    path("missions/", views.missions, name="missions"),
]
