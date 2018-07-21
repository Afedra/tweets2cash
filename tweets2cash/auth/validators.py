# -*- coding: utf-8 -*-

from django.core import validators as core_validators
from django.utils.translation import ugettext as _

from rest_framework import serializers
from django.core.exceptions import ValidationError

import re


class BaseRegisterValidator(serializers.Serializer):
    full_name = serializers.CharField(max_length=256, required=False)
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=4)

    def validate_username(self, value):
        validator = core_validators.RegexValidator(re.compile('^[\w.-]+$'), _("invalid username"), "invalid")

        try:
            validator(value)
        except ValidationError:
            raise ValidationError(_("Required. 150 characters or fewer. Letters, numbers "
                                    "and /./-/_ characters'"))
        return value


class PublicRegisterValidator(BaseRegisterValidator):
    pass

