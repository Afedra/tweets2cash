# -*- coding: utf-8 -*-

from .development import *

CELERY_ENABLED = False

MEDIA_ROOT = "/tmp"

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
INSTALLED_APPS = INSTALLED_APPS + [
    "tests",
]

REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "anon-write": None,
    "anon-read": None,
    "user-write": None,
    "user-read": None,
    "login-fail": None,
    "register-success": None,
    "user-detail": None,
    "user-update": None,
}
