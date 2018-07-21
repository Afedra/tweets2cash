# -*- coding: utf-8 -*-

from rest_framework.permissions import BasePermission
from django.apps import apps


class IsTheSameUser(BasePermission):
    def has_object_permission(self, request, view, obj=None):
        return obj and request.user.is_authenticated() and (request.user.pk == obj.pk)
