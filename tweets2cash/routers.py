# -*- coding: utf-8 -*-

from rest_framework import routers
from django.conf import settings

router = routers.DefaultRouter(trailing_slash=False)

# Locales
from tweets2cash.locale.api import LocalesViewSet

router.register(r"locales", LocalesViewSet, base_name="locales")


# Users & Roles
from tweets2cash.auth.api import AuthViewSet
from tweets2cash.users.api import UsersViewSet

router.register(r"auth", AuthViewSet, base_name="auth")
router.register(r"users", UsersViewSet, base_name="users")
