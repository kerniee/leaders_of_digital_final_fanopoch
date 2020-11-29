import django_filters
from django.shortcuts import render as django_render, redirect
from django.http import HttpResponse
from django.shortcuts import render as django_render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView
from django_filters.views import FilterView
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as django_login
from groups_manager.models import Member

from main.models import Card, CardType, Worker


def render(request, *args, **kwargs):
    if len(args) > 1:
        args[1]["data"] = get_down_menu_data(request)
    elif "context" in kwargs:
        kwargs["context"]["data"] = get_down_menu_data(request)
    else:
        kwargs["context"] = {"data": get_down_menu_data(request)}
    return django_render(request, *args, **kwargs)


def get_down_menu_data(request):
    u = request.user
    # TODO:
    data = [
        ("Обязанности", "requests", 22),
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


def login(request):
    return django_render(request, "main/login.html", {"ip_address": "/"})


def logout_process(request):
    logout(request)
    return redirect("index")


def process_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        django_login(request, user)
        return redirect("index")
    else:
        return redirect("login")


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
    context_object_name = 'cards'
    filterset_class = CardsFilter

    def get_queryset(self):
        queryset = Card.objects.filter(to_users__django_user=self.request.user) \
                   | Card.objects.filter(to_groups__group_members__django_user=self.request.user)
        return queryset


class MyCardsView(FilterView):
    paginate_by = 10
    template_name = 'main/cards.html'
    context_object_name = 'cards'
    filterset_class = CardsFilter

    def get_queryset(self):
        return Card.objects.filter(creator=Member.objects.filter(django_user=self.request.user).first())


class CardsCreateView(CreateView):
    model = Card
    fields = (
        'header',
        'cls',
        'type',
        'priority',
        'deadline',
        'to_users',
        'to_groups'
    )

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['data'] = get_down_menu_data(self.request)
        return context

    def form_valid(self, form):
        card = form.save(commit=False)
        card.creator = Worker.objects.filter(django_user=self.request.user).first()
        card.save()
        return redirect('cards')


class CardDetailView(DetailView):
    model = Card

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['data'] = get_down_menu_data(self.request)
        return context

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        obj.views.add(Worker.objects.filter(django_user=self.request.user).first())
        return obj
