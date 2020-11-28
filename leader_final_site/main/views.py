import django_filters
from django.shortcuts import render as django_render
from django.http import HttpResponse
from django.views.generic import ListView
from django_filters.views import FilterView

from main.models import Card


def render(*args, **kwargs):
    if len(args) > 2:
        args[2]["data"] = get_down_menu_data()
    elif "context" in kwargs:
        kwargs["context"]["data"] = get_down_menu_data()
    else:
        kwargs["context"] = {"data": get_down_menu_data()}
    return django_render(*args, **kwargs)


def get_down_menu_data():
    data = [
        ("Заявки", "requests", 22),
        ("Сообщения", "messages", 0),
        ("Поручения", "missions", 2)
    ]
    return data


def index(request):
    return render(request, "main/index.html", context={})


def requests(request):
    cards = Card.objects.filter(type=1)
    f = CardsFilter(request.GET, queryset=cards)
    return render(request, "main/requests.html", {'filter': f})


def messages(request):
    cards = Card.objects.filter(type=2)
    f = CardsFilter(request.GET, queryset=cards)
    return render(request, "main/messages.html", {'filter': f})


def missions(request):
    cards = Card.objects.filter(type=3)
    f = CardsFilter(request.GET, queryset=cards)
    return render(request, "main/missions.html", {'filter': f})


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
        fields = ['priority', 'creator', 'cls']


class CardsListView(FilterView):
    paginate_by = 10
    template_name = 'main/cards.html'
    model = Card
    context_object_name = 'cards'
    filterset_class = CardsFilter
