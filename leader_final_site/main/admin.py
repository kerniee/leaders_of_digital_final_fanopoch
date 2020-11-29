from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from groups_manager.models import Member

from main.models import Card, CardType


@admin.register(CardType)
class CardTypeAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_filter = [
        'cls',
        'type',
        'is_finished'
    ]
    list_display = [
        'header',
        'cls',
        'type',
        'priority',
        'deadline',
        'is_finished',
        'finished_at',
        'creator',
        'created_at'
    ]
    sortable_by = [
        'created_at',
        'finished_at',
        'priority',
        'deadline'
    ]
