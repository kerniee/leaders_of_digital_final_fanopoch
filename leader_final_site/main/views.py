import django_filters
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django_filters.views import FilterView

from main.models import Card


def index(request):
    return render(request, "main/index.html")


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
