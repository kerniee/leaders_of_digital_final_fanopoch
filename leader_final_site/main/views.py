from django.shortcuts import render
from django.http import HttpResponse


def get_down_menu_data():
    data = [
        ("Заявки", "requests", 22),
        ("Сообщения", "messages", 0),
        ("Поручения", "missions", 2)
    ]
    return data


def index(request):
    return render(request, "main/index.html", {"data": get_down_menu_data()})


def requests(request):
    return render(request, "main/requests.html", {"data": get_down_menu_data()})


def messages(request):
    return render(request, "main/messages.html", {"data": get_down_menu_data()})


def missions(request):
    return render(request, "main/missions.html", {"data": get_down_menu_data()})
