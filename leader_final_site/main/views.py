import django_filters
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render as django_render, redirect
from django.http import HttpResponse
from django.shortcuts import render as django_render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView
from django_filters.views import FilterView
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as django_login
from groups_manager.models import Member

from main.models import Card, CardType


def render(request, *args, **kwargs):
    if len(args) > 1:
        args[1]["data"] = get_down_menu_data(request)
    elif "context" in kwargs:
        kwargs["context"]["data"] = get_down_menu_data(request)
    else:
        kwargs["context"] = {"data": get_down_menu_data(request)}
    return django_render(request, *args, **kwargs)


def get_down_menu_data(request):
    total_cards = Card.objects.filter(to_users__django_user=request.user) \
                  | Card.objects.filter(to_groups__group_members__django_user=request.user)
    viewed_cars = total_cards.filter(views__django_user=request.user)
    data = [
        ("Заявки", "requests",
         total_cards.filter(cls=1).count() - viewed_cars.filter(cls=1).count()),
        ("Сообщения", "messages",
         total_cards.filter(cls=2).count() - viewed_cars.filter(cls=2).count()),
        ("Поручения", "missions",
         total_cards.filter(cls=3).count() - viewed_cars.filter(cls=3).count())
    ]
    return data


@login_required
def index(request):
    return render(request, "main/index.html", context={})


@login_required
def requests(request):
    cards = Card.objects.filter(cls=1)
    f = CardsFilter(request.GET, queryset=cards)
    return render(request, "main/requests.html", {'filter': f})


@login_required
def messages(request):
    cards = Card.objects.filter(cls=2)
    f = CardsFilter(request.GET, queryset=cards)
    return render(request, "main/messages.html", {'filter': f})


@login_required
def missions(request):
    cards = Card.objects.filter(cls=3)
    f = CardsFilter(request.GET, queryset=cards)
    return render(request, "main/missions.html", {'filter': f})


def login(request):
    return django_render(request, "main/login.html", {"ip_address": "/"})


@login_required
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


class CardsListView(FilterView, LoginRequiredMixin):
    paginate_by = 10
    template_name = 'main/cards.html'
    context_object_name = 'cards'
    filterset_class = CardsFilter

    def get_queryset(self):
        queryset = Card.objects.filter(to_users__django_user=self.request.user) \
                   | Card.objects.filter(to_groups__group_members__django_user=self.request.user)
        return queryset


class CardsCreateView(CreateView, LoginRequiredMixin):
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
        card.creator = Member.objects.filter(django_user=self.request.user).first()
        card.save()
        return redirect('cards')


class CardDetailView(DetailView, LoginRequiredMixin):
    model = Card

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        obj.views.add(Member.objects.filter(django_user=self.request.user).first())
        return obj
