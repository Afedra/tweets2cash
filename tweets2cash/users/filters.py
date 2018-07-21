# -*- coding: utf-8 -*-

from rest_framework.filters import FilterBackend
from django.apps import apps
from django.db.models import Q
from rest_framework import exceptions as exc

#####################################################################
# User filters
#####################################################################

class UserFilterBackend(FilterBackend):

    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            qs = queryset
        else:
            qs = queryset.filter(username=request.user.username)

        return qs.distinct()
