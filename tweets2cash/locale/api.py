# -*- coding: utf-8 -*-

from django.conf import settings
from rest_framework import response
from rest_framework.viewsets import ViewSet
from rest_framework import permissions


class LocalesViewSet(ViewSet):
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        locales = [{"code": c, "name": n, "bidi": c in settings.LANGUAGES_BIDI} for c, n in settings.LANGUAGES]
        return response.Ok(locales)
