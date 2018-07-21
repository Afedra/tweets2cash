# -*- coding: utf-8 -*-

from django.apps import apps

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from django.utils.translation import ugettext_lazy as _

from . import  models
from .forms import UserChangeForm, UserCreationForm

## Admin panels
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("full_name", "email", "bio", "photo")}),
        (_("Extra info"), {"fields": ("token", "email_token", "new_email")}),
        (_("Permissions"), {"fields": ("is_active", "is_superuser")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("username", "email", "full_name")
    list_filter = ("is_superuser", "is_active")
    search_fields = ("username", "full_name", "email")
    ordering = ("username",)
    filter_horizontal = ()

admin.site.register(models.User, UserAdmin)
