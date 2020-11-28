import django_filters
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django_filters.views import FilterView

from main.models import Card


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


class CardsFilter(django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        fields=(
            ('priority', 'priority'),
            ('deadline', 'deadline'),
            ('finished_at', 'finished_at'),
            ('created_at', 'created_at')
        ),
        field_labels={
            'priority': 'Приоритет',
            'deadline': 'Дедлайн',
            'finished_at': 'Завершено',
            'created_at': 'Создано'
        }
    )

    class Meta:
        model = Card
        fields = ['priority', 'creator', 'cls', 'type']


class CardsListView(FilterView):
    paginate_by = 10
    template_name = 'main/cards.html'
    model = Card
    context_object_name = 'cards'
    filterset_class = CardsFilter
