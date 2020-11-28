from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from main.models import User, Card


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'parent_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


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
