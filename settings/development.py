# -*- coding: utf-8 -*-

from .common import *

DEBUG = True

TEMPLATES[0]["OPTIONS"]['context_processors'] += "django.template.context_processors.debug"
